"""
Flutterwave Payment Routes for NVC Banking Platform

This module provides Flask routes for Flutterwave payment processing,
including payment links, webhooks, transfers, and virtual accounts.
"""

import json
import uuid
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.exceptions import BadRequest

from flutterwave_integration import flutterwave_service
from models import Transaction, User, PaymentGateway, db
from decorators import admin_required

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprints
flutterwave_bp = Blueprint('flutterwave', __name__, url_prefix='/api/flutterwave')
flutterwave_web_bp = Blueprint('flutterwave_web', __name__, url_prefix='/flutterwave')

@flutterwave_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Flutterwave integration"""
    try:
        return jsonify({
            'status': 'ok',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'Flutterwave Payment Integration',
            'version': '1.0.0'
        }), 200
    except Exception as e:
        logger.error(f"Flutterwave health check failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@flutterwave_bp.route('/create-payment', methods=['POST'])
@login_required
def create_payment():
    """Create a payment link through Flutterwave"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No request data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['amount', 'currency', 'customer']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Generate transaction reference
        tx_ref = f"NVC-{uuid.uuid4()}"
        data['tx_ref'] = tx_ref
        
        # Add redirect URLs
        base_url = request.host_url.rstrip('/')
        data['redirect_url'] = f"{base_url}/flutterwave/payment-callback/{tx_ref}"
        
        # Create payment link
        result = flutterwave_service.create_payment_link(data)
        
        if result.get('status') == 'success':
            # Save initial transaction record
            flutterwave_service.save_transaction_to_database(result, current_user.id)
            
            return jsonify({
                'status': 'success',
                'message': 'Payment link created successfully',
                'data': {
                    'link': result['data']['link'],
                    'tx_ref': tx_ref,
                    'payment_id': result['data']['id']
                }
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': result.get('message', 'Failed to create payment link')
            }), 400
    
    except Exception as e:
        logger.error(f"Error creating Flutterwave payment: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to create payment: {str(e)}'
        }), 500

@flutterwave_bp.route('/verify-payment/<transaction_id>', methods=['GET'])
@login_required
def verify_payment(transaction_id):
    """Verify a payment transaction"""
    try:
        result = flutterwave_service.verify_payment(transaction_id)
        
        if result.get('status') == 'success':
            # Update transaction in database
            transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
            if transaction:
                data = result.get('data', {})
                transaction.status = flutterwave_service._map_flutterwave_status(data.get('status', 'pending'))
                transaction.gateway_response = json.dumps(result)
                transaction.updated_at = datetime.utcnow()
                db.session.commit()
            
            return jsonify({
                'status': 'success',
                'data': result['data']
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': result.get('message', 'Payment verification failed')
            }), 400
    
    except Exception as e:
        logger.error(f"Error verifying Flutterwave payment: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to verify payment: {str(e)}'
        }), 500

@flutterwave_bp.route('/create-virtual-account', methods=['POST'])
@login_required
def create_virtual_account():
    """Create a virtual account for collecting payments"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No request data provided'
            }), 400
        
        # Add user information if not provided
        if 'email' not in data:
            data['email'] = current_user.email
        
        result = flutterwave_service.create_virtual_account(data)
        
        return jsonify({
            'status': 'success' if result.get('status') == 'success' else 'error',
            'data': result.get('data', {}),
            'message': result.get('message', '')
        }), 201 if result.get('status') == 'success' else 400
    
    except Exception as e:
        logger.error(f"Error creating virtual account: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to create virtual account: {str(e)}'
        }), 500

@flutterwave_bp.route('/initiate-transfer', methods=['POST'])
@login_required
def initiate_transfer():
    """Initiate a transfer to bank account"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No request data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['account_bank', 'account_number', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }), 400
        
        result = flutterwave_service.initiate_transfer(data)
        
        return jsonify({
            'status': 'success' if result.get('status') == 'success' else 'error',
            'data': result.get('data', {}),
            'message': result.get('message', '')
        }), 201 if result.get('status') == 'success' else 400
    
    except Exception as e:
        logger.error(f"Error initiating transfer: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to initiate transfer: {str(e)}'
        }), 500

@flutterwave_bp.route('/banks/<country>', methods=['GET'])
@login_required
def get_banks(country):
    """Get list of banks for a country"""
    try:
        result = flutterwave_service.get_banks(country)
        
        return jsonify({
            'status': 'success' if result.get('status') == 'success' else 'error',
            'data': result.get('data', []),
            'message': result.get('message', '')
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting banks: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to get banks: {str(e)}'
        }), 500

@flutterwave_bp.route('/verify-account', methods=['POST'])
@login_required
def verify_account():
    """Verify bank account details"""
    try:
        data = request.get_json()
        if not data or 'account_number' not in data or 'account_bank' not in data:
            return jsonify({
                'status': 'error',
                'message': 'account_number and account_bank are required'
            }), 400
        
        result = flutterwave_service.verify_bank_account(
            data['account_number'], 
            data['account_bank']
        )
        
        return jsonify({
            'status': 'success' if result.get('status') == 'success' else 'error',
            'data': result.get('data', {}),
            'message': result.get('message', '')
        }), 200
    
    except Exception as e:
        logger.error(f"Error verifying account: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to verify account: {str(e)}'
        }), 500

@flutterwave_bp.route('/webhook', methods=['POST'])
def webhook():
    """Handle Flutterwave webhooks"""
    try:
        # Get the signature from headers
        signature = request.headers.get('verif-hash')
        
        # Get raw payload
        payload = request.get_data(as_text=True)
        
        # Verify signature if provided
        if signature:
            if not flutterwave_service.verify_webhook_signature(payload, signature):
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid signature'
                }), 401
        
        # Parse webhook data
        webhook_data = request.get_json()
        
        # Process the webhook
        result = flutterwave_service.process_webhook_payment(webhook_data)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error processing Flutterwave webhook: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Web interface routes
@flutterwave_web_bp.route('/')
@login_required
def dashboard():
    """Flutterwave payment dashboard"""
    try:
        # Get recent Flutterwave transactions
        flutterwave_gateway = PaymentGateway.query.filter_by(name='Flutterwave').first()
        
        if flutterwave_gateway:
            transactions = Transaction.query.filter_by(
                payment_gateway_id=flutterwave_gateway.id
            ).order_by(
                Transaction.created_at.desc()
            ).limit(10).all()
        else:
            transactions = []
        
        return render_template('flutterwave/dashboard.html', transactions=transactions)
    
    except Exception as e:
        logger.error(f"Error rendering Flutterwave dashboard: {str(e)}")
        flash('Error loading dashboard', 'error')
        return redirect(url_for('dashboard_bp.dashboard'))

@flutterwave_web_bp.route('/payment-callback/<tx_ref>')
def payment_callback(tx_ref):
    """Handle payment callback from Flutterwave"""
    try:
        # Verify the payment
        result = flutterwave_service.verify_payment(tx_ref)
        
        if result.get('status') == 'success':
            data = result.get('data', {})
            status = data.get('status', '').lower()
            
            if status == 'successful':
                flash('Payment completed successfully!', 'success')
                return render_template('flutterwave/payment_success.html', 
                                     transaction=data, tx_ref=tx_ref)
            elif status == 'failed':
                flash('Payment failed. Please try again.', 'error')
                return render_template('flutterwave/payment_failed.html', 
                                     transaction=data, tx_ref=tx_ref)
            else:
                flash('Payment is being processed.', 'info')
                return render_template('flutterwave/payment_pending.html', 
                                     transaction=data, tx_ref=tx_ref)
        else:
            flash('Unable to verify payment status.', 'warning')
            return redirect(url_for('flutterwave_web.dashboard'))
    
    except Exception as e:
        logger.error(f"Error in payment callback: {str(e)}")
        flash('Error processing payment callback', 'error')
        return redirect(url_for('flutterwave_web.dashboard'))

@flutterwave_web_bp.route('/create-payment', methods=['GET', 'POST'])
@login_required
def create_payment_form():
    """Web form for creating payments"""
    if request.method == 'POST':
        try:
            data = {
                'amount': float(request.form['amount']),
                'currency': request.form['currency'],
                'customer': {
                    'email': request.form['customer_email'],
                    'name': request.form['customer_name'],
                    'phone': request.form.get('customer_phone', '')
                },
                'description': request.form.get('description', ''),
                'title': 'NVC Banking Platform Payment'
            }
            
            # Generate transaction reference
            tx_ref = f"NVC-{uuid.uuid4()}"
            data['tx_ref'] = tx_ref
            
            # Add redirect URLs
            base_url = request.host_url.rstrip('/')
            data['redirect_url'] = f"{base_url}/flutterwave/payment-callback/{tx_ref}"
            
            # Create payment link
            result = flutterwave_service.create_payment_link(data)
            
            if result.get('status') == 'success':
                # Save transaction
                flutterwave_service.save_transaction_to_database(result, current_user.id)
                
                # Redirect to payment page
                return redirect(result['data']['link'])
            else:
                flash(f"Error creating payment: {result.get('message', 'Unknown error')}", 'error')
        
        except Exception as e:
            logger.error(f"Error in create payment form: {str(e)}")
            flash(f'Error creating payment: {str(e)}', 'error')
    
    return render_template('flutterwave/create_payment.html')

# Admin routes
@flutterwave_bp.route('/admin/transactions', methods=['GET'])
@login_required
@admin_required
def admin_transactions():
    """Get all Flutterwave transactions (admin only)"""
    try:
        transactions = Transaction.query.join(
            Transaction.payment_gateway
        ).filter(
            Transaction.payment_gateway.has(name='Flutterwave')
        ).order_by(
            Transaction.created_at.desc()
        ).limit(100).all()
        
        result = []
        for tx in transactions:
            result.append({
                'transaction_id': tx.transaction_id,
                'external_id': tx.external_id,
                'amount': float(tx.amount),
                'currency': tx.currency,
                'status': tx.status,
                'created_at': tx.created_at.isoformat() if tx.created_at else None,
                'updated_at': tx.updated_at.isoformat() if tx.updated_at else None
            })
        
        return jsonify({
            'status': 'success',
            'count': len(result),
            'data': result
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting admin transactions: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to get transactions: {str(e)}'
        }), 500