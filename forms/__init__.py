
"""
Forms Package
This package contains all form definitions for the NVC Banking Platform
"""

from .account_forms import AccountHolderForm, AccountForm, AddressForm, PhoneForm
from .capital_injection_forms import (
    FinancialInstitutionProfileForm, 
    CapitalInjectionApplicationForm,
    ApplicationReviewForm,
    DocumentUploadForm,
    CapitalInjectionTermsForm
)
from .payment_forms import TransferForm, DepositForm

__all__ = [
    'AccountHolderForm',
    'AccountForm', 
    'AddressForm',
    'PhoneForm',
    'FinancialInstitutionProfileForm',
    'CapitalInjectionApplicationForm',
    'ApplicationReviewForm',
    'DocumentUploadForm',
    'CapitalInjectionTermsForm',
    'TransferForm',
    'DepositForm'
]
