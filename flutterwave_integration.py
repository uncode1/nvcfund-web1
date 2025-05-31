"""
Flutterwave Payment Integration for NVC Banking Platform

This module provides comprehensive Flutterwave payment processing capabilities
including card payments, mobile money, bank transfers, and virtual accounts.
"""

import os
import uuid
import hashlib
import hmac
import json
import logging
import requests
from datetime import datetime
from typing import Dict, Any, Optional, List
from decimal import Decimal

from app import db
from models import Transaction, PaymentGateway, User, TransactionStatus

# Configure logging
logger = logging.getLogger(__name__)

class FlutterwaveService:
    """Service for processing payments through Flutterwave API"""
    
    def __init__(self):
        """Initialize Flutterwave service with API credentials"""
        self.secret_key = os.environ.get('FLUTTERWAVE_SECRET_KEY')
        self.public_key = os.environ.get('FLUTTERWAVE_PUBLIC_KEY')
        self.encryption_key = os.environ.get('FLUTTERWAVE_ENCRYPTION_KEY')
        self.base_url = "https://api.flutterwave.com/v3"
        
        if not all([self.secret_key, self.public_key]):
            logger.warning("Flutterwave API credentials not configured")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Flutterwave API requests"""
        return {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Make authenticated request to Flutterwave API"""
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=data)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Flutterwave API request failed: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response content: {e.response.text}")
            raise
    
    def create_payment_link(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a payment link for card and other payment methods
        
        Args:
            payment_data: Payment details including amount, currency, customer info
            
        Returns:
            Payment link response with checkout URL
        """
        tx_ref = payment_data.get('tx_ref', f"NVC-{uuid.uuid4()}")
        
        payload = {
            "tx_ref": tx_ref,
            "amount": str(payment_data['amount']),
            "currency": payment_data.get('currency', 'USD'),
            "redirect_url": payment_data.get('redirect_url'),
            "payment_options": payment_data.get('payment_options', 'card,mobilemoney,banktransfer'),
            "customer": {
                "email": payment_data['customer']['email'],
                "phonenumber": payment_data['customer'].get('phone', ''),
                "name": payment_data['customer']['name']
            },
            "customizations": {
                "title": payment_data.get('title', 'NVC Banking Platform'),
                "description": payment_data.get('description', 'Payment processing'),
                "logo": payment_data.get('logo', '')
            },
            "meta": payment_data.get('meta', {})
        }
        
        response = self._make_request('POST', 'payments', payload)
        return response
    
    def verify_payment(self, transaction_id: str) -> Dict[str, Any]:
        """
        Verify a payment transaction
        
        Args:
            transaction_id: Flutterwave transaction ID or tx_ref
            
        Returns:
            Payment verification details
        """
        try:
            # Try verifying by transaction ID first
            response = self._make_request('GET', f'transactions/{transaction_id}/verify')
            return response
        except:
            # If that fails, try by tx_ref
            response = self._make_request('GET', f'transactions/verify_by_reference', {'tx_ref': transaction_id})
            return response
    
    def create_virtual_account(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a virtual account for collecting payments
        
        Args:
            account_data: Account creation details
            
        Returns:
            Virtual account details
        """
        payload = {
            "email": account_data['email'],
            "is_permanent": account_data.get('is_permanent', True),
            "bvn": account_data.get('bvn', ''),
            "tx_ref": account_data.get('tx_ref', f"VA-{uuid.uuid4()}"),
            "phonenumber": account_data.get('phone', ''),
            "firstname": account_data.get('firstname', ''),
            "lastname": account_data.get('lastname', ''),
            "narration": account_data.get('narration', 'NVC Banking Virtual Account')
        }
        
        response = self._make_request('POST', 'virtual-account-numbers', payload)
        return response
    
    def initiate_transfer(self, transfer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initiate a transfer to bank account or mobile money
        
        Args:
            transfer_data: Transfer details
            
        Returns:
            Transfer response
        """
        payload = {
            "account_bank": transfer_data['account_bank'],
            "account_number": transfer_data['account_number'],
            "amount": transfer_data['amount'],
            "narration": transfer_data.get('narration', 'NVC Banking Transfer'),
            "currency": transfer_data.get('currency', 'NGN'),
            "reference": transfer_data.get('reference', f"TRANSFER-{uuid.uuid4()}"),
            "callback_url": transfer_data.get('callback_url', ''),
            "debit_currency": transfer_data.get('debit_currency', 'NGN')
        }
        
        # Add beneficiary details if provided
        if 'beneficiary_name' in transfer_data:
            payload['beneficiary_name'] = transfer_data['beneficiary_name']
        
        response = self._make_request('POST', 'transfers', payload)
        return response
    
    def get_banks(self, country: str = 'NG') -> Dict[str, Any]:
        """
        Get list of banks for a specific country
        
        Args:
            country: Country code (NG, GH, KE, etc.)
            
        Returns:
            List of banks
        """
        response = self._make_request('GET', 'banks', {'country': country})
        return response
    
    def verify_bank_account(self, account_number: str, account_bank: str) -> Dict[str, Any]:
        """
        Verify bank account details
        
        Args:
            account_number: Bank account number
            account_bank: Bank code
            
        Returns:
            Account verification details
        """
        payload = {
            "account_number": account_number,
            "account_bank": account_bank
        }
        
        response = self._make_request('POST', 'accounts/resolve', payload)
        return response
    
    def get_transfer_fee(self, amount: float, currency: str = 'NGN') -> Dict[str, Any]:
        """
        Get transfer fee for a specific amount
        
        Args:
            amount: Transfer amount
            currency: Currency code
            
        Returns:
            Fee calculation details
        """
        response = self._make_request('GET', 'transfers/fee', {
            'amount': amount,
            'currency': currency
        })
        return response
    
    def create_payment_plan(self, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a payment plan for recurring payments
        
        Args:
            plan_data: Payment plan details
            
        Returns:
            Payment plan response
        """
        payload = {
            "amount": plan_data['amount'],
            "name": plan_data['name'],
            "interval": plan_data.get('interval', 'monthly'),  # monthly, weekly, daily
            "duration": plan_data.get('duration', 12),  # number of times to charge
            "currency": plan_data.get('currency', 'NGN')
        }
        
        response = self._make_request('POST', 'payment-plans', payload)
        return response
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """
        Verify webhook signature from Flutterwave
        
        Args:
            payload: Raw webhook payload
            signature: Signature from webhook headers
            
        Returns:
            True if signature is valid
        """
        if not self.secret_key:
            return False
        
        hash_signature = hmac.new(
            self.secret_key.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hash_signature == signature
    
    def save_transaction_to_database(self, flutterwave_response: Dict[str, Any], user_id: int = None) -> Transaction:
        """
        Save Flutterwave transaction to database
        
        Args:
            flutterwave_response: Response from Flutterwave API
            user_id: User ID (optional)
            
        Returns:
            Saved Transaction object
        """
        try:
            # Find or create Flutterwave payment gateway
            gateway = PaymentGateway.query.filter_by(name='Flutterwave').first()
            if not gateway:
                gateway = PaymentGateway()
                gateway.name = 'Flutterwave'
                gateway.description = 'Flutterwave Payment Gateway - African Payment Solutions'
                gateway.is_active = True
                gateway.api_endpoint = self.base_url
                db.session.add(gateway)
                db.session.flush()
            
            # Extract transaction data
            data = flutterwave_response.get('data', {})
            
            transaction = Transaction()
            transaction.transaction_id = data.get('tx_ref', f"FLW-{uuid.uuid4()}")
            transaction.external_id = data.get('id', '')
            transaction.payment_gateway_id = gateway.id
            transaction.user_id = user_id
            transaction.amount = float(data.get('amount', 0))
            transaction.currency = data.get('currency', 'USD')
            transaction.status = self._map_flutterwave_status(data.get('status', 'pending'))
            transaction.gateway_response = json.dumps(flutterwave_response)
            transaction.created_at = datetime.utcnow()
            
            # Add customer information
            customer = data.get('customer', {})
            transaction.payer_info = json.dumps({
                'email': customer.get('email', ''),
                'name': customer.get('name', ''),
                'phone': customer.get('phone_number', '')
            })
            
            transaction.description = data.get('narration', 'Flutterwave payment')
            
            db.session.add(transaction)
            db.session.commit()
            
            return transaction
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving Flutterwave transaction to database: {str(e)}")
            raise
    
    def _map_flutterwave_status(self, flutterwave_status: str) -> str:
        """Map Flutterwave status to internal transaction status"""
        status_mapping = {
            'successful': TransactionStatus.COMPLETED.value,
            'failed': TransactionStatus.FAILED.value,
            'pending': TransactionStatus.PENDING.value,
            'cancelled': TransactionStatus.CANCELLED.value,
        }
        
        return status_mapping.get(flutterwave_status.lower(), TransactionStatus.PENDING.value)
    
    def process_webhook_payment(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming webhook from Flutterwave
        
        Args:
            webhook_data: Webhook payload
            
        Returns:
            Processing result
        """
        try:
            event_type = webhook_data.get('event')
            
            if event_type == 'charge.completed':
                # Verify the payment
                tx_ref = webhook_data.get('data', {}).get('tx_ref')
                if tx_ref:
                    verification_result = self.verify_payment(tx_ref)
                    
                    # Update transaction in database
                    transaction = Transaction.query.filter_by(transaction_id=tx_ref).first()
                    if transaction:
                        data = verification_result.get('data', {})
                        transaction.status = self._map_flutterwave_status(data.get('status', 'pending'))
                        transaction.gateway_response = json.dumps(verification_result)
                        transaction.updated_at = datetime.utcnow()
                        db.session.commit()
                
                return {'status': 'success', 'message': 'Payment webhook processed'}
            
            return {'status': 'ignored', 'message': f'Unhandled event type: {event_type}'}
        
        except Exception as e:
            logger.error(f"Error processing Flutterwave webhook: {str(e)}")
            return {'status': 'error', 'message': str(e)}

# Global service instance
flutterwave_service = FlutterwaveService()