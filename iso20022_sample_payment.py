"""
Sample ISO 20022 Payment Creation Demo
Demonstrates creating a realistic payment message
"""

from iso20022_integration import create_iso20022_payment_message
import json
from datetime import datetime

def create_sample_payment():
    """Create a sample ISO 20022 payment for demonstration"""
    
    # Sample payment data - International wire transfer
    payment_data = {
        'creditor_name': 'Deutsche Bank AG',
        'creditor_country': 'DE',
        'creditor_iban': 'DE89370400440532013000',
        'creditor_bank_bic': 'DEUTDEFF',
        'creditor_account_name': 'Corporate Treasury Account',
        'amount': '250000.00',
        'currency': 'EUR',
        'purpose_code': 'TRAD',
        'remittance_info': 'Trade settlement for international commodity purchase - Invoice #INV-2024-001234',
        'instruction_id': f"NVC{datetime.now().strftime('%Y%m%d%H%M%S')}001",
        'end_to_end_id': f"E2E{datetime.now().strftime('%Y%m%d%H%M%S')}001"
    }
    
    try:
        # Generate the ISO 20022 XML message
        xml_message = create_iso20022_payment_message(payment_data)
        
        print("ISO 20022 Payment Message Generated Successfully!")
        print("=" * 60)
        print(f"Instruction ID: {payment_data['instruction_id']}")
        print(f"Beneficiary: {payment_data['creditor_name']}")
        print(f"Amount: {payment_data['currency']} {payment_data['amount']}")
        print(f"Purpose: {payment_data['purpose_code']} - Trade Settlement")
        print("=" * 60)
        print("\nGenerated XML Message:")
        print(xml_message)
        
        return xml_message, payment_data
        
    except Exception as e:
        print(f"Error creating payment: {str(e)}")
        return None, None

if __name__ == "__main__":
    create_sample_payment()