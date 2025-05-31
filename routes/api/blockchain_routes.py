"""
Blockchain API Routes
This module handles REST API endpoints for blockchain functionality
"""

import logging
import threading
from datetime import datetime
from flask import Blueprint, jsonify, request
from auth import login_required, admin_required, api_test_access
from blockchain import (
    init_web3, 
    get_settlement_contract, 
    get_multisig_wallet, 
    get_nvc_token,
    initialize_settlement_contract,
    initialize_multisig_wallet,
    initialize_nvc_token,
    create_new_settlement,
    settle_payment_via_contract,
    get_transaction_status,
    submit_multisig_transaction,
    confirm_multisig_transaction,
    transfer_nvc_tokens,
    get_nvc_token_balance
)
from blockchain_utils import generate_ethereum_account
from models import BlockchainTransaction, BlockchainAccount, SmartContract, db

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
blockchain_api = Blueprint('blockchain_api', __name__)

@blockchain_api.route('/status', methods=['GET'])
@api_test_access
def get_blockchain_status(user=None):
    """Get the current blockchain connection status"""
    try:
        # Attempt to initialize Web3
        web3 = init_web3()
        
        # Try to access blockchain data to verify connection
        try:
            network_id = web3.net.version
            # Fix: Get client version via RPC call to web3_clientVersion
            node_info = web3.manager.request_blocking("web3_clientVersion", [])
            latest_block = web3.eth.block_number
            
            # Successfully connected - calculate block time
            block_time = None
            if latest_block > 0:
                try:
                    current_block = web3.eth.get_block(latest_block)
                    previous_block = web3.eth.get_block(latest_block - 1)
                    block_time = current_block.timestamp - previous_block.timestamp
                except Exception as block_ex:
                    logger.warning(f"Could not calculate block time: {str(block_ex)}")
                    # Couldn't get block details but still connected
                    pass
            
            # Return success response with blockchain details
            return jsonify({
                'status': 'ok',
                'message': 'Blockchain connection established',
                'details': {
                    'network_id': network_id,
                    'node_info': node_info,
                    'latest_block': latest_block,
                    'block_time': block_time,
                },
                'lastChecked': datetime.utcnow().isoformat()
            })
        
        except Exception as e:
            # Connected but can't get all details
            logger.warning(f"Connected to blockchain but encountered an error: {str(e)}")
            return jsonify({
                'status': 'warning',
                'message': f'Connected to blockchain but encountered an error: {str(e)}',
                'lastChecked': datetime.utcnow().isoformat()
            })
            
    except Exception as e:
        # Failed to connect to blockchain
        logger.error(f"Error checking blockchain status: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error checking blockchain status: {str(e)}',
            'lastChecked': datetime.utcnow().isoformat()
        })

# Global deployment status
deployment_status = {
    "settlement_contract": {"status": "not_started", "address": None, "error": None},
    "multisig_wallet": {"status": "not_started", "address": None, "error": None},
    "nvc_token": {"status": "not_started", "address": None, "error": None}
}

@blockchain_api.route('/deployment/start', methods=['POST'])
@api_test_access
def deploy_all_contracts(user=None):
    """Deploy all smart contracts in the correct sequence"""
    global deployment_status
    
    # Import the UserRole enum
    from models import UserRole
    
    # Check if user has admin role
    if user and user.role != UserRole.ADMIN:
        return jsonify({
            'success': False,
            'message': 'Admin privileges required for contract deployment'
        }), 403
    
    # Reset deployment status
    deployment_status = {
        "settlement_contract": {"status": "PENDING", "address": None, "error": None},
        "multisig_wallet": {"status": "PENDING", "address": None, "error": None},
        "nvc_token": {"status": "PENDING", "address": None, "error": None}
    }
    
    # Start a background thread to handle deployments
    deployment_thread = threading.Thread(target=deploy_contracts_background)
    deployment_thread.daemon = True
    deployment_thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Deployment started in background',
        'status_endpoint': '/api/blockchain/deployment/status'
    })


def deploy_contracts_background():
    """Background function to deploy all contracts"""
    global deployment_status
    
    # Import app at function level to avoid circular imports
    from app import app
    
    # Use application context to ensure database operations work correctly
    with app.app_context():
        try:
            # 1. Deploy Settlement Contract
            logger.info("Starting Settlement Contract deployment...")
            deployment_status["settlement_contract"]["status"] = "in_progress"
            
            settlement_address, settlement_tx = initialize_settlement_contract()
            
            if settlement_address:
                deployment_status["settlement_contract"]["status"] = "completed"
                deployment_status["settlement_contract"]["address"] = settlement_address
                deployment_status["settlement_contract"]["tx_hash"] = settlement_tx
                logger.info(f"Settlement Contract deployed at: {settlement_address}")
            else:
                deployment_status["settlement_contract"]["status"] = "failed"
                deployment_status["settlement_contract"]["error"] = "Failed to deploy contract"
                logger.error("Settlement Contract deployment failed")
                return
                
            # 2. Deploy MultiSig Wallet
            logger.info("Starting MultiSig Wallet deployment...")
            deployment_status["multisig_wallet"]["status"] = "in_progress"
            
            # Get admin users for MultiSig owners
            from models import User, UserRole
            admins = User.query.filter_by(role=UserRole.ADMIN).all()
            
            # Get ethereum addresses for admins (or create new ones)
            owner_addresses = []
            for admin in admins:
                blockchain_account = BlockchainAccount.query.filter_by(user_id=admin.id).first()
                if blockchain_account:
                    owner_addresses.append(blockchain_account.eth_address)
                else:
                    # Generate a new account if needed
                    new_address, private_key = generate_ethereum_account()
                    owner_addresses.append(new_address)
            
            # Ensure we have at least 3 owners
            while len(owner_addresses) < 3:
                new_address, _ = generate_ethereum_account()
                owner_addresses.append(new_address)
                
            multisig_address, multisig_tx = initialize_multisig_wallet(owner_addresses, 2)
            
            if multisig_address:
                deployment_status["multisig_wallet"]["status"] = "completed"
                deployment_status["multisig_wallet"]["address"] = multisig_address
                deployment_status["multisig_wallet"]["tx_hash"] = multisig_tx
                logger.info(f"MultiSig Wallet deployed at: {multisig_address}")
            else:
                deployment_status["multisig_wallet"]["status"] = "failed"
                deployment_status["multisig_wallet"]["error"] = "Failed to deploy contract"
                logger.error("MultiSig Wallet deployment failed")
                
            # 3. Deploy NVC Token
            logger.info("Starting NVC Token deployment...")
            deployment_status["nvc_token"]["status"] = "in_progress"
            
            token_address, token_tx = initialize_nvc_token()
            
            if token_address:
                deployment_status["nvc_token"]["status"] = "completed"
                deployment_status["nvc_token"]["address"] = token_address
                deployment_status["nvc_token"]["tx_hash"] = token_tx
                logger.info(f"NVC Token deployed at: {token_address}")
            else:
                deployment_status["nvc_token"]["status"] = "failed"
                deployment_status["nvc_token"]["error"] = "Failed to deploy contract"
                logger.error("NVC Token deployment failed")
                
        except Exception as e:
            logger.error(f"Error during contract deployment sequence: {str(e)}")
            # Mark any pending deployments as failed
            for contract_name, status in deployment_status.items():
                if status["status"] in ["pending", "in_progress"]:
                    deployment_status[contract_name]["status"] = "failed"
                    deployment_status[contract_name]["error"] = str(e)


@blockchain_api.route('/deployment/status', methods=['GET'])
@api_test_access
def get_deployment_status():
    """Get the status of the contract deployments"""
    global deployment_status
    
    # Check if contracts exist in database
    from models import SmartContract, db
    
    # Update status from database for already deployed contracts
    settlement = SmartContract.query.filter_by(name="SettlementContract").first()
    multisig = SmartContract.query.filter_by(name="MultiSigWallet").first()
    token = SmartContract.query.filter_by(name="NVCToken").first()
    
    # Create response dictionary
    response = {}
    
    # Add settlement contract status
    if settlement:
        response["settlement_contract"] = {
            "status": "COMPLETED",
            "address": settlement.address
        }
    else:
        response["settlement_contract"] = {
            "status": deployment_status["settlement_contract"]["status"],
            "address": None
        }
        
    # Add multisig wallet status
    if multisig:
        response["multisig_wallet"] = {
            "status": "COMPLETED",
            "address": multisig.address
        }
    else:
        response["multisig_wallet"] = {
            "status": deployment_status["multisig_wallet"]["status"],
            "address": None
        }
        
    # Add NVC token status
    if token:
        response["nvc_token"] = {
            "status": "COMPLETED",
            "address": token.address
        }
    else:
        response["nvc_token"] = {
            "status": deployment_status["nvc_token"]["status"],
            "address": None
        }
    
    return jsonify(response)

# (Removed duplicate blockchain status endpoint)


@blockchain_api.route('/deployment/contract', methods=['POST'])
@api_test_access
def deploy_specific_contract(user=None):
    """Deploy a specific smart contract"""
    # Import the UserRole enum
    from models import UserRole
    
    # Check if user has admin role
    if user and user.role != UserRole.ADMIN:
        return jsonify({
            'success': False,
            'message': 'Admin privileges required for contract deployment'
        }), 403
    try:
        data = request.get_json()
        contract_type = data.get('contract_type')
        
        if not contract_type:
            return jsonify({
                'success': False,
                'message': 'Missing contract_type parameter'
            }), 400
            
        if contract_type == 'settlement_contract':
            contract_address, tx_hash = initialize_settlement_contract()
            contract_name = "Settlement Contract"
        elif contract_type == 'multisig_wallet':
            # Get a list of admin users to be owners
            from models import User, UserRole
            admins = User.query.filter_by(role=UserRole.ADMIN).all()
            
            # Use admin ethereum addresses if they exist, otherwise create new ones
            owner_addresses = []
            for admin in admins:
                blockchain_account = BlockchainAccount.query.filter_by(user_id=admin.id).first()
                if blockchain_account:
                    owner_addresses.append(blockchain_account.eth_address)
            
            # Add at least 3 addresses if not enough admins
            while len(owner_addresses) < 3:
                new_address, _ = generate_ethereum_account()
                owner_addresses.append(new_address)
            
            # Deploy with 2/3 required confirmations
            contract_address, tx_hash = initialize_multisig_wallet(owner_addresses, 2)
            contract_name = "MultiSig Wallet"
        elif contract_type == 'nvc_token':
            contract_address, tx_hash = initialize_nvc_token()
            contract_name = "NVC Token"
        else:
            return jsonify({
                'success': False,
                'message': f'Unknown contract type: {contract_type}'
            }), 400
        
        if contract_address:
            return jsonify({
                'success': True,
                'address': contract_address,
                'tx_hash': tx_hash,
                'message': f'{contract_name} deployment initiated'
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Failed to deploy {contract_name}'
            }), 500
    except Exception as e:
        logger.error(f"Error deploying contract: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@blockchain_api.route('/settlement/create', methods=['POST'])
@login_required
def create_settlement():
    """Create a new settlement using the settlement contract"""
    try:
        data = request.get_json()
        
        to_address = data.get('to_address')
        amount = float(data.get('amount'))
        metadata = data.get('metadata', '')
        
        # Get the user's ethereum address
        from flask_login import current_user
        blockchain_account = BlockchainAccount.query.filter_by(user_id=current_user.id).first()
        
        if not blockchain_account:
            # Create a new account if the user doesn't have one
            eth_address, private_key = generate_ethereum_account()
            blockchain_account = BlockchainAccount(
                user_id=current_user.id,
                eth_address=eth_address,
                eth_private_key=private_key
            )
            db.session.add(blockchain_account)
            db.session.commit()
        
        from_address = blockchain_account.eth_address
        private_key = blockchain_account.eth_private_key
        
        # Generate a transaction ID
        import uuid
        transaction_id = str(uuid.uuid4())
        
        # Create the settlement
        tx_hash = create_new_settlement(
            from_address=from_address,
            to_address=to_address,
            amount_in_eth=amount,
            private_key=private_key,
            transaction_id=transaction_id,
            tx_metadata=metadata
        )
        
        if tx_hash:
            # Save the transaction in the database
            blockchain_tx = BlockchainTransaction(
                user_id=current_user.id,
                from_address=from_address,
                to_address=to_address,
                eth_tx_hash=tx_hash,
                amount=amount,
                contract_address=get_settlement_contract().address,
                transaction_type='SETTLEMENT_CREATE',
                status='pending',
                tx_metadata=metadata
            )
            db.session.add(blockchain_tx)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'tx_hash': tx_hash,
                'transaction_id': transaction_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create settlement'
            }), 500
    except Exception as e:
        logger.error(f"Error creating settlement: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@blockchain_api.route('/settlement/<settlement_id>', methods=['GET'])
@login_required
def get_settlement(settlement_id):
    """Get details for a specific settlement"""
    try:
        # This would typically involve calling a function to get settlement details from the contract
        # For now, we'll return a mock response
        settlement_contract = get_settlement_contract()
        
        if not settlement_contract:
            return jsonify({
                'success': False,
                'message': 'Settlement contract is not deployed'
            }), 400
        
        # In a real implementation, we would get this from the contract:
        # settlement = settlement_contract.functions.getSettlement(settlement_id).call()
        
        # Mock data for demonstration
        settlement = {
            'id': settlement_id,
            'transactionId': 'tx_' + settlement_id,
            'from': '0x1234567890123456789012345678901234567890',
            'to': '0x0987654321098765432109876543210987654321',
            'amount': 1.5,
            'fee': 0.015,
            'status': 0,  # Pending
            'timestamp': 1617234567,
            'metadata': 'Test settlement'
        }
        
        return jsonify({
            'success': True,
            'settlement': settlement
        })
    except Exception as e:
        logger.error(f"Error getting settlement {settlement_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@blockchain_api.route('/settlement/<settlement_id>/complete', methods=['POST'])
@admin_required
def complete_settlement(settlement_id):
    """Complete a pending settlement"""
    try:
        # This would involve calling the contract to complete the settlement
        # For now, we'll return a mock response
        settlement_contract = get_settlement_contract()
        
        if not settlement_contract:
            return jsonify({
                'success': False,
                'message': 'Settlement contract is not deployed'
            }), 400
        
        # In a real implementation:
        # tx_hash = settlement_contract.functions.completeSettlement(settlement_id).transact()
        
        # Mock data
        tx_hash = '0x123456789abcdef123456789abcdef123456789abcdef123456789abcdef1234'
        
        return jsonify({
            'success': True,
            'tx_hash': tx_hash
        })
    except Exception as e:
        logger.error(f"Error completing settlement {settlement_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@blockchain_api.route('/settlement/<settlement_id>/cancel', methods=['POST'])
@admin_required
def cancel_settlement(settlement_id):
    """Cancel a pending settlement"""
    try:
        # This would involve calling the contract to cancel the settlement
        # For now, we'll return a mock response
        settlement_contract = get_settlement_contract()
        
        if not settlement_contract:
            return jsonify({
                'success': False,
                'message': 'Settlement contract is not deployed'
            }), 400
        
        # In a real implementation:
        # tx_hash = settlement_contract.functions.cancelSettlement(settlement_id).transact()
        
        # Mock data
        tx_hash = '0xabcdef123456789abcdef123456789abcdef123456789abcdef123456789abcd'
        
        return jsonify({
            'success': True,
            'tx_hash': tx_hash
        })
    except Exception as e:
        logger.error(f"Error cancelling settlement {settlement_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@blockchain_api.route('/multisig/submit', methods=['POST'])
@login_required
def submit_multisig():
    """Submit a transaction to the multisig wallet"""
    try:
        data = request.get_json()
        
        destination = data.get('destination')
        amount = float(data.get('amount'))
        tx_data = data.get('data', '0x')
        
        # Get the user's ethereum address
        from flask_login import current_user
        blockchain_account = BlockchainAccount.query.filter_by(user_id=current_user.id).first()
        
        if not blockchain_account:
            return jsonify({
                'success': False,
                'message': 'You do not have an associated Ethereum account'
            }), 400
        
        from_address = blockchain_account.eth_address
        private_key = blockchain_account.eth_private_key
        
        # Generate a transaction ID
        import uuid
        transaction_id = str(uuid.uuid4())
        
        # Submit the transaction to the multisig wallet
        tx_hash = submit_multisig_transaction(
            from_address=from_address,
            to_address=destination,
            amount_in_eth=amount,
            data=tx_data,
            private_key=private_key,
            transaction_id=transaction_id
        )
        
        if tx_hash:
            # Save the transaction in the database
            blockchain_tx = BlockchainTransaction(
                user_id=current_user.id,
                from_address=from_address,
                to_address=destination,
                eth_tx_hash=tx_hash,
                amount=amount,
                contract_address=get_multisig_wallet().address,
                transaction_type='MULTISIG_SUBMIT',
                status='pending',
                tx_metadata=f"Data: {tx_data}"
            )
            db.session.add(blockchain_tx)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'tx_hash': tx_hash,
                'transaction_id': transaction_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to submit transaction to MultiSig wallet'
            }), 500
    except Exception as e:
        logger.error(f"Error submitting multisig transaction: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@blockchain_api.route('/multisig/transaction/<tx_id>', methods=['GET'])
@login_required
def get_multisig_transaction(tx_id):
    """Get details for a multisig transaction"""
    try:
        # This would involve calling the contract to get transaction details
        # For now, we'll return a mock response
        multisig_wallet = get_multisig_wallet()
        
        if not multisig_wallet:
            return jsonify({
                'success': False,
                'message': 'MultiSig wallet is not deployed'
            }), 400
        
        # In a real implementation:
        # tx = multisig_wallet.functions.transactions(tx_id).call()
        # confirmations = [
        #     multisig_wallet.functions.getOwner(i).call()
        #     for i in range(multisig_wallet.functions.getConfirmationCount(tx_id).call())
        # ]
        
        # Mock data
        tx = {
            'id': tx_id,
            'destination': '0x1234567890123456789012345678901234567890',
            'value': 1.0,
            'data': '0x',
            'executed': False,
            'confirmations': 1,
            'confirmedBy': ['0xabcdef1234567890abcdef1234567890abcdef12']
        }
        
        return jsonify({
            'success': True,
            'transaction': tx,
            'required_confirmations': 2
        })
    except Exception as e:
        logger.error(f"Error getting multisig transaction {tx_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@blockchain_api.route('/multisig/confirm/<tx_id>', methods=['POST'])
@login_required
def confirm_multisig_tx(tx_id):
    """Confirm a multisig transaction"""
    try:
        # Get the user's ethereum address
        from flask_login import current_user
        blockchain_account = BlockchainAccount.query.filter_by(user_id=current_user.id).first()
        
        if not blockchain_account:
            return jsonify({
                'success': False,
                'message': 'You do not have an associated Ethereum account'
            }), 400
        
        from_address = blockchain_account.eth_address
        private_key = blockchain_account.eth_private_key
        
        # Generate a transaction ID for our records
        import uuid
        internal_tx_id = str(uuid.uuid4())
        
        # Confirm the transaction
        tx_hash = confirm_multisig_transaction(
            transaction_id=internal_tx_id,
            from_address=from_address,
            private_key=private_key,
            multisig_tx_id=int(tx_id)
        )
        
        if tx_hash:
            # Save the transaction in the database
            blockchain_tx = BlockchainTransaction(
                user_id=current_user.id,
                from_address=from_address,
                to_address=get_multisig_wallet().address,
                eth_tx_hash=tx_hash,
                amount=0,  # No ETH is transferred for confirmations
                contract_address=get_multisig_wallet().address,
                transaction_type='MULTISIG_CONFIRM',
                status='pending',
                tx_metadata=f"Confirmed transaction {tx_id}"
            )
            db.session.add(blockchain_tx)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'tx_hash': tx_hash
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to confirm transaction'
            }), 500
    except Exception as e:
        logger.error(f"Error confirming multisig transaction {tx_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@blockchain_api.route('/multisig/execute/<tx_id>', methods=['POST'])
@login_required
def execute_multisig_tx(tx_id):
    """Execute a multisig transaction that has enough confirmations"""
    try:
        # Get the user's ethereum address
        from flask_login import current_user
        blockchain_account = BlockchainAccount.query.filter_by(user_id=current_user.id).first()
        
        if not blockchain_account:
            return jsonify({
                'success': False,
                'message': 'You do not have an associated Ethereum account'
            }), 400
        
        from_address = blockchain_account.eth_address
        private_key = blockchain_account.eth_private_key
        
        # This would involve calling the contract to execute the transaction
        # For now, we'll return a mock response
        
        # In a real implementation:
        # tx_hash = multisig_wallet.functions.executeTransaction(tx_id).transact({
        #     'from': from_address
        # })
        
        # Mock data
        tx_hash = '0xfedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210'
        
        # Save the transaction in the database
        blockchain_tx = BlockchainTransaction(
            user_id=current_user.id,
            from_address=from_address,
            to_address=get_multisig_wallet().address,
            eth_tx_hash=tx_hash,
            amount=0,  # The execution itself doesn't transfer ETH
            contract_address=get_multisig_wallet().address,
            transaction_type='MULTISIG_EXECUTE',
            status='pending',
            tx_metadata=f"Executed transaction {tx_id}"
        )
        db.session.add(blockchain_tx)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'tx_hash': tx_hash
        })
    except Exception as e:
        logger.error(f"Error executing multisig transaction {tx_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@blockchain_api.route('/token/transfer', methods=['POST'])
@login_required
def transfer_tokens():
    """Transfer NVC tokens from the user's account to another address"""
    try:
        data = request.get_json()
        
        to_address = data.get('to_address')
        amount = float(data.get('amount'))
        
        # Get the user's ethereum address
        from flask_login import current_user
        blockchain_account = BlockchainAccount.query.filter_by(user_id=current_user.id).first()
        
        if not blockchain_account:
            return jsonify({
                'success': False,
                'message': 'You do not have an associated Ethereum account'
            }), 400
        
        from_address = blockchain_account.eth_address
        private_key = blockchain_account.eth_private_key
        
        # Generate a transaction ID
        import uuid
        transaction_id = str(uuid.uuid4())
        
        # Transfer the tokens
        tx_hash = transfer_nvc_tokens(
            from_address=from_address,
            to_address=to_address,
            amount=amount,
            private_key=private_key,
            transaction_id=transaction_id
        )
        
        if tx_hash:
            # Save the transaction in the database
            blockchain_tx = BlockchainTransaction(
                user_id=current_user.id,
                from_address=from_address,
                to_address=to_address,
                eth_tx_hash=tx_hash,
                amount=amount,
                contract_address=get_nvc_token().address,
                transaction_type='TOKEN_TRANSFER',
                status='pending'
            )
            db.session.add(blockchain_tx)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'tx_hash': tx_hash
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to transfer tokens'
            }), 500
    except Exception as e:
        logger.error(f"Error transferring tokens: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@blockchain_api.route('/token/mint', methods=['POST'])
@admin_required
def mint_tokens():
    """Mint new NVC tokens (admin only)"""
    try:
        data = request.get_json()
        
        to_address = data.get('to_address')
        amount = float(data.get('amount'))
        
        # This would involve calling the contract to mint tokens
        # For now, we'll return a mock response
        token_contract = get_nvc_token()
        
        if not token_contract:
            return jsonify({
                'success': False,
                'message': 'NVC Token contract is not deployed'
            }), 400
        
        # In a real implementation:
        # tx_hash = token_contract.functions.mint(to_address, amount).transact()
        
        # Mock data
        tx_hash = '0x1122334455667788991122334455667788991122334455667788991122334455'
        
        return jsonify({
            'success': True,
            'tx_hash': tx_hash
        })
    except Exception as e:
        logger.error(f"Error minting tokens: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@blockchain_api.route('/token/burn', methods=['POST'])
@admin_required
def burn_tokens():
    """Burn existing NVC tokens (admin only)"""
    try:
        data = request.get_json()
        
        from_address = data.get('from_address')
        amount = float(data.get('amount'))
        
        # This would involve calling the contract to burn tokens
        # For now, we'll return a mock response
        token_contract = get_nvc_token()
        
        if not token_contract:
            return jsonify({
                'success': False,
                'message': 'NVC Token contract is not deployed'
            }), 400
        
        # In a real implementation:
        # tx_hash = token_contract.functions.burn(from_address, amount).transact()
        
        # Mock data
        tx_hash = '0x5544332211998877665544332211998877665544332211998877665544332211'
        
        return jsonify({
            'success': True,
            'tx_hash': tx_hash
        })
    except Exception as e:
        logger.error(f"Error burning tokens: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@blockchain_api.route('/token/balance/<address>', methods=['GET'])
@login_required
def token_balance(address):
    """Get the NVC token balance for an address"""
    try:
        token_contract = get_nvc_token()
        
        if not token_contract:
            return jsonify({
                'success': False,
                'message': 'NVC Token contract is not deployed'
            }), 400
        
        balance = get_nvc_token_balance(address)
        
        return jsonify({
            'success': True,
            'address': address,
            'balance': balance
        })
    except Exception as e:
        logger.error(f"Error getting token balance for {address}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500