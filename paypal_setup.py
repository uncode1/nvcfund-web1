"""
Simple PayPal API Setup Interface
Direct access to configure PayPal credentials without authentication
"""

import os
from flask import Blueprint, request, render_template_string, flash, redirect, url_for
from wtforms import Form, StringField, validators
import paypalrestsdk

# Create blueprint
paypal_setup_bp = Blueprint('paypal_setup', __name__, url_prefix='/paypal-setup')

class PayPalSetupForm(Form):
    """Form for PayPal API credentials input"""
    client_id = StringField('PayPal Client ID', [
        validators.DataRequired(message="Client ID is required"),
        validators.Length(min=10, message="Client ID must be at least 10 characters")
    ])
    client_secret = StringField('PayPal Client Secret', [
        validators.DataRequired(message="Client Secret is required"),
        validators.Length(min=10, message="Client Secret must be at least 10 characters")
    ])

SETUP_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PayPal API Setup</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card shadow">
                    <div class="card-header bg-primary text-white">
                        <h4 class="mb-0">
                            <i class="fab fa-paypal me-2"></i>
                            PayPal API Configuration
                        </h4>
                    </div>
                    
                    <div class="card-body">
                        {% with messages = get_flashed_messages(with_categories=true) %}
                            {% if messages %}
                                {% for category, message in messages %}
                                    <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                                        {{ message }}
                                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                    </div>
                                {% endfor %}
                            {% endif %}
                        {% endwith %}

                        <div class="alert alert-info">
                            <h6><i class="fas fa-info-circle"></i> Instructions</h6>
                            <p class="mb-2">Enter your PayPal Live API credentials to enable balance checking and payment processing.</p>
                            <p class="mb-0">Get these from your <a href="https://developer.paypal.com" target="_blank" class="alert-link">PayPal Developer Dashboard</a> under your Live app settings.</p>
                        </div>

                        <form method="POST" action="{{ url_for('paypal_setup.setup_credentials') }}">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="client_id" class="form-label">
                                            <i class="fas fa-key"></i> PayPal Client ID
                                        </label>
                                        {{ form.client_id(class="form-control", placeholder="Enter Client ID") }}
                                        {% if form.client_id.errors %}
                                            <div class="text-danger small mt-1">
                                                {% for error in form.client_id.errors %}
                                                    <div>{{ error }}</div>
                                                {% endfor %}
                                            </div>
                                        {% endif %}
                                    </div>
                                </div>
                                
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="client_secret" class="form-label">
                                            <i class="fas fa-lock"></i> PayPal Client Secret
                                        </label>
                                        {{ form.client_secret(class="form-control", placeholder="Enter Client Secret", type="password") }}
                                        {% if form.client_secret.errors %}
                                            <div class="text-danger small mt-1">
                                                {% for error in form.client_secret.errors %}
                                                    <div>{{ error }}</div>
                                                {% endfor %}
                                            </div>
                                        {% endif %}
                                    </div>
                                </div>
                            </div>

                            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="fas fa-save"></i> Configure PayPal
                                </button>
                            </div>
                        </form>

                        <hr class="my-4">
                        
                        <div class="row">
                            <div class="col-md-6">
                                <h6><i class="fas fa-question-circle"></i> How to Get Credentials</h6>
                                <ol class="small">
                                    <li>Go to <a href="https://developer.paypal.com" target="_blank">developer.paypal.com</a></li>
                                    <li>Log in with your PayPal business account</li>
                                    <li>Create or select your application</li>
                                    <li>Switch to "Live" mode (not Sandbox)</li>
                                    <li>Copy the Client ID and Client Secret</li>
                                </ol>
                            </div>
                            
                            <div class="col-md-6">
                                <h6><i class="fas fa-shield-alt"></i> Current Status</h6>
                                <p class="small">
                                    Client ID: <code>{{ current_client_id if current_client_id else 'Not configured' }}</code><br>
                                    Status: <span class="badge bg-{{ 'success' if has_credentials else 'warning' }}">
                                        {{ 'Configured' if has_credentials else 'Not configured' }}
                                    </span>
                                </p>
                                {% if has_credentials %}
                                    <a href="{{ url_for('paypal_setup.test_credentials') }}" class="btn btn-sm btn-outline-primary">
                                        <i class="fas fa-wifi"></i> Test Connection
                                    </a>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@paypal_setup_bp.route('/', methods=['GET', 'POST'])
def setup_credentials():
    """Setup PayPal API credentials"""
    form = PayPalSetupForm(request.form)
    
    # Check current credentials
    current_client_id = os.environ.get('PAYPAL_CLIENT_ID', '')
    has_credentials = bool(current_client_id and os.environ.get('PAYPAL_CLIENT_SECRET'))
    
    if request.method == 'POST' and form.validate():
        try:
            # Test the credentials
            paypalrestsdk.configure({
                "mode": "live",
                "client_id": form.client_id.data,
                "client_secret": form.client_secret.data
            })
            
            # Try to get an access token
            import paypalrestsdk.api
            access_token = paypalrestsdk.api.get_access_token()
            
            if access_token:
                # Store credentials
                os.environ['PAYPAL_CLIENT_ID'] = form.client_id.data
                os.environ['PAYPAL_CLIENT_SECRET'] = form.client_secret.data
                
                # Test balance retrieval
                from gateway_balance_checker import GatewayBalanceChecker
                checker = GatewayBalanceChecker()
                balance_result = checker.check_paypal_balance()
                
                if balance_result.get('success'):
                    flash(f'PayPal credentials configured successfully! USD Balance: ${balance_result.get("total_usd", 0):,.2f}', 'success')
                else:
                    flash('PayPal credentials saved, but balance check requires additional permissions', 'warning')
                    
                # Redirect to refresh the page with new status
                return redirect(url_for('paypal_setup.setup_credentials'))
            else:
                flash('Invalid PayPal credentials - authentication failed', 'error')
                
        except Exception as e:
            flash(f'Error configuring PayPal: {str(e)}', 'error')
    
    return render_template_string(SETUP_TEMPLATE, 
                                form=form, 
                                current_client_id=current_client_id[:12] + '...' if current_client_id else '',
                                has_credentials=has_credentials)

@paypal_setup_bp.route('/test')
def test_credentials():
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
        flash(f'Error testing PayPal: {str(e)}', 'error')
    
    return redirect(url_for('paypal_setup.setup_credentials'))