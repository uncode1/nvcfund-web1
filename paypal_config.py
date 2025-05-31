"""
PayPal API Credentials Configuration
Secure interface for configuring PayPal API credentials
"""

import os
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required
from wtforms import Form, StringField, validators
import paypalrestsdk

# Create blueprint
paypal_config_bp = Blueprint('paypal_config', __name__, url_prefix='/paypal-config')

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

@paypal_config_bp.route('/', methods=['GET', 'POST'])
@login_required
def configure_credentials():
    """Configure PayPal API credentials"""
    form = PayPalCredentialsForm(request.form)
    
    # Check if credentials already exist
    current_client_id = os.environ.get('PAYPAL_CLIENT_ID', '')
    current_has_credentials = bool(current_client_id and os.environ.get('PAYPAL_CLIENT_SECRET'))
    
    if request.method == 'POST' and form.validate():
        try:
            # Test the credentials by attempting to get an access token
            paypalrestsdk.configure({
                "mode": "live",
                "client_id": form.client_id.data,
                "client_secret": form.client_secret.data
            })
            
            # Test connection
            access_token = paypalrestsdk.api.get_access_token()
            
            if access_token:
                # Store credentials securely
                os.environ['PAYPAL_CLIENT_ID'] = form.client_id.data
                os.environ['PAYPAL_CLIENT_SECRET'] = form.client_secret.data
                
                # Test balance retrieval
                from gateway_balance_checker import GatewayBalanceChecker
                checker = GatewayBalanceChecker()
                balance_result = checker.check_paypal_balance()
                
                if balance_result.get('success'):
                    flash(f'PayPal credentials verified successfully! USD Balance: ${balance_result.get("total_usd", 0):,.2f}', 'success')
                    return redirect(url_for('nvct_treasury.dashboard'))
                else:
                    flash('PayPal credentials verified, but could not retrieve balance information. Please check account permissions.', 'warning')
                    return redirect(url_for('nvct_treasury.dashboard'))
            else:
                flash('Invalid PayPal credentials - could not authenticate', 'error')
                
        except Exception as e:
            flash(f'Error validating PayPal credentials: {str(e)}', 'error')
    
    return render_template('paypal_credentials.html', 
                         form=form, 
                         current_has_credentials=current_has_credentials,
                         masked_client_id=current_client_id[:8] + '...' if current_client_id else '')

@paypal_config_bp.route('/test-connection')
@login_required  
def test_connection():
    """Test existing PayPal credentials"""
    try:
        from gateway_balance_checker import GatewayBalanceChecker
        checker = GatewayBalanceChecker()
        result = checker.check_paypal_balance()
        
        if result.get('success'):
            flash(f'PayPal connection successful! USD Balance: ${result.get("total_usd", 0):,.2f}', 'success')
        else:
            flash(f'PayPal connection failed: {result.get("message", "Unknown error")}', 'error')
            
    except Exception as e:
        flash(f'Error testing PayPal connection: {str(e)}', 'error')
    
    return redirect(url_for('paypal_config.configure_credentials'))