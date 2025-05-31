"""
Treasury Operations for NVCT Token Management
This module handles direct token minting and treasury operations for the NVCT issuer
"""
import logging
from datetime import datetime
from decimal import Decimal
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from models import db, Transaction, TransactionStatus, TransactionType
from account_holder_models import BankAccount, CurrencyType, AccountHolder, AccountType
from forms import TreasuryMintForm, GatewayFundingForm
from wtforms import Form, StringField, validators
from utils import generate_transaction_id

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
treasury_bp = Blueprint('nvct_treasury', __name__, url_prefix='/nvct-treasury')

class PayPalCredentialsForm(Form):
    """Form for PayPal API credentials input"""
    client_id = StringField('PayPal Client ID', [
        validators.DataRequired(message="Client ID is required"),
        validators.Length(min=10, message="Client ID must be at least 10 characters")
    ])
    client_secret = StringField('PayPal Client Secret', [
        validators.DataRequired(message="Client Secret is required"),
        validators.Length(min=10, message="Client Secret must be at least 10 characters")
    ])

class TreasuryOperations:
    """Treasury operations for NVCT token management"""
    
    @staticmethod
    def mint_nvct_tokens(account_id, amount, purpose="Treasury Operation", authorized_by=None):
        """
        Mint NVCT tokens directly to an account
        
        Args:
            account_id: Target account ID to receive tokens
            amount: Amount of NVCT tokens to mint
            purpose: Purpose of the minting operation
            authorized_by: User ID who authorized the operation
            
        Returns:
            Transaction object if successful, None otherwise
        """
        try:
            # Get target account
            target_account = BankAccount.query.get(account_id)
            if not target_account:
                logger.error(f"Account {account_id} not found")
                return None
                
            if target_account.currency != CurrencyType.NVCT:
                logger.error(f"Account {account_id} is not an NVCT account")
                return None
            
            # Create treasury minting transaction
            transaction = Transaction(
                transaction_id=generate_transaction_id(),
                transaction_type=TransactionType.TRANSFER,
                status=TransactionStatus.COMPLETED,
                amount=Decimal(str(amount)),
                currency='NVCT',
                sender_account_id=None,  # Treasury mint has no sender
                recipient_account_id=account_id,
                description=f"Treasury Mint: {purpose}",
                reference_number=f"MINT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                authorized_by=authorized_by or "Treasury System"
            )
            
            # Update account balance
            target_account.balance += Decimal(str(amount))
            target_account.available_balance += Decimal(str(amount))
            
            # Save to database
            db.session.add(transaction)
            db.session.commit()
            
            logger.info(f"Minted {amount} NVCT tokens to account {account_id}")
            return transaction
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error minting NVCT tokens: {str(e)}")
            return None
    
    @staticmethod
    def create_gateway_reserve_account(gateway_name, initial_funding=0):
        """
        Create a reserve account for a payment gateway
        
        Args:
            gateway_name: Name of the payment gateway (Stripe, PayPal, Flutterwave)
            initial_funding: Initial NVCT funding amount
            
        Returns:
            BankAccount object if successful, None otherwise
        """
        try:
            # Create account holder for gateway
            gateway_holder = AccountHolder(
                entity_name=f"{gateway_name} Gateway Reserve",
                entity_type="Payment Gateway",
                contact_email=f"{gateway_name.lower()}@nvcfund.com",
                phone_number="N/A",
                address="Treasury Operations",
                city="Global",
                country="GL",
                is_institution=True,
                is_correspondent_bank=False,
                account_status="ACTIVE"
            )
            
            db.session.add(gateway_holder)
            db.session.flush()  # Get the ID
            
            # Create NVCT reserve account
            reserve_account = BankAccount(
                account_holder_id=gateway_holder.id,
                account_number=f"GATE-{gateway_name.upper()}-{datetime.now().strftime('%Y%m%d')}",
                account_name=f"{gateway_name} Gateway Reserve Account",
                account_type=AccountType.INSTITUTIONAL,
                currency=CurrencyType.NVCT,
                balance=0.0,
                available_balance=0.0,
                status=AccountStatus.ACTIVE
            )
            
            db.session.add(reserve_account)
            db.session.commit()
            
            # Provide initial funding if specified
            if initial_funding > 0:
                TreasuryOperations.mint_nvct_tokens(
                    reserve_account.id,
                    initial_funding,
                    f"Initial funding for {gateway_name} gateway",
                    "Treasury System"
                )
            
            logger.info(f"Created {gateway_name} gateway reserve account with {initial_funding} NVCT")
            return reserve_account
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating gateway reserve account: {str(e)}")
            return None
    
    @staticmethod
    def fund_gateway_account(gateway_account_id, amount, purpose="Gateway Funding"):
        """
        Fund a gateway reserve account with NVCT tokens
        
        Args:
            gateway_account_id: Gateway account ID to fund
            amount: Amount of NVCT tokens to add
            purpose: Purpose of the funding
            
        Returns:
            Transaction object if successful, None otherwise
        """
        return TreasuryOperations.mint_nvct_tokens(
            gateway_account_id,
            amount,
            purpose,
            "Treasury System"
        )

@treasury_bp.route('/dashboard')
@login_required
def dashboard():
    """Treasury operations dashboard"""
    
    # Get treasury statistics
    total_nvct_supply = db.session.query(db.func.sum(BankAccount.balance)).filter(
        BankAccount.currency == CurrencyType.NVCT
    ).scalar() or Decimal('0')
    
    # Get gateway accounts
    gateway_accounts = BankAccount.query.filter(
        BankAccount.account_name.like('%Gateway%'),
        BankAccount.currency == CurrencyType.NVCT
    ).all()
    
    mint_form = TreasuryMintForm()
    funding_form = GatewayFundingForm()
    
    return render_template('treasury/dashboard.html',
                         total_supply=total_nvct_supply,
                         gateway_accounts=gateway_accounts,
                         mint_form=mint_form,
                         funding_form=funding_form)

@treasury_bp.route('/mint-tokens', methods=['POST'])
@login_required
def mint_tokens():
    """Mint NVCT tokens to an account"""
    form = TreasuryMintForm()
    
    if form.validate_on_submit():
        result = TreasuryOperations.mint_nvct_tokens(
            form.account_id.data,
            form.amount.data,
            form.purpose.data,
            current_user.id
        )
        
        if result:
            flash(f"Successfully minted {form.amount.data} NVCT tokens", "success")
        else:
            flash("Error minting tokens", "danger")
    else:
        flash("Invalid form data", "danger")
    
    return redirect(url_for('treasury.dashboard'))

@treasury_bp.route('/create-gateway-account', methods=['POST'])
@login_required
def create_gateway_account():
    """Create a new gateway reserve account"""
    gateway_name = request.form.get('gateway_name')
    initial_funding = float(request.form.get('initial_funding', 0))
    
    if not gateway_name:
        flash("Gateway name is required", "danger")
        return redirect(url_for('nvct_treasury.dashboard'))
    
    result = TreasuryOperations.create_gateway_reserve_account(
        gateway_name,
        initial_funding
    )
    
    if result:
        flash(f"Created {gateway_name} gateway account with {initial_funding} NVCT", "success")
    else:
        flash("Error creating gateway account", "danger")
    
    return redirect(url_for('treasury.dashboard'))

@treasury_bp.route('/fund-gateway', methods=['POST'])
@login_required
def fund_gateway():
    """Fund a gateway account with NVCT tokens"""
    form = GatewayFundingForm()
    
    if form.validate_on_submit():
        result = TreasuryOperations.fund_gateway_account(
            form.gateway_account_id.data,
            form.amount.data,
            form.purpose.data
        )
        
        if result:
            flash(f"Successfully funded gateway with {form.amount.data} NVCT", "success")
        else:
            flash("Error funding gateway account", "danger")
    else:
        flash("Invalid form data", "danger")
    
    return redirect(url_for('treasury.dashboard'))