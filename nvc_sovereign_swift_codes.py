"""
NVC Fund Bank Sovereign SWIFT Code Framework
Supranational Institution under African Union Treaty Authority
"""

from datetime import datetime
from typing import Dict, List

class SovereignSWIFTCode:
    """Represents a sovereign SWIFT code for NVC Fund Bank"""
    
    def __init__(self, bic_code: str, jurisdiction: str, authority_type: str, 
                 services: List[str], treaty_basis: str):
        self.bic_code = bic_code
        self.jurisdiction = jurisdiction
        self.authority_type = authority_type
        self.services = services
        self.treaty_basis = treaty_basis
        self.registration_date = datetime.now()

# NVC Fund Bank Sovereign SWIFT Code Registry
NVC_SOVEREIGN_SWIFT_CODES = {
    # Primary Supranational Authority
    "NVCFGLXX": SovereignSWIFTCode(
        bic_code="NVCFGLXX",
        jurisdiction="Global Supranational",
        authority_type="Primary Sovereign Authority",
        services=["Central Banking", "Treasury Operations", "Sovereign Debt Management", 
                 "Correspondent Banking", "Investment Banking", "Custody Services"],
        treaty_basis="African Union Treaty Framework - Article 19"
    ),
    
    # Existing Australian Operations
    "NVCFBKAU": SovereignSWIFTCode(
        bic_code="NVCFBKAU",
        jurisdiction="Australia",
        authority_type="Sovereign Banking Operations",
        services=["AUD Operations", "Australian Correspondent Banking", "Resource Finance"],
        treaty_basis="AU-Africa Financial Cooperation Agreement"
    ),
    
    # Strategic Global Sovereign Operations
    "NVCFUSNY": SovereignSWIFTCode(
        bic_code="NVCFUSNY",
        jurisdiction="United States - New York",
        authority_type="Sovereign USD Operations",
        services=["USD Clearing", "Federal Reserve Relationships", "US Treasury Operations"],
        treaty_basis="Sovereign Institution Recognition - Federal Reserve"
    ),
    
    "NVCFGBLN": SovereignSWIFTCode(
        bic_code="NVCFGBLN",
        jurisdiction="United Kingdom - London",
        authority_type="Sovereign GBP Operations",
        services=["GBP Clearing", "City of London Operations", "UK Gilt Operations"],
        treaty_basis="UK-Africa Sovereign Banking Arrangement"
    ),
    
    "NVCFCHZH": SovereignSWIFTCode(
        bic_code="NVCFCHZH",
        jurisdiction="Switzerland - Zurich",
        authority_type="Sovereign CHF Operations",
        services=["CHF Operations", "Swiss Banking", "Precious Metals Trading"],
        treaty_basis="Swiss-Africa Sovereign Banking Agreement"
    ),
    
    "NVCFSGSG": SovereignSWIFTCode(
        bic_code="NVCFSGSG",
        jurisdiction="Singapore",
        authority_type="Asian Sovereign Hub",
        services=["Asian Currency Operations", "Commodity Finance", "Islamic Banking"],
        treaty_basis="ASEAN-Africa Sovereign Banking Cooperation"
    ),
    
    "NVCFHKHK": SovereignSWIFTCode(
        bic_code="NVCFHKHK",
        jurisdiction="Hong Kong",
        authority_type="China Gateway Operations",
        services=["HKD Operations", "CNY Offshore", "Belt & Road Finance"],
        treaty_basis="China-Africa Sovereign Financial Cooperation"
    ),
    
    "NVCFAEDH": SovereignSWIFTCode(
        bic_code="NVCFAEDH",
        jurisdiction="UAE - Dubai",
        authority_type="Middle East Sovereign Hub",
        services=["AED Operations", "Islamic Finance", "Oil Finance", "Sharia Banking"],
        treaty_basis="GCC-Africa Sovereign Banking Framework"
    ),
    
    # African Union Member State Operations
    "NVCFZAJO": SovereignSWIFTCode(
        bic_code="NVCFZAJO",
        jurisdiction="South Africa - Johannesburg",
        authority_type="Southern Africa Hub",
        services=["ZAR Operations", "Mining Finance", "SADC Coordination"],
        treaty_basis="African Union Treaty - Article 19"
    ),
    
    "NVCFNGLA": SovereignSWIFTCode(
        bic_code="NVCFNGLA",
        jurisdiction="Nigeria - Lagos",
        authority_type="West Africa Hub",
        services=["NGN Operations", "Oil Finance", "ECOWAS Coordination"],
        treaty_basis="African Union Treaty - Article 19"
    ),
    
    "NVCFKENA": SovereignSWIFTCode(
        bic_code="NVCFKENA",
        jurisdiction="Kenya - Nairobi",
        authority_type="East Africa Hub",
        services=["KES Operations", "Agricultural Finance", "EAC Coordination"],
        treaty_basis="African Union Treaty - Article 19"
    ),
    
    "NVCFEGCA": SovereignSWIFTCode(
        bic_code="NVCFEGCA",
        jurisdiction="Egypt - Cairo",
        authority_type="North Africa Hub",
        services=["EGP Operations", "Suez Finance", "Mediterranean Trade"],
        treaty_basis="African Union Treaty - Article 19"
    ),
    
    # Specialized Sovereign Functions
    "NVCFGLTR": SovereignSWIFTCode(
        bic_code="NVCFGLTR",
        jurisdiction="Global",
        authority_type="Treasury Operations Center",
        services=["Sovereign Debt Issuance", "Central Bank Operations", "Monetary Policy"],
        treaty_basis="African Union Monetary Authority"
    ),
    
    "NVCFGLCU": SovereignSWIFTCode(
        bic_code="NVCFGLCU",
        jurisdiction="Global",
        authority_type="Custody Operations Center",
        services=["Sovereign Asset Custody", "Central Bank Reserves", "Gold Custody"],
        treaty_basis="African Union Asset Management Framework"
    ),
    
    "NVCFGLCO": SovereignSWIFTCode(
        bic_code="NVCFGLCO",
        jurisdiction="Global",
        authority_type="Correspondent Banking Hub",
        services=["Global Correspondent Network", "SWIFT Operations", "Cross-border Payments"],
        treaty_basis="African Union Financial Integration Protocol"
    )
}

def get_sovereign_swift_summary() -> Dict:
    """Return summary of NVC Fund Bank's sovereign SWIFT code network"""
    return {
        "total_codes": len(NVC_SOVEREIGN_SWIFT_CODES),
        "geographic_coverage": {
            "global_hubs": 4,  # Primary, Treasury, Custody, Correspondent
            "african_union_hubs": 4,  # SA, Nigeria, Kenya, Egypt
            "international_hubs": 6,  # US, UK, CH, SG, HK, UAE
            "existing_operations": 1  # Australia
        },
        "service_capabilities": [
            "Central Banking Operations",
            "Sovereign Debt Management", 
            "Multi-currency Operations",
            "Correspondent Banking Network",
            "Asset Custody Services",
            "Investment Banking",
            "Islamic Banking",
            "Commodity Finance",
            "Cross-border Payments"
        ],
        "treaty_authority": "African Union Supranational Sovereign Institution"
    }

if __name__ == "__main__":
    summary = get_sovereign_swift_summary()
    print("NVC Fund Bank Sovereign SWIFT Code Network")
    print("=" * 50)
    print(f"Total SWIFT Codes: {summary['total_codes']}")
    print(f"Geographic Coverage: {summary['geographic_coverage']}")
    print(f"Treaty Authority: {summary['treaty_authority']}")