"""
ISO 20022 Routes for NVC Banking Platform
Handles ISO 20022 message processing and financial messaging standards
"""

from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
import logging
from datetime import datetime
import xml.etree.ElementTree as ET
from decimal import Decimal
import uuid
import json

from iso20022_integration import (
    iso20022_service, 
    ISO20022MessageType,
    create_iso20022_payment_message,
    process_iso20022_message
)
# Import decorators if available, otherwise create a simple decorator
try:
    from decorators import require_role
except ImportError:
    def require_role(roles):
        def decorator(func):
            return func
        return decorator
from models import db

logger = logging.getLogger(__name__)

iso20022_bp = Blueprint('iso20022', __name__, url_prefix='/iso20022')

@iso20022_bp.route('/dashboard')
@login_required
@require_role(['ADMIN', 'OPERATOR'])
def dashboard():
    """ISO 20022 messaging dashboard"""
    try:
        return render_template('iso20022/dashboard.html', 
                             title="ISO 20022 Financial Messaging")
    except Exception as e:
        logger.error(f"Error loading ISO 20022 dashboard: {str(e)}")
        flash('Error loading dashboard', 'error')
        return redirect(url_for('web.main.index'))

@iso20022_bp.route('/payment-status', methods=['GET', 'POST'])
@login_required
@require_role(['ADMIN', 'OPERATOR'])
def payment_status():
    """Generate payment status reports"""
    if request.method == 'POST':
        try:
            # Get payment status data
            payment_id = request.form.get('payment_id')
            status = request.form.get('status', 'ACCP')  # ACCP = Accepted
            
            # Generate payment status report XML
            status_xml = iso20022_service.generate_payment_status_report(payment_id, status)
            
            return render_template('iso20022/payment_status_created.html',
                                 xml_message=status_xml,
                                 payment_id=payment_id,
                                 status=status)
        except Exception as e:
            logger.error(f"Error creating payment status report: {str(e)}")
            flash(f'Error creating status report: {str(e)}', 'error')
    
    return render_template('iso20022/create_payment_status.html')

@iso20022_bp.route('/account-statement', methods=['GET', 'POST'])
@login_required
@require_role(['ADMIN', 'OPERATOR'])
def account_statement():
    """Generate account statements"""
    if request.method == 'POST':
        try:
            # Get account statement data
            account_number = request.form.get('account_number')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            
            # Generate account statement XML
            statement_xml = iso20022_service.generate_account_statement(
                account_number, start_date, end_date
            )
            
            return render_template('iso20022/account_statement_created.html',
                                 xml_message=statement_xml,
                                 account_number=account_number,
                                 start_date=start_date,
                                 end_date=end_date)
        except Exception as e:
            logger.error(f"Error creating account statement: {str(e)}")
            flash(f'Error creating statement: {str(e)}', 'error')
    
    return render_template('iso20022/create_account_statement.html')

@iso20022_bp.route('/direct-debit', methods=['GET', 'POST'])
@login_required
@require_role(['ADMIN', 'OPERATOR'])
def direct_debit():
    """Generate direct debit initiation"""
    if request.method == 'POST':
        try:
            # Get direct debit data
            debit_data = {
                'debtor_name': request.form.get('debtor_name', ''),
                'debtor_iban': request.form.get('debtor_iban', ''),
                'amount': request.form.get('amount', '0.00'),
                'currency': request.form.get('currency', 'USD'),
                'collection_date': request.form.get('collection_date', ''),
                'end_to_end_id': request.form.get('end_to_end_id', '')
            }
            
            # Generate direct debit XML
            debit_xml = iso20022_service.generate_direct_debit_initiation(debit_data)
            
            return render_template('iso20022/direct_debit_created.html',
                                 xml_message=debit_xml,
                                 debit_data=debit_data)
        except Exception as e:
            logger.error(f"Error creating direct debit: {str(e)}")
            flash(f'Error creating direct debit: {str(e)}', 'error')
    
    return render_template('iso20022/create_direct_debit.html')

@iso20022_bp.route('/debit-credit-notification', methods=['GET', 'POST'])
@login_required
@require_role(['ADMIN', 'OPERATOR'])
def debit_credit_notification():
    """Generate debit credit notification"""
    if request.method == 'POST':
        try:
            # Get notification data
            notification_data = {
                'account_iban': request.form.get('account_iban', ''),
                'amount': request.form.get('amount', '0.00'),
                'currency': request.form.get('currency', 'USD'),
                'credit_debit_indicator': request.form.get('credit_debit_indicator', 'CRDT'),
                'transaction_reference': request.form.get('transaction_reference', '')
            }
            
            # Generate notification XML
            notification_xml = iso20022_service.generate_debit_credit_notification(notification_data)
            
            return render_template('iso20022/notification_created.html',
                                 xml_message=notification_xml,
                                 notification_data=notification_data)
        except Exception as e:
            logger.error(f"Error creating notification: {str(e)}")
            flash(f'Error creating notification: {str(e)}', 'error')
    
    return render_template('iso20022/create_notification.html')

@iso20022_bp.route('/create-payment', methods=['GET', 'POST'])
@login_required
@require_role(['ADMIN', 'OPERATOR'])
def create_payment():
    """Create ISO 20022 payment message"""
    if request.method == 'GET':
        return render_template('iso20022/create_payment.html',
                             title="Create ISO 20022 Payment")
    
    try:
        # Extract payment data from form
        payment_data = {
            'creditor_name': request.form.get('creditor_name'),
            'creditor_account': request.form.get('creditor_account'),
            'creditor_iban': request.form.get('creditor_iban'),
            'creditor_bank_bic': request.form.get('creditor_bank_bic'),
            'creditor_country': request.form.get('creditor_country'),
            'amount': request.form.get('amount'),
            'currency': request.form.get('currency', 'USD'),
            'remittance_info': request.form.get('remittance_info'),
            'purpose_code': request.form.get('purpose_code'),
            'instruction_id': f"NVC{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8]}",
            'end_to_end_id': f"E2E{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8]}"
        }
        
        # Validate required fields
        required_fields = ['creditor_name', 'amount']
        for field in required_fields:
            if not payment_data.get(field):
                flash(f'Missing required field: {field}', 'error')
                return render_template('iso20022/create_payment.html',
                                     title="Create ISO 20022 Payment")
        
        # Generate ISO 20022 message
        xml_message = create_iso20022_payment_message(payment_data)
        
        # Store message for tracking (you may want to add a database model for this)
        logger.info(f"Created ISO 20022 payment: {payment_data['instruction_id']}")
        
        flash('ISO 20022 payment message created successfully!', 'success')
        return render_template('iso20022/payment_created.html',
                             xml_message=xml_message,
                             payment_data=payment_data,
                             title="Payment Message Created")
        
    except Exception as e:
        logger.error(f"Error creating ISO 20022 payment: {str(e)}")
        flash(f'Error creating payment: {str(e)}', 'error')
        return render_template('iso20022/create_payment.html',
                             title="Create ISO 20022 Payment")

@iso20022_bp.route('/process-message', methods=['GET', 'POST'])
@login_required
@require_role(['ADMIN', 'OPERATOR'])
def process_message():
    """Process incoming ISO 20022 message"""
    if request.method == 'GET':
        return render_template('iso20022/process_message.html',
                             title="Process ISO 20022 Message")
    
    try:
        xml_content = request.form.get('xml_content')
        if not xml_content:
            flash('Please provide XML content to process', 'error')
            return render_template('iso20022/process_message.html',
                                 title="Process ISO 20022 Message")
        
        # Process the message
        result = process_iso20022_message(xml_content)
        
        if 'error' in result:
            flash(f'Error processing message: {result["error"]}', 'error')
            return render_template('iso20022/process_message.html',
                                 title="Process ISO 20022 Message")
        
        logger.info(f"Processed ISO 20022 message: {result.get('message_id', 'unknown')}")
        flash('Message processed successfully!', 'success')
        
        return render_template('iso20022/message_processed.html',
                             result=result,
                             title="Message Processed")
        
    except Exception as e:
        logger.error(f"Error processing ISO 20022 message: {str(e)}")
        flash(f'Error processing message: {str(e)}', 'error')
        return render_template('iso20022/process_message.html',
                             title="Process ISO 20022 Message")

@iso20022_bp.route('/generate-statement')
@login_required
@require_role(['ADMIN', 'OPERATOR'])
def generate_statement():
    """Generate ISO 20022 account statement"""
    try:
        account_number = request.args.get('account_number', 'GL89NVCT0000000000000001')
        
        # Sample transactions (in a real implementation, fetch from database)
        transactions = [
            {
                'amount': '1000.00',
                'currency': 'USD',
                'type': 'CRDT',
                'date': '2024-01-15',
                'value_date': '2024-01-15',
                'end_to_end_id': 'E2E20240115001',
                'remittance_info': 'Customer deposit'
            },
            {
                'amount': '250.00',
                'currency': 'USD',
                'type': 'DBIT',
                'date': '2024-01-16',
                'value_date': '2024-01-16',
                'end_to_end_id': 'E2E20240116001',
                'remittance_info': 'Transfer to external account'
            }
        ]
        
        xml_statement = iso20022_service.generate_account_statement_iso20022(
            account_number, transactions
        )
        
        return render_template('iso20022/statement_generated.html',
                             xml_statement=xml_statement,
                             account_number=account_number,
                             title="ISO 20022 Statement Generated")
        
    except Exception as e:
        logger.error(f"Error generating ISO 20022 statement: {str(e)}")
        flash(f'Error generating statement: {str(e)}', 'error')
        return redirect(url_for('iso20022.dashboard'))

@iso20022_bp.route('/validate-message', methods=['POST'])
@login_required
@require_role(['ADMIN', 'OPERATOR'])
def validate_message():
    """Validate ISO 20022 message format"""
    try:
        xml_content = request.form.get('xml_content')
        message_type = request.form.get('message_type', 'pain.001.001.03')
        
        if not xml_content:
            return jsonify({'error': 'No XML content provided'}), 400
        
        # Map string to enum
        type_mapping = {
            'pain.001.001.03': ISO20022MessageType.PAIN_001,
            'pain.002.001.03': ISO20022MessageType.PAIN_002,
            'camt.053.001.02': ISO20022MessageType.CAMT_053
        }
        
        msg_type_enum = type_mapping.get(message_type)
        if not msg_type_enum:
            return jsonify({'error': 'Unsupported message type'}), 400
        
        validation_result = iso20022_service.validator.validate_message_structure(
            xml_content, msg_type_enum
        )
        
        return jsonify(validation_result)
        
    except Exception as e:
        logger.error(f"Error validating ISO 20022 message: {str(e)}")
        return jsonify({'error': str(e)}), 500

@iso20022_bp.route('/api/send-payment', methods=['POST'])
@login_required
@require_role(['ADMIN', 'API'])
def api_send_payment():
    """API endpoint to send ISO 20022 payment"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Generate payment message
        xml_message = create_iso20022_payment_message(data)
        
        # In a real implementation, you would send this to the payment network
        # For now, we'll just return the generated message
        
        result = {
            'status': 'success',
            'instruction_id': data.get('instruction_id'),
            'message_id': f"NVC{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'xml_message': xml_message,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"API payment sent: {result['instruction_id']}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in API payment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@iso20022_bp.route('/api/receive-message', methods=['POST'])
def api_receive_message():
    """API endpoint to receive ISO 20022 messages from external systems"""
    try:
        # This endpoint would typically be called by external payment networks
        xml_content = request.data.decode('utf-8')
        
        if not xml_content:
            return jsonify({'error': 'No XML content provided'}), 400
        
        # Process the incoming message
        result = process_iso20022_message(xml_content)
        
        if 'error' in result:
            logger.error(f"Error processing incoming message: {result['error']}")
            return jsonify({'status': 'error', 'message': result['error']}), 400
        
        # Store the processed message (implement database storage as needed)
        logger.info(f"Received ISO 20022 message: {result.get('message_id', 'unknown')}")
        
        return jsonify({
            'status': 'success',
            'message': 'Message processed successfully',
            'message_id': result.get('message_id'),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error receiving ISO 20022 message: {str(e)}")
        return jsonify({'error': str(e)}), 500

@iso20022_bp.route('/message-types')
@login_required
def message_types():
    """Display supported ISO 20022 message types"""
    message_types = {
        'Payment Initiation': {
            'pain.001.001.03': 'CustomerCreditTransferInitiation',
            'pain.002.001.03': 'PaymentStatusReport',
            'pain.007.001.02': 'CustomerPaymentReversal',
            'pain.008.001.02': 'CustomerDirectDebitInitiation'
        },
        'Account Management': {
            'acmt.001.001.05': 'AccountOpeningInstruction',
            'acmt.002.001.05': 'AccountDetailsConfirmation',
            'acmt.003.001.05': 'AccountModificationInstruction',
            'acmt.005.001.05': 'RequestForAccountManagementStatusReport'
        },
        'Cash Management': {
            'camt.052.001.02': 'BankToCustomerAccountReport',
            'camt.053.001.02': 'BankToCustomerStatement',
            'camt.054.001.02': 'BankToCustomerDebitCreditNotification',
            'camt.056.001.01': 'FIToFIPaymentCancellationRequest'
        },
        'Trade Services': {
            'tsmt.009.001.03': 'StatusChangeRequestNotification',
            'tsmt.010.001.03': 'StatusChangeRequestAcceptance'
        },
        'Securities': {
            'semt.002.001.02': 'CustodyStatementOfHoldings',
            'semt.003.001.02': 'AccountingStatementOfHoldings'
        }
    }
    
    return render_template('iso20022/message_types.html',
                         message_types=message_types,
                         title="ISO 20022 Message Types")

def register_iso20022_routes(app):
    """Register ISO 20022 routes with the Flask app"""
    app.register_blueprint(iso20022_bp)
    logger.info("ISO 20022 routes registered successfully")