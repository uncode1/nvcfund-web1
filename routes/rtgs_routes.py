"""
Real-Time Gross Settlement (RTGS) Routes
Routes for handling RTGS transfers between central banks and financial institutions
Includes functionality for canceling and editing pending RTGS transfers
"""

import os
import uuid
import datetime
import json
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc

from app import db
from auth import admin_required
from models import Transaction, TransactionStatus, TransactionType, User, FinancialInstitution, FinancialInstitutionType
from utils import get_transaction_metadata, generate_transaction_id, get_institution_metadata
from blockchain_utils import generate_ethereum_account

# Create the blueprint
rtgs_routes = Blueprint('rtgs', __name__, url_prefix='/rtgs')

@rtgs_routes.route('/dashboard')
@login_required
def dashboard():
    """RTGS Transfer Dashboard"""
    # Get recent transactions and process their metadata
    transactions = Transaction.query.filter_by(
        transaction_type=TransactionType.RTGS_TRANSFER
    ).order_by(desc(Transaction.created_at)).limit(20).all()
    
    # Process transaction metadata for each transaction
    processed_transactions = []
    for tx in transactions:
        tx_data = {
            'transaction': tx,
            'metadata': get_transaction_metadata(tx)
        }
        processed_transactions.append(tx_data)
    
    # Count transactions by status
    total_count = Transaction.query.filter_by(
        transaction_type=TransactionType.RTGS_TRANSFER
    ).count()
    
    completed_count = Transaction.query.filter_by(
        transaction_type=TransactionType.RTGS_TRANSFER,
        status=TransactionStatus.COMPLETED
    ).count()
    
    pending_count = Transaction.query.filter_by(
        transaction_type=TransactionType.RTGS_TRANSFER,
        status=TransactionStatus.PENDING
    ).count()
    
    failed_count = Transaction.query.filter_by(
        transaction_type=TransactionType.RTGS_TRANSFER,
        status=TransactionStatus.FAILED
    ).count()
    
    # Get central banks and other RTGS-enabled institutions
    institutions = FinancialInstitution.query.filter_by(rtgs_enabled=True).all()
    
    # Process institution metadata for each institution to get country info
    from utils import get_institution_metadata
    
    # Create a list of institutions with their metadata
    processed_institutions = []
    for institution in institutions:
        metadata = get_institution_metadata(institution)
        institution_data = {
            'institution': institution,
            'metadata': metadata,
            'country': metadata.get('country', 'N/A')  # Get country from metadata
        }
        processed_institutions.append(institution_data)
    
    return render_template('rtgs/dashboard.html',
                          transactions=processed_transactions,
                          total_count=total_count,
                          completed_count=completed_count,
                          pending_count=pending_count,
                          failed_count=failed_count,
                          institutions=processed_institutions)

@rtgs_routes.route('/new_transfer', methods=['GET', 'POST'])
@login_required
def new_transfer():
    """Create a new RTGS transfer"""
    if request.method == 'POST':
        try:
            # Get form data
            institution_id = request.form.get('institution_id')
            amount = float(request.form.get('amount', 0))
            currency = request.form.get('currency', 'USD')
            beneficiary_account = request.form.get('beneficiary_account', '')
            beneficiary_name = request.form.get('beneficiary_name', '')
            beneficiary_bank = request.form.get('beneficiary_bank', '')
            purpose_code = request.form.get('purpose_code', '')
            description = request.form.get('description', '')
            
            # Validate data
            if not institution_id:
                flash('Please select a central bank or financial institution', 'danger')
                return redirect(url_for('rtgs.new_transfer'))
            
            if amount <= 0:
                flash('Amount must be greater than zero', 'danger')
                return redirect(url_for('rtgs.new_transfer'))
            
            if not beneficiary_account or not beneficiary_name or not beneficiary_bank:
                flash('Beneficiary name, bank name, and account number are required', 'danger')
                return redirect(url_for('rtgs.new_transfer'))
            
            # Get institution
            institution = FinancialInstitution.query.get(institution_id)
            if not institution:
                flash('Institution not found', 'danger')
                return redirect(url_for('rtgs.new_transfer'))
            
            if not institution.rtgs_enabled:
                flash('This institution does not support RTGS transfers', 'danger')
                return redirect(url_for('rtgs.new_transfer'))
            
            # Create transaction record
            metadata = {
                'institution_id': institution.id,
                'purpose_code': purpose_code,
                'initiated_at': datetime.datetime.utcnow().isoformat(),
                'rtgs_transfer_id': str(uuid.uuid4()),
                'settlement_type': 'RTGS',
                'priority': 'HIGH',
                'beneficiary_name': beneficiary_name,
                'beneficiary_bank': beneficiary_bank,
                'beneficiary_account': beneficiary_account,
                'recipient_bank_name': beneficiary_bank,  # Use beneficiary's bank name
                'recipient_processing_institution': institution.name,  # The RTGS institution
                'recipient_bank_swift': institution.swift_code or 'Unknown'
            }
            
            transaction = Transaction(
                transaction_id=generate_transaction_id(),
                user_id=current_user.id,
                transaction_type=TransactionType.RTGS_TRANSFER,
                amount=amount,
                currency=currency,
                status=TransactionStatus.PENDING,
                description=description or f"RTGS transfer to {beneficiary_name}",
                institution_id=institution.id,
                # Store recipient details in dedicated fields
                recipient_name=beneficiary_name,
                recipient_institution=institution.name,  # The RTGS/clearing institution
                recipient_account=beneficiary_account,
                recipient_bank=beneficiary_bank,  # Store the actual bank name where the account is held
                tx_metadata_json=json.dumps(metadata)
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            flash(f'RTGS transfer initiated. Transaction ID: {transaction.transaction_id}', 'success')
            return redirect(url_for('rtgs.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating RTGS transfer: {str(e)}")
            flash(f'Error creating transfer: {str(e)}', 'danger')
            return redirect(url_for('rtgs.new_transfer'))
    
    # GET request - show form
    institutions = FinancialInstitution.query.filter_by(rtgs_enabled=True).all()
    purpose_codes = [
        ('CORT', 'Corporate Transfer'),
        ('INTC', 'Intra-Company Payment'),
        ('TREA', 'Treasury Transfer'),
        ('CASH', 'Cash Management Transfer'),
        ('DIVI', 'Dividend Payment'),
        ('GOVT', 'Government Payment'),
        ('PENS', 'Pension Payment'),
        ('SALA', 'Salary Payment'),
        ('TAXS', 'Tax Payment'),
        ('TRAD', 'Trade Payment'),
    ]
    return render_template('rtgs/new_transfer.html',
                          institutions=institutions,
                          purpose_codes=purpose_codes)

@rtgs_routes.route('/api/transfer', methods=['POST'])
@login_required
@admin_required
def api_transfer():
    """API endpoint for RTGS transfers"""
    try:
        data = request.json
        
        # Validate request
        required_fields = ['institution_id', 'amount', 'currency', 'beneficiary_account', 'beneficiary_name', 'beneficiary_bank']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Get institution
        institution = FinancialInstitution.query.get(data['institution_id'])
        if not institution:
            return jsonify({'success': False, 'error': 'Institution not found'}), 404
        
        if not institution.rtgs_enabled:
            return jsonify({'success': False, 'error': 'This institution does not support RTGS transfers'}), 400
        
        # Create transaction
        # Create metadata
        metadata = {
            'institution_id': institution.id,
            'purpose_code': data.get('purpose_code', ''),
            'initiated_at': datetime.datetime.utcnow().isoformat(),
            'rtgs_transfer_id': str(uuid.uuid4()),
            'settlement_type': 'RTGS',
            'priority': data.get('priority', 'HIGH'),
            'api_initiated': True,
            'beneficiary_name': data['beneficiary_name'],
            'beneficiary_bank': data['beneficiary_bank'],
            'beneficiary_account': data['beneficiary_account'],
            'recipient_bank_name': data['beneficiary_bank'],  # Use beneficiary's bank name
            'recipient_processing_institution': institution.name,  # The RTGS institution
            'recipient_bank_swift': institution.swift_code or 'Unknown'
        }
        
        transaction = Transaction(
            transaction_id=generate_transaction_id(),
            user_id=current_user.id,
            transaction_type=TransactionType.RTGS_TRANSFER,
            amount=float(data['amount']),
            currency=data['currency'],
            status=TransactionStatus.PENDING,
            description=data.get('description') or f"RTGS transfer to {data['beneficiary_name']}",
            institution_id=institution.id,
            # Store recipient details in dedicated fields
            recipient_name=data['beneficiary_name'],
            recipient_institution=institution.name,  # The RTGS/clearing institution
            recipient_account=data['beneficiary_account'],
            recipient_bank=data['beneficiary_bank'],  # Store the actual bank name where the account is held
            recipient_country=get_institution_metadata(institution).get('country', ''),
            tx_metadata_json=json.dumps(metadata)
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'transaction_id': transaction.transaction_id,
            'status': transaction.status.value,
            'message': 'RTGS transfer initiated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in RTGS API transfer: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@rtgs_routes.route('/cancel/<transaction_id>', methods=['GET', 'POST'])
@login_required
def cancel_transfer(transaction_id):
    """Cancel a pending RTGS transfer"""
    # Find the transaction
    transaction = Transaction.query.filter_by(
        transaction_id=transaction_id,
        transaction_type=TransactionType.RTGS_TRANSFER
    ).first_or_404()
    
    # Check permissions
    if transaction.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to cancel this transaction.', 'danger')
        return redirect(url_for('rtgs.dashboard'))
    
    # Check if transaction can be canceled
    if transaction.status != TransactionStatus.PENDING:
        flash('Only pending transactions can be canceled.', 'danger')
        return redirect(url_for('web.main.transaction_details', transaction_id=transaction_id))
    
    if request.method == 'POST':
        # Confirm the cancellation
        if request.form.get('confirm_cancel') == 'yes':
            transaction.status = TransactionStatus.CANCELLED
            
            # Add cancellation info to metadata
            metadata = get_transaction_metadata(transaction)
            metadata['canceled_at'] = datetime.datetime.utcnow().isoformat()
            metadata['canceled_by'] = current_user.username
            metadata['cancellation_reason'] = request.form.get('reason', 'User requested cancellation')
            transaction.tx_metadata_json = json.dumps(metadata)
            
            db.session.commit()
            
            flash('RTGS transfer has been successfully canceled.', 'success')
            return redirect(url_for('rtgs.dashboard'))
    
    # Show confirmation form
    return render_template('rtgs/cancel_transfer.html', transaction=transaction)

@rtgs_routes.route('/edit/<transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transfer(transaction_id):
    """Edit a pending RTGS transfer"""
    # Find the transaction
    transaction = Transaction.query.filter_by(
        transaction_id=transaction_id,
        transaction_type=TransactionType.RTGS_TRANSFER
    ).first_or_404()
    
    # Check permissions
    if transaction.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to edit this transaction.', 'danger')
        return redirect(url_for('rtgs.dashboard'))
    
    # Check if transaction can be edited
    if transaction.status != TransactionStatus.PENDING:
        flash('Only pending transactions can be edited.', 'danger')
        return redirect(url_for('web.main.transaction_details', transaction_id=transaction_id))
    
    # Get the current metadata
    metadata = get_transaction_metadata(transaction)
    
    if request.method == 'POST':
        try:
            # Get form data
            beneficiary_account = request.form.get('beneficiary_account', '')
            beneficiary_name = request.form.get('beneficiary_name', '')
            beneficiary_bank = request.form.get('beneficiary_bank', '')
            purpose_code = request.form.get('purpose_code', '')
            description = request.form.get('description', '')
            
            # Validate data
            if not beneficiary_account or not beneficiary_name or not beneficiary_bank:
                flash('Beneficiary name, bank name, and account number are required', 'danger')
                return redirect(url_for('rtgs.edit_transfer', transaction_id=transaction_id))
            
            # Update transaction and metadata
            transaction.recipient_account = beneficiary_account
            transaction.recipient_name = beneficiary_name
            transaction.recipient_bank = beneficiary_bank
            transaction.description = description
            
            # Update metadata
            metadata['beneficiary_account'] = beneficiary_account
            metadata['beneficiary_name'] = beneficiary_name
            metadata['beneficiary_bank'] = beneficiary_bank
            metadata['recipient_bank_name'] = beneficiary_bank
            metadata['purpose_code'] = purpose_code
            metadata['last_edited_at'] = datetime.datetime.utcnow().isoformat()
            metadata['edited_by'] = current_user.username
            
            transaction.tx_metadata_json = json.dumps(metadata)
            
            db.session.commit()
            
            flash('RTGS transfer has been successfully updated.', 'success')
            return redirect(url_for('web.main.transaction_details', transaction_id=transaction_id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating RTGS transfer: {str(e)}")
            flash(f'Error updating transfer: {str(e)}', 'danger')
    
    # Prepare form data
    purpose_codes = [
        ('CORT', 'Corporate Transfer'),
        ('INTC', 'Intra-Company Payment'),
        ('TREA', 'Treasury Transfer'),
        ('CASH', 'Cash Management Transfer'),
        ('DIVI', 'Dividend Payment'),
        ('GOVT', 'Government Payment'),
        ('PENS', 'Pension Payment'),
        ('SALA', 'Salary Payment'),
        ('TAXS', 'Tax Payment'),
        ('TRAD', 'Trade Payment'),
    ]
    
    # Show edit form
    return render_template('rtgs/edit_transfer.html', 
                          transaction=transaction, 
                          metadata=metadata,
                          purpose_codes=purpose_codes)

@rtgs_routes.route('/api/status/<transaction_id>', methods=['GET'])
@login_required
@admin_required
def check_status(transaction_id):
    """Check the status of an RTGS transfer"""
    try:
        transaction = Transaction.query.filter_by(
            transaction_id=transaction_id,
            transaction_type=TransactionType.RTGS_TRANSFER
        ).first()
        
        if not transaction:
            return jsonify({'success': False, 'error': 'Transaction not found'}), 404
        
        # Check if user has permission to view this transaction
        if transaction.user_id != current_user.id and not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        # Get recipient info from metadata
        metadata = get_transaction_metadata(transaction)
        
        # Format response json
        response_data = {
            'success': True,
            'transaction_id': transaction.transaction_id,
            'status': transaction.status.value,
            'initiated_at': transaction.created_at.isoformat(),
            'updated_at': transaction.updated_at.isoformat() if hasattr(transaction, 'updated_at') else None,
            'amount': transaction.amount,
            'currency': transaction.currency,
            'recipient_name': metadata.get('beneficiary_name', ''),
            'recipient_account': metadata.get('beneficiary_account', ''),
            'recipient_bank_name': metadata.get('recipient_bank_name', ''),
            'metadata': metadata
        }
        
        # Check if HTML format is requested
        format_param = request.args.get('format', 'json')
        if format_param == 'html':
            # Render the enhanced viewer template with the transaction data
            return render_template(
                'rtgs/api_viewer.html',
                transaction=transaction,
                metadata=metadata,
                json_data=json.dumps(response_data, indent=2)
            )
        elif format_param == 'pdf':
            # Generate PDF of the API response
            from weasyprint import HTML
            import tempfile
            
            # Create HTML content for the PDF
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>RTGS Transaction {transaction.transaction_id}</title>
                <style>
                    @page {{ size: letter portrait; margin: 1cm; }}
                    body {{ font-family: 'Helvetica', 'Arial', sans-serif; padding: 15px; font-size: 10px; }}
                    h1 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 5px; font-size: 16px; margin-top: 0; }}
                    h2 {{ color: #3498db; margin-top: 10px; font-size: 14px; }}
                    .transaction-info {{ margin-bottom: 10px; }}
                    .json-data {{ 
                        font-family: 'Courier New', 'Consolas', monospace; 
                        background-color: #f8f9fa;
                        padding: 8px;
                        border-radius: 4px;
                        white-space: pre-wrap;
                        font-size: 9px;
                        line-height: 1.2;
                    }}
                    .badge {{
                        display: inline-block;
                        padding: 2px 5px;
                        border-radius: 3px;
                        font-weight: bold;
                        color: white;
                        font-size: 9px;
                    }}
                    .badge-PENDING {{ background-color: #ffc107; color: #212529; }}
                    .badge-COMPLETED {{ background-color: #28a745; }}
                    .badge-FAILED {{ background-color: #dc3545; }}
                    .badge-CANCELLED {{ background-color: #6c757d; }}
                    .field-label {{ font-weight: bold; min-width: 120px; display: inline-block; }}
                    .field-value {{ display: inline-block; }}
                    .status-field {{ margin-bottom: 5px; }}
                    .footer {{ 
                        margin-top: 15px;
                        font-size: 8px;
                        color: #6c757d;
                        text-align: center;
                        border-top: 1px solid #eee;
                        padding-top: 5px;
                    }}
                </style>
            </head>
            <body>
                <h1>RTGS Transaction Details</h1>
                
                <div class="transaction-info">
                    <div class="status-field">
                        <span class="field-label">Status:</span>
                        <span class="badge badge-{transaction.status.value}">{transaction.status.value}</span>
                    </div>
                    <div>
                        <span class="field-label">Transaction ID:</span>
                        <span class="field-value">{transaction.transaction_id}</span>
                    </div>
                    <div>
                        <span class="field-label">Created:</span>
                        <span class="field-value">{transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')}</span>
                    </div>
                    <div>
                        <span class="field-label">Amount:</span>
                        <span class="field-value">{transaction.amount:,.2f} {transaction.currency}</span>
                    </div>
                    <div>
                        <span class="field-label">Recipient:</span>
                        <span class="field-value">{metadata.get('beneficiary_name', 'N/A')}</span>
                    </div>
                    <div>
                        <span class="field-label">Recipient Bank:</span>
                        <span class="field-value">{metadata.get('recipient_bank_name', 'N/A')}</span>
                    </div>
                    <div>
                        <span class="field-label">Account Number:</span>
                        <span class="field-value">{metadata.get('beneficiary_account', 'N/A')}</span>
                    </div>
                </div>
                
                <h2>Complete API Response</h2>
                <pre class="json-data">{json.dumps(response_data, indent=2)}</pre>
                
                <div class="footer">
                    <p>Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | NVC Global RTGS System</p>
                    <p>Page 1</p>
                </div>
            </body>
            </html>
            """
            
            # Create PDF
            pdf_file = tempfile.NamedTemporaryFile(suffix='.pdf')
            HTML(string=html_content).write_pdf(pdf_file.name)
            
            # Return the PDF as a response
            with open(pdf_file.name, 'rb') as f:
                binary_pdf = f.read()
            
            response = current_app.response_class(
                binary_pdf,
                mimetype='application/pdf',
                headers={'Content-Disposition': f'attachment; filename=rtgs-transaction-{transaction.transaction_id}.pdf'}
            )
            return response
        
        # Default: Return JSON response
        return jsonify(response_data)
        
    except Exception as e:
        current_app.logger.error(f"Error checking RTGS transfer status: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
        
@rtgs_routes.route('/add_institution', methods=['POST'])
@login_required
@admin_required
def add_institution():
    """Add a new RTGS-enabled financial institution"""
    try:
        name = request.form.get('name')
        institution_type_str = request.form.get('institution_type')
        swift_code = request.form.get('swift_code')
        country = request.form.get('country')
        api_endpoint = request.form.get('api_endpoint')
        s2s_enabled = request.form.get('s2s_enabled') == 'on'
        
        # Validate inputs
        if not name:
            flash('Institution name is required', 'danger')
            return redirect(url_for('rtgs.dashboard'))
        
        if not institution_type_str:
            flash('Institution type is required', 'danger')
            return redirect(url_for('rtgs.dashboard'))
            
        # Convert institution type string to enum
        try:
            institution_type = FinancialInstitutionType(institution_type_str.lower())
        except ValueError:
            flash(f'Invalid institution type: {institution_type_str}', 'danger')
            return redirect(url_for('rtgs.dashboard'))
        
        # Generate Ethereum address for the institution
        eth_address, _ = generate_ethereum_account()
        
        if not eth_address:
            flash('Failed to generate Ethereum address', 'danger')
            return redirect(url_for('rtgs.dashboard'))
        
        # Prepare metadata with country information and other details
        metadata = {}
        if country:
            metadata["country"] = country
            
        # Get RTGS system information
        rtgs_system = request.form.get('rtgs_system', '')
        if rtgs_system:
            metadata["rtgs_system"] = rtgs_system
        
        # Add timestamp
        metadata["added_at"] = datetime.datetime.utcnow().isoformat()
        
        # Add SWIFT info if available
        if swift_code:
            if "swift" not in metadata:
                metadata["swift"] = {}
            metadata["swift"]["bic"] = swift_code
        
        # Create new institution with RTGS enabled
        institution = FinancialInstitution(
            name=name,
            institution_type=institution_type,
            api_endpoint=api_endpoint,
            ethereum_address=eth_address,
            swift_code=swift_code if swift_code else None,
            rtgs_enabled=True,  # Always enable RTGS
            s2s_enabled=s2s_enabled,
            is_active=True,
            metadata_json=json.dumps(metadata) if metadata else None
        )
        
        db.session.add(institution)
        db.session.commit()
        
        flash(f'RTGS-enabled institution "{name}" added successfully', 'success')
        return redirect(url_for('rtgs.dashboard'))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error adding RTGS institution: {str(e)}")
        flash(f'Error adding institution: {str(e)}', 'danger')
        return redirect(url_for('rtgs.dashboard'))