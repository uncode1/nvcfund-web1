"""
ISO 9362:2022 Implementation for NVC Banking Platform
Business Identifier Code (BIC) Standard Implementation

This module implements the latest ISO 9362:2022 standard for SWIFT Business Identifier Codes,
providing enhanced BIC validation, routing, and financial institution identification capabilities.
"""

import re
import logging
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
import sqlite3
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BICType(Enum):
    """BIC code types according to ISO 9362:2022"""
    INSTITUTION = "INST"  # Financial institution
    CORPORATE = "CORP"    # Corporate entity
    TREASURY = "TRES"     # Treasury operations
    CORRESPONDENT = "CORR" # Correspondent banking

class BICStatus(Enum):
    """BIC status codes"""
    ACTIVE = "A"
    PASSIVE = "P"
    SUSPENDED = "S"
    DELETED = "D"

@dataclass
class BICInfo:
    """BIC information structure according to ISO 9362:2022"""
    bic_code: str
    institution_name: str
    institution_code: str
    country_code: str
    location_code: str
    branch_code: Optional[str]
    bic_type: BICType
    status: BICStatus
    registration_date: datetime
    last_updated: datetime
    services: List[str]
    connectivity_status: str

class ISO9362Validator:
    """ISO 9362:2022 BIC Validator"""
    
    # ISO 9362:2022 BIC format patterns
    BIC8_PATTERN = re.compile(r'^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}$')
    BIC11_PATTERN = re.compile(r'^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}[A-Z0-9]{3}$')
    
    # Country codes (ISO 3166-1 alpha-2)
    VALID_COUNTRY_CODES = {
        'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT',
        'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI',
        'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY',
        'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN',
        'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM',
        'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK',
        'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL',
        'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM',
        'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR',
        'IS', 'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN',
        'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS',
        'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK',
        'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW',
        'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP',
        'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM',
        'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RU', 'RW',
        'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM',
        'SN', 'SO', 'SR', 'SS', 'ST', 'SV', 'SX', 'SY', 'SZ', 'TC', 'TD', 'TF',
        'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW',
        'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI',
        'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW'
    }
    
    @classmethod
    def validate_bic(cls, bic_code: str) -> Tuple[bool, str]:
        """
        Validate BIC code according to ISO 9362:2022 standard
        
        Args:
            bic_code: BIC code to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not bic_code:
            return False, "BIC code cannot be empty"
        
        bic_code = bic_code.upper().strip()
        
        # Check length (8 or 11 characters)
        if len(bic_code) not in [8, 11]:
            return False, "BIC code must be 8 or 11 characters long"
        
        # Validate format
        if len(bic_code) == 8:
            if not cls.BIC8_PATTERN.match(bic_code):
                return False, "Invalid BIC8 format"
        else:
            if not cls.BIC11_PATTERN.match(bic_code):
                return False, "Invalid BIC11 format"
        
        # Extract components
        institution_code = bic_code[0:4]
        country_code = bic_code[4:6]
        location_code = bic_code[6:8]
        branch_code = bic_code[8:11] if len(bic_code) == 11 else None
        
        # Validate institution code (4 letters)
        if not institution_code.isalpha():
            return False, "Institution code must contain only letters"
        
        # Validate country code
        if country_code not in cls.VALID_COUNTRY_CODES:
            return False, f"Invalid country code: {country_code}"
        
        # Validate location code (2 alphanumeric)
        if not location_code.isalnum():
            return False, "Location code must be alphanumeric"
        
        # Validate branch code if present
        if branch_code and not branch_code.isalnum():
            return False, "Branch code must be alphanumeric"
        
        return True, "Valid BIC code"
    
    @classmethod
    def parse_bic(cls, bic_code: str) -> Dict[str, str]:
        """
        Parse BIC code into components
        
        Args:
            bic_code: Valid BIC code
            
        Returns:
            Dictionary with BIC components
        """
        is_valid, error = cls.validate_bic(bic_code)
        if not is_valid:
            raise ValueError(f"Invalid BIC code: {error}")
        
        bic_code = bic_code.upper().strip()
        
        return {
            'institution_code': bic_code[0:4],
            'country_code': bic_code[4:6],
            'location_code': bic_code[6:8],
            'branch_code': bic_code[8:11] if len(bic_code) == 11 else None,
            'is_branch_specific': len(bic_code) == 11,
            'primary_bic': bic_code[0:8]
        }

class BICRegistry:
    """ISO 9362:2022 BIC Registry Implementation"""
    
    def __init__(self, db_path: str = "bic_registry.db"):
        """Initialize BIC registry with SQLite database"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the BIC registry database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS bic_registry (
                    bic_code TEXT PRIMARY KEY,
                    institution_name TEXT NOT NULL,
                    institution_code TEXT NOT NULL,
                    country_code TEXT NOT NULL,
                    location_code TEXT NOT NULL,
                    branch_code TEXT,
                    bic_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    registration_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    services TEXT,
                    connectivity_status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_country_code ON bic_registry(country_code)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_institution_code ON bic_registry(institution_code)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_status ON bic_registry(status)
            """)
    
    def register_bic(self, bic_info: BICInfo) -> bool:
        """
        Register a new BIC code in the registry
        
        Args:
            bic_info: BIC information to register
            
        Returns:
            True if registration successful
        """
        try:
            # Validate BIC format
            is_valid, error = ISO9362Validator.validate_bic(bic_info.bic_code)
            if not is_valid:
                logger.error(f"Invalid BIC format: {error}")
                return False
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO bic_registry 
                    (bic_code, institution_name, institution_code, country_code, 
                     location_code, branch_code, bic_type, status, registration_date, 
                     last_updated, services, connectivity_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    bic_info.bic_code,
                    bic_info.institution_name,
                    bic_info.institution_code,
                    bic_info.country_code,
                    bic_info.location_code,
                    bic_info.branch_code,
                    bic_info.bic_type.value,
                    bic_info.status.value,
                    bic_info.registration_date.isoformat(),
                    bic_info.last_updated.isoformat(),
                    json.dumps(bic_info.services),
                    bic_info.connectivity_status
                ))
            
            logger.info(f"BIC registered successfully: {bic_info.bic_code}")
            return True
            
        except Exception as e:
            logger.error(f"Error registering BIC {bic_info.bic_code}: {str(e)}")
            return False
    
    def lookup_bic(self, bic_code: str) -> Optional[BICInfo]:
        """
        Lookup BIC information from registry
        
        Args:
            bic_code: BIC code to lookup
            
        Returns:
            BICInfo object if found, None otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM bic_registry WHERE bic_code = ?
                """, (bic_code.upper(),))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                return BICInfo(
                    bic_code=row['bic_code'],
                    institution_name=row['institution_name'],
                    institution_code=row['institution_code'],
                    country_code=row['country_code'],
                    location_code=row['location_code'],
                    branch_code=row['branch_code'],
                    bic_type=BICType(row['bic_type']),
                    status=BICStatus(row['status']),
                    registration_date=datetime.fromisoformat(row['registration_date']),
                    last_updated=datetime.fromisoformat(row['last_updated']),
                    services=json.loads(row['services']) if row['services'] else [],
                    connectivity_status=row['connectivity_status']
                )
                
        except Exception as e:
            logger.error(f"Error looking up BIC {bic_code}: {str(e)}")
            return None
    
    def search_by_country(self, country_code: str) -> List[BICInfo]:
        """
        Search BIC codes by country
        
        Args:
            country_code: ISO 3166-1 alpha-2 country code
            
        Returns:
            List of BICInfo objects
        """
        results = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM bic_registry 
                    WHERE country_code = ? AND status = 'A'
                    ORDER BY institution_name
                """, (country_code.upper(),))
                
                for row in cursor.fetchall():
                    results.append(BICInfo(
                        bic_code=row['bic_code'],
                        institution_name=row['institution_name'],
                        institution_code=row['institution_code'],
                        country_code=row['country_code'],
                        location_code=row['location_code'],
                        branch_code=row['branch_code'],
                        bic_type=BICType(row['bic_type']),
                        status=BICStatus(row['status']),
                        registration_date=datetime.fromisoformat(row['registration_date']),
                        last_updated=datetime.fromisoformat(row['last_updated']),
                        services=json.loads(row['services']) if row['services'] else [],
                        connectivity_status=row['connectivity_status']
                    ))
                    
        except Exception as e:
            logger.error(f"Error searching BICs by country {country_code}: {str(e)}")
        
        return results

class SWIFTMessageRouter:
    """Enhanced SWIFT message routing with ISO 9362:2022 support"""
    
    def __init__(self, bic_registry: BICRegistry):
        self.bic_registry = bic_registry
    
    def route_message(self, sender_bic: str, receiver_bic: str, message_type: str) -> Dict[str, any]:
        """
        Route SWIFT message using ISO 9362:2022 BIC validation
        
        Args:
            sender_bic: Sender's BIC code
            receiver_bic: Receiver's BIC code
            message_type: SWIFT message type (e.g., MT103, MT202)
            
        Returns:
            Routing information dictionary
        """
        routing_info = {
            'status': 'pending',
            'sender_valid': False,
            'receiver_valid': False,
            'route_available': False,
            'errors': []
        }
        
        try:
            # Validate sender BIC
            sender_valid, sender_error = ISO9362Validator.validate_bic(sender_bic)
            if not sender_valid:
                routing_info['errors'].append(f"Invalid sender BIC: {sender_error}")
            else:
                routing_info['sender_valid'] = True
                routing_info['sender_info'] = self.bic_registry.lookup_bic(sender_bic)
            
            # Validate receiver BIC
            receiver_valid, receiver_error = ISO9362Validator.validate_bic(receiver_bic)
            if not receiver_valid:
                routing_info['errors'].append(f"Invalid receiver BIC: {receiver_error}")
            else:
                routing_info['receiver_valid'] = True
                routing_info['receiver_info'] = self.bic_registry.lookup_bic(receiver_bic)
            
            # Check if routing is possible
            if routing_info['sender_valid'] and routing_info['receiver_valid']:
                # Additional check: ensure both BICs exist in registry for routing
                sender_info = self.bic_registry.lookup_bic(sender_bic) if routing_info['sender_valid'] else None
                receiver_info = self.bic_registry.lookup_bic(receiver_bic) if routing_info['receiver_valid'] else None
                
                if sender_info and receiver_info:
                    routing_info['route_available'] = True
                    routing_info['status'] = 'route_available'
                    routing_info['message_type'] = message_type
                    routing_info['routing_path'] = self._calculate_routing_path(sender_bic, receiver_bic)
                    routing_info['estimated_delivery'] = 'Same day'
                    routing_info['routing_method'] = 'Direct SWIFT Network'
                else:
                    routing_info['route_available'] = False
                    routing_info['status'] = 'route_unavailable'
                    if not sender_info:
                        routing_info['errors'].append(f"Sender BIC {sender_bic} not found in registry")
                    if not receiver_info:
                        routing_info['errors'].append(f"Receiver BIC {receiver_bic} not found in registry")
            else:
                routing_info['route_available'] = False
                routing_info['status'] = 'validation_failed'
            
        except Exception as e:
            routing_info['errors'].append(f"Routing error: {str(e)}")
            routing_info['status'] = 'error'
        
        return routing_info
    
    def _calculate_routing_path(self, sender_bic: str, receiver_bic: str) -> List[str]:
        """Calculate optimal routing path between BICs"""
        # For now, direct routing
        # In production, this would implement correspondent banking path calculation
        return [sender_bic, receiver_bic]

def initialize_nvc_bic_registry():
    """Initialize BIC registry with NVC Fund Bank and common correspondent banks"""
    registry = BICRegistry()
    
    # Register NVC Fund Bank BIC
    nvc_bic = BICInfo(
        bic_code="NVCFGLXX",  # NVC Fund Global
        institution_name="NVC Fund Bank",
        institution_code="NVCF",
        country_code="GL",  # Global operations
        location_code="XX",
        branch_code=None,
        bic_type=BICType.INSTITUTION,
        status=BICStatus.ACTIVE,
        registration_date=datetime.now(),
        last_updated=datetime.now(),
        services=["SWIFT", "ISO20022", "Correspondent Banking", "Treasury", "Trade Finance"],
        connectivity_status="LIVE"
    )
    
    registry.register_bic(nvc_bic)
    
    # Register some major correspondent banks for testing
    correspondent_banks = [
        {
            'bic_code': 'CHASUS33',
            'institution_name': 'JPMorgan Chase Bank N.A.',
            'country_code': 'US'
        },
        {
            'bic_code': 'CITIUS33',
            'institution_name': 'Citibank N.A.',
            'country_code': 'US'
        },
        {
            'bic_code': 'DEUTDEFF',
            'institution_name': 'Deutsche Bank AG',
            'country_code': 'DE'
        },
        {
            'bic_code': 'HSBCGB2L',
            'institution_name': 'HSBC Bank plc',
            'country_code': 'GB'
        },
        {
            'bic_code': 'HBUKGB4B',
            'institution_name': 'HSBC Bank plc',
            'country_code': 'GB'
        }
    ]
    
    for bank in correspondent_banks:
        correspondent_bic = BICInfo(
            bic_code=bank['bic_code'],
            institution_name=bank['institution_name'],
            institution_code=bank['bic_code'][0:4],
            country_code=bank['country_code'],
            location_code=bank['bic_code'][6:8],
            branch_code=None,
            bic_type=BICType.CORRESPONDENT,
            status=BICStatus.ACTIVE,
            registration_date=datetime.now(),
            last_updated=datetime.now(),
            services=["SWIFT", "Correspondent Banking"],
            connectivity_status="LIVE"
        )
        registry.register_bic(correspondent_bic)
    
    logger.info("BIC registry initialized with NVC Fund Bank and correspondent banks")
    return registry

if __name__ == "__main__":
    # Test ISO 9362:2022 implementation
    print("Testing ISO 9362:2022 Implementation")
    print("=" * 50)
    
    # Test BIC validation
    test_bics = [
        "NVCFGLXX",      # Valid BIC8
        "CHASUS33XXX",   # Valid BIC11
        "INVALID",       # Invalid
        "TESTXX22",      # Valid format, fictional
    ]
    
    for bic in test_bics:
        is_valid, message = ISO9362Validator.validate_bic(bic)
        print(f"BIC: {bic} - {'✓' if is_valid else '✗'} {message}")
    
    print("\nInitializing BIC Registry...")
    registry = initialize_nvc_bic_registry()
    
    print("\nTesting BIC lookup...")
    nvc_info = registry.lookup_bic("NVCFGLXX")
    if nvc_info:
        print(f"Found: {nvc_info.institution_name} - Status: {nvc_info.status.value}")
    
    print("\nTesting SWIFT message routing...")
    router = SWIFTMessageRouter(registry)
    routing = router.route_message("NVCFGLXX", "CHASUS33", "MT103")
    print(f"Routing status: {routing['status']}")
    print(f"Route available: {routing['route_available']}")