"""
Payment Gateway Balance Checker
Verifies actual fiat balances in Stripe, PayPal, and Flutterwave accounts
"""

import os
import stripe
import requests
from datetime import datetime
import paypalrestsdk
from flask import current_app

class GatewayBalanceChecker:
    """Check real fiat balances across payment gateways"""
    
    def __init__(self):
        self.stripe_key = os.environ.get('STRIPE_SECRET_KEY')
        self.paypal_client_id = os.environ.get('PAYPAL_CLIENT_ID')
        self.paypal_client_secret = os.environ.get('PAYPAL_CLIENT_SECRET')
        self.flutterwave_secret = os.environ.get('FLUTTERWAVE_SECRET_KEY')
        
    def check_stripe_balance(self):
        """Check Stripe account balance"""
        try:
            stripe.api_key = self.stripe_key
            balance = stripe.Balance.retrieve()
            
            balances = {}
            for currency_balance in balance['available']:
                currency = currency_balance['currency'].upper()
                amount = currency_balance['amount'] / 100  # Convert from cents
                balances[currency] = amount
                
            return {
                'success': True,
                'balances': balances,
                'total_usd': balances.get('USD', 0),
                'last_checked': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Could not retrieve Stripe balance'
            }
    
    def check_paypal_balance(self):
        """Check PayPal account balance"""
        try:
            # Configure PayPal SDK
            paypalrestsdk.configure({
                "mode": "live",  # Change to "sandbox" for testing
                "client_id": self.paypal_client_id,
                "client_secret": self.paypal_client_secret
            })
            
            # Get access token
            access_token = paypalrestsdk.api.get_access_token()
            
            # Make API call to get balance
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            
            response = requests.get(
                'https://api.paypal.com/v1/reporting/balances',
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                balances = {}
                total_usd = 0
                
                for balance in data.get('balances', []):
                    currency = balance['currency']
                    amount = float(balance['total_balance']['value'])
                    balances[currency] = amount
                    if currency == 'USD':
                        total_usd = amount
                
                return {
                    'success': True,
                    'balances': balances,
                    'total_usd': total_usd,
                    'last_checked': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}',
                    'message': 'Could not retrieve PayPal balance'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Could not retrieve PayPal balance'
            }
    
    def check_flutterwave_balance(self):
        """Check Flutterwave account balance"""
        try:
            headers = {
                'Authorization': f'Bearer {self.flutterwave_secret}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                'https://api.flutterwave.com/v3/balances',
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                balances = {}
                total_usd = 0
                
                for balance in data.get('data', []):
                    currency = balance['currency']
                    amount = float(balance['available_balance'])
                    balances[currency] = amount
                    if currency == 'USD':
                        total_usd = amount
                
                return {
                    'success': True,
                    'balances': balances,
                    'total_usd': total_usd,
                    'last_checked': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}',
                    'message': 'Could not retrieve Flutterwave balance'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Could not retrieve Flutterwave balance'
            }
    
    def check_all_gateway_balances(self):
        """Check balances across all payment gateways"""
        results = {
            'stripe': self.check_stripe_balance(),
            'paypal': self.check_paypal_balance(),
            'flutterwave': self.check_flutterwave_balance(),
            'summary': {
                'total_usd_across_gateways': 0,
                'gateways_checked': 0,
                'successful_checks': 0
            }
        }
        
        # Calculate summary
        for gateway, result in results.items():
            if gateway != 'summary':
                results['summary']['gateways_checked'] += 1
                if result.get('success'):
                    results['summary']['successful_checks'] += 1
                    results['summary']['total_usd_across_gateways'] += result.get('total_usd', 0)
        
        return results

def check_gateway_fiat_balances():
    """Main function to check all gateway balances"""
    checker = GatewayBalanceChecker()
    return checker.check_all_gateway_balances()

if __name__ == "__main__":
    # Test the balance checker
    results = check_gateway_fiat_balances()
    print("Gateway Balance Check Results:")
    print("=" * 50)
    
    for gateway, result in results.items():
        if gateway != 'summary':
            print(f"\n{gateway.upper()}:")
            if result.get('success'):
                print(f"  Status: ✓ Connected")
                print(f"  USD Balance: ${result.get('total_usd', 0):,.2f}")
                for currency, amount in result.get('balances', {}).items():
                    print(f"  {currency}: {amount:,.2f}")
            else:
                print(f"  Status: ✗ Error")
                print(f"  Message: {result.get('message', 'Unknown error')}")
    
    print(f"\nSUMMARY:")
    summary = results['summary']
    print(f"  Total USD across all gateways: ${summary['total_usd_across_gateways']:,.2f}")
    print(f"  Successful connections: {summary['successful_checks']}/{summary['gateways_checked']}")