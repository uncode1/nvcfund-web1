'''Fork off utils.py to deal tiwj circular import
   of fortmat_currency and format_transaction_type'''
import locale
import logging

# Set locale for currency formatting
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except:
    # Fallback if locale is not available
    pass

logger = logging.getLogger(__name__)

def format_currency(amount, currency='USD'):
    """Format a monetary amount with currency symbol and 2 decimal places
    
    Args:
        amount (float): The monetary amount to format
        currency (str): The currency code (e.g. 'USD', 'EUR')
        
    Returns:
        str: Formatted currency string (e.g. '$1,234.56')
    """
    if amount is None:
        return f"{currency} 0.00"
        
    # Handle common currency symbols
    currency_symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'CAD': 'C$',
        'AUD': 'A$',
        'CHF': 'CHF',
    }
    
    # Get symbol or use currency code
    symbol = currency_symbols.get(currency, currency)
    
    # Format with thousands separator and 2 decimal places
    if currency == 'JPY':  # JPY traditionally has no decimal places
        formatted = f"{symbol}{int(amount):,}"
    else:
        formatted = f"{symbol}{amount:,.2f}"
        
    return formatted

def format_transaction_type(transaction_type):
    """
    Format transaction type for display in a user-friendly way
    
    Args:
        transaction_type: TransactionType enum value or string
        
    Returns:
        str: Formatted transaction type for display
    """
    # Using a logger instead of print for debugging
    logger.debug(f"format_transaction_type called with {transaction_type}")
    # Convert to string if it's an enum
    if hasattr(transaction_type, 'value'):
        type_value = transaction_type.value
    else:
        type_value = str(transaction_type)
    
    # Define friendly names for transaction types
    friendly_names = {
        'RTGS_TRANSFER': 'Real Time Gross Settlement (RTGS) Transaction',
        'SERVER_TO_SERVER': 'Server-to-Server Transfer',
        'SWIFT_TRANSFER': 'SWIFT Transfer',
        'SWIFT_GPI_PAYMENT': 'SWIFT GPI Payment',
        'SWIFT_LETTER_OF_CREDIT': 'SWIFT Letter of Credit',
        'SWIFT_FUND_TRANSFER': 'SWIFT Fund Transfer (MT103)',
        'SWIFT_INSTITUTION_TRANSFER': 'SWIFT Institution Transfer (MT202)',
        'SWIFT_FREE_FORMAT': 'SWIFT Free Format Message (MT799)',
        'INTERNATIONAL_WIRE': 'International Wire Transfer',
        'OFF_LEDGER_TRANSFER': 'Off-Ledger Transfer',
        'TOKEN_EXCHANGE': 'Token Exchange',
        'EDI_PAYMENT': 'EDI Payment',
        'EDI_ACH_TRANSFER': 'EDI ACH Transfer',
        'EDI_WIRE_TRANSFER': 'EDI Wire Transfer',
        'TREASURY_TRANSFER': 'Treasury Transfer',
        'TREASURY_INVESTMENT': 'Treasury Investment',
        'TREASURY_LOAN': 'Treasury Loan',
        'TREASURY_DEBT_REPAYMENT': 'Treasury Debt Repayment',
        'SALARY_PAYMENT': 'Salary Payment',
        'BILL_PAYMENT': 'Bill Payment',
        'CONTRACT_PAYMENT': 'Contract Payment',
        'BULK_PAYROLL': 'Bulk Payroll Processing',
        'DEPOSIT': 'Deposit',
        'WITHDRAWAL': 'Withdrawal',
        'TRANSFER': 'Transfer',
        'PAYMENT': 'Payment',
        'SETTLEMENT': 'Settlement'
    }
    
    # Return friendly name or formatted original if not found
    return friendly_names.get(type_value, type_value.replace('_', ' ').title())
