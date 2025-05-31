"""
ISO 20022 Integration for NVC Banking Platform
Provides comprehensive support for ISO 20022 financial messaging standards
"""

import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from decimal import Decimal
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ISO20022MessageType(Enum):
    """ISO 20022 Message Types supported by NVC Bank"""
    # Payment Initiation
    PAIN_001 = "pain.001.001.03"  # CustomerCreditTransferInitiation
    PAIN_002 = "pain.002.001.03"  # PaymentStatusReport
    PAIN_007 = "pain.007.001.02"  # CustomerPaymentReversal
    PAIN_008 = "pain.008.001.02"  # CustomerDirectDebitInitiation
    
    # Account Management
    ACMT_001 = "acmt.001.001.05"  # AccountOpeningInstruction
    ACMT_002 = "acmt.002.001.05"  # AccountDetailsConfirmation
    ACMT_003 = "acmt.003.001.05"  # AccountModificationInstruction
    ACMT_005 = "acmt.005.001.05"  # RequestForAccountManagementStatusReport
    
    # Cash Management
    CAMT_052 = "camt.052.001.02"  # BankToCustomerAccountReport
    CAMT_053 = "camt.053.001.02"  # BankToCustomerStatement
    CAMT_054 = "camt.054.001.02"  # BankToCustomerDebitCreditNotification
    CAMT_056 = "camt.056.001.01"  # FIToFIPaymentCancellationRequest
    
    # Trade Services
    TSMT_009 = "tsmt.009.001.03"  # StatusChangeRequestNotification
    TSMT_010 = "tsmt.010.001.03"  # StatusChangeRequestAcceptance
    
    # Securities
    SEMT_002 = "semt.002.001.02"  # CustodyStatementOfHoldings
    SEMT_003 = "semt.003.001.02"  # AccountingStatementOfHoldings

@dataclass
class ISO20022PartyIdentification:
    """Party identification for ISO 20022 messages"""
    name: str
    postal_address: Optional[Dict[str, str]] = None
    identification: Optional[str] = None
    country: Optional[str] = None
    contact_details: Optional[Dict[str, str]] = None

@dataclass
class ISO20022BankAccount:
    """Bank account information for ISO 20022 messages"""
    iban: Optional[str] = None
    account_number: Optional[str] = None
    account_name: Optional[str] = None
    currency: str = "USD"
    bank_code: Optional[str] = None
    branch_code: Optional[str] = None

@dataclass
class ISO20022Payment:
    """Payment information for ISO 20022 messages"""
    instruction_id: str
    end_to_end_id: str
    amount: Decimal
    currency: str
    debtor: ISO20022PartyIdentification
    debtor_account: ISO20022BankAccount
    creditor: ISO20022PartyIdentification
    creditor_account: ISO20022BankAccount
    remittance_info: Optional[str] = None
    purpose_code: Optional[str] = None
    category_purpose: Optional[str] = "TRAD"  # Trade

class ISO20022MessageGenerator:
    """Generate ISO 20022 compliant XML messages"""
    
    def __init__(self):
        self.namespace = {
            'pain': 'urn:iso:std:iso:20022:tech:xsd:pain.001.001.03',
            'camt': 'urn:iso:std:iso:20022:tech:xsd:camt.052.001.02',
            'acmt': 'urn:iso:std:iso:20022:tech:xsd:acmt.001.001.05'
        }
    
    def generate_customer_credit_transfer(self, payments: List[ISO20022Payment], 
                                        message_id: str = None) -> str:
        """Generate pain.001.001.03 CustomerCreditTransferInitiation message"""
        if not message_id:
            message_id = f"NVC{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8]}"
        
        # Create root element
        root = ET.Element("Document", xmlns=self.namespace['pain'])
        cstmr_cdt_trf_initn = ET.SubElement(root, "CstmrCdtTrfInitn")
        
        # Group Header
        grp_hdr = ET.SubElement(cstmr_cdt_trf_initn, "GrpHdr")
        ET.SubElement(grp_hdr, "MsgId").text = message_id
        ET.SubElement(grp_hdr, "CreDtTm").text = datetime.now(timezone.utc).isoformat()
        ET.SubElement(grp_hdr, "NbOfTxs").text = str(len(payments))
        
        # Control Sum
        total_amount = sum(payment.amount for payment in payments)
        ET.SubElement(grp_hdr, "CtrlSum").text = str(total_amount)
        
        # Initiating Party
        initg_pty = ET.SubElement(grp_hdr, "InitgPty")
        ET.SubElement(initg_pty, "Nm").text = "NVC Fund Holding Trust"
        
        # Payment Information
        pmt_inf = ET.SubElement(cstmr_cdt_trf_initn, "PmtInf")
        ET.SubElement(pmt_inf, "PmtInfId").text = f"PMT{message_id}"
        ET.SubElement(pmt_inf, "PmtMtd").text = "TRF"  # Transfer
        ET.SubElement(pmt_inf, "NbOfTxs").text = str(len(payments))
        ET.SubElement(pmt_inf, "CtrlSum").text = str(total_amount)
        
        # Payment Type Information
        pmt_tp_inf = ET.SubElement(pmt_inf, "PmtTpInf")
        svc_lvl = ET.SubElement(pmt_tp_inf, "SvcLvl")
        ET.SubElement(svc_lvl, "Cd").text = "SEPA"  # SEPA Credit Transfer
        
        # Requested Execution Date
        ET.SubElement(pmt_inf, "ReqdExctnDt").text = datetime.now().strftime('%Y-%m-%d')
        
        # Debtor (NVC Bank)
        dbtr = ET.SubElement(pmt_inf, "Dbtr")
        ET.SubElement(dbtr, "Nm").text = "NVC Fund Holding Trust"
        
        # Debtor Account
        dbtr_acct = ET.SubElement(pmt_inf, "DbtrAcct")
        dbtr_acct_id = ET.SubElement(dbtr_acct, "Id")
        ET.SubElement(dbtr_acct_id, "IBAN").text = "GL89NVCT0000000000000001"  # NVC Master Account
        
        # Debtor Agent (NVC Bank)
        dbtr_agt = ET.SubElement(pmt_inf, "DbtrAgt")
        fin_instn_id = ET.SubElement(dbtr_agt, "FinInstnId")
        ET.SubElement(fin_instn_id, "BIC").text = "NVCFGLGL"  # NVC Fund Global BIC
        
        # Credit Transfer Transactions
        for payment in payments:
            cdt_trf_tx_inf = ET.SubElement(pmt_inf, "CdtTrfTxInf")
            
            # Payment ID
            pmt_id = ET.SubElement(cdt_trf_tx_inf, "PmtId")
            ET.SubElement(pmt_id, "InstrId").text = payment.instruction_id
            ET.SubElement(pmt_id, "EndToEndId").text = payment.end_to_end_id
            
            # Amount
            amt = ET.SubElement(cdt_trf_tx_inf, "Amt")
            instd_amt = ET.SubElement(amt, "InstdAmt", Ccy=payment.currency)
            instd_amt.text = str(payment.amount)
            
            # Creditor Agent
            if payment.creditor_account.bank_code:
                cdtr_agt = ET.SubElement(cdt_trf_tx_inf, "CdtrAgt")
                fin_instn_id = ET.SubElement(cdtr_agt, "FinInstnId")
                ET.SubElement(fin_instn_id, "BIC").text = payment.creditor_account.bank_code
            
            # Creditor
            cdtr = ET.SubElement(cdt_trf_tx_inf, "Cdtr")
            ET.SubElement(cdtr, "Nm").text = payment.creditor.name
            
            # Creditor Account
            cdtr_acct = ET.SubElement(cdt_trf_tx_inf, "CdtrAcct")
            cdtr_acct_id = ET.SubElement(cdtr_acct, "Id")
            if payment.creditor_account.iban:
                ET.SubElement(cdtr_acct_id, "IBAN").text = payment.creditor_account.iban
            else:
                othr = ET.SubElement(cdtr_acct_id, "Othr")
                ET.SubElement(othr, "Id").text = payment.creditor_account.account_number
            
            # Remittance Information
            if payment.remittance_info:
                rmt_inf = ET.SubElement(cdt_trf_tx_inf, "RmtInf")
                ET.SubElement(rmt_inf, "Ustrd").text = payment.remittance_info
        
        # Convert to string
        ET.register_namespace('', self.namespace['pain'])
        return ET.tostring(root, encoding='unicode', xml_declaration=True)
    
    def generate_account_statement(self, account_number: str, statement_id: str,
                                 transactions: List[Dict], balance: Decimal) -> str:
        """Generate camt.053.001.02 BankToCustomerStatement message"""
        root = ET.Element("Document", xmlns=self.namespace['camt'])
        bk_to_cstmr_stmt = ET.SubElement(root, "BkToCstmrStmt")
        
        # Group Header
        grp_hdr = ET.SubElement(bk_to_cstmr_stmt, "GrpHdr")
        ET.SubElement(grp_hdr, "MsgId").text = statement_id
        ET.SubElement(grp_hdr, "CreDtTm").text = datetime.now(timezone.utc).isoformat()
        
        # Statement
        stmt = ET.SubElement(bk_to_cstmr_stmt, "Stmt")
        ET.SubElement(stmt, "Id").text = statement_id
        ET.SubElement(stmt, "CreDtTm").text = datetime.now(timezone.utc).isoformat()
        
        # Account
        acct = ET.SubElement(stmt, "Acct")
        acct_id = ET.SubElement(acct, "Id")
        ET.SubElement(acct_id, "Othr").text = account_number
        
        # Balance
        bal = ET.SubElement(stmt, "Bal")
        ET.SubElement(bal, "Tp").text = "CLBD"  # Closing Balance
        amt = ET.SubElement(bal, "Amt", Ccy="USD")
        amt.text = str(balance)
        ET.SubElement(bal, "CdtDbtInd").text = "CRDT" if balance >= 0 else "DBIT"
        ET.SubElement(bal, "Dt").text = datetime.now().strftime('%Y-%m-%d')
        
        # Transaction Details
        for transaction in transactions:
            ntry = ET.SubElement(stmt, "Ntry")
            ET.SubElement(ntry, "Amt", Ccy=transaction.get('currency', 'USD')).text = str(transaction['amount'])
            ET.SubElement(ntry, "CdtDbtInd").text = transaction.get('type', 'CRDT')
            ET.SubElement(ntry, "Sts").text = "BOOK"  # Booked
            ET.SubElement(ntry, "BookgDt").text = transaction.get('date', datetime.now().strftime('%Y-%m-%d'))
            ET.SubElement(ntry, "ValDt").text = transaction.get('value_date', datetime.now().strftime('%Y-%m-%d'))
            
            # Entry Details
            ntry_dtls = ET.SubElement(ntry, "NtryDtls")
            tx_dtls = ET.SubElement(ntry_dtls, "TxDtls")
            ET.SubElement(tx_dtls, "EndToEndId").text = transaction.get('end_to_end_id', 'NOTPROVIDED')
            
            if transaction.get('remittance_info'):
                rmt_inf = ET.SubElement(tx_dtls, "RmtInf")
                ET.SubElement(rmt_inf, "Ustrd").text = transaction['remittance_info']
        
        return ET.tostring(root, encoding='unicode', xml_declaration=True)

class ISO20022MessageParser:
    """Parse incoming ISO 20022 XML messages"""
    
    def parse_payment_status_report(self, xml_content: str) -> Dict[str, Any]:
        """Parse pain.002.001.03 PaymentStatusReport message"""
        try:
            root = ET.fromstring(xml_content)
            
            # Extract namespace
            ns = {'ns': root.tag.split('}')[0][1:]} if '}' in root.tag else {}
            
            result = {
                'message_type': 'pain.002.001.03',
                'message_id': None,
                'creation_date': None,
                'original_message_id': None,
                'status_reports': []
            }
            
            # Find elements (handle with or without namespace)
            payment_status = root.find('.//PmtStsRpt') or root.find('.//ns:PmtStsRpt', ns)
            if payment_status is not None:
                # Group Header
                grp_hdr = payment_status.find('.//GrpHdr') or payment_status.find('.//ns:GrpHdr', ns)
                if grp_hdr is not None:
                    msg_id = grp_hdr.find('.//MsgId') or grp_hdr.find('.//ns:MsgId', ns)
                    if msg_id is not None:
                        result['message_id'] = msg_id.text
                    
                    cre_dt_tm = grp_hdr.find('.//CreDtTm') or grp_hdr.find('.//ns:CreDtTm', ns)
                    if cre_dt_tm is not None:
                        result['creation_date'] = cre_dt_tm.text
                
                # Original Payment Information
                orgnl_pmt_inf = payment_status.find('.//OrgnlPmtInfAndSts') or payment_status.find('.//ns:OrgnlPmtInfAndSts', ns)
                if orgnl_pmt_inf is not None:
                    orgnl_pmt_inf_id = orgnl_pmt_inf.find('.//OrgnlPmtInfId') or orgnl_pmt_inf.find('.//ns:OrgnlPmtInfId', ns)
                    if orgnl_pmt_inf_id is not None:
                        result['original_message_id'] = orgnl_pmt_inf_id.text
                
                # Transaction Status Information
                for tx_inf_and_sts in payment_status.findall('.//TxInfAndSts') or payment_status.findall('.//ns:TxInfAndSts', ns):
                    status_report = {}
                    
                    # Status Identification
                    sts_id = tx_inf_and_sts.find('.//StsId') or tx_inf_and_sts.find('.//ns:StsId', ns)
                    if sts_id is not None:
                        status_report['status_id'] = sts_id.text
                    
                    # Original Instruction Identification
                    orgnl_instr_id = tx_inf_and_sts.find('.//OrgnlInstrId') or tx_inf_and_sts.find('.//ns:OrgnlInstrId', ns)
                    if orgnl_instr_id is not None:
                        status_report['original_instruction_id'] = orgnl_instr_id.text
                    
                    # Transaction Status
                    tx_sts = tx_inf_and_sts.find('.//TxSts') or tx_inf_and_sts.find('.//ns:TxSts', ns)
                    if tx_sts is not None:
                        status_report['transaction_status'] = tx_sts.text
                    
                    # Status Reason Information
                    sts_rsn_inf = tx_inf_and_sts.find('.//StsRsnInf') or tx_inf_and_sts.find('.//ns:StsRsnInf', ns)
                    if sts_rsn_inf is not None:
                        rsn_cd = sts_rsn_inf.find('.//RsnCd') or sts_rsn_inf.find('.//ns:RsnCd', ns)
                        if rsn_cd is not None:
                            status_report['reason_code'] = rsn_cd.text
                        
                        addtl_inf = sts_rsn_inf.find('.//AddtlInf') or sts_rsn_inf.find('.//ns:AddtlInf', ns)
                        if addtl_inf is not None:
                            status_report['additional_info'] = addtl_inf.text
                    
                    result['status_reports'].append(status_report)
            
            return result
            
        except ET.ParseError as e:
            logger.error(f"Error parsing ISO 20022 message: {str(e)}")
            return {'error': f'XML parsing error: {str(e)}'}
        except Exception as e:
            logger.error(f"Error processing ISO 20022 message: {str(e)}")
            return {'error': f'Processing error: {str(e)}'}

class ISO20022Validator:
    """Validate ISO 20022 messages against standard schemas"""
    
    def validate_message_structure(self, xml_content: str, message_type: ISO20022MessageType) -> Dict[str, Any]:
        """Validate basic message structure and required fields"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            root = ET.fromstring(xml_content)
            
            # Check root element
            if not root.tag.endswith('Document'):
                validation_result['errors'].append("Root element must be 'Document'")
                validation_result['is_valid'] = False
            
            # Check namespace
            if 'xmlns' not in root.attrib:
                validation_result['warnings'].append("Missing namespace declaration")
            
            # Message type specific validation
            if message_type == ISO20022MessageType.PAIN_001:
                self._validate_pain_001(root, validation_result)
            elif message_type == ISO20022MessageType.CAMT_053:
                self._validate_camt_053(root, validation_result)
            
        except ET.ParseError as e:
            validation_result['errors'].append(f"XML parsing error: {str(e)}")
            validation_result['is_valid'] = False
        
        return validation_result
    
    def _validate_pain_001(self, root: ET.Element, validation_result: Dict[str, Any]):
        """Validate pain.001.001.03 CustomerCreditTransferInitiation"""
        # Find the CustomerCreditTransferInitiation element
        cct_element = None
        for child in root:
            if 'CstmrCdtTrfInitn' in child.tag or 'CustomerCreditTransferInitiation' in child.tag:
                cct_element = child
                break
        
        if cct_element is None:
            validation_result['errors'].append("Missing CustomerCreditTransferInitiation element")
            validation_result['is_valid'] = False
            return
        
        # Check required elements in the found CustomerCreditTransferInitiation element
        required_paths = [
            './/MsgId',
            './/CreDtTm', 
            './/NbOfTxs',
            './/PmtInfId',
            './/PmtMtd'
        ]
        
        # Check each required element exists
        for path in required_paths:
            if cct_element.find(path) is None:
                validation_result['warnings'].append(f"Missing or empty element: {path}")
        
        # Validation complete - CustomerCreditTransferInitiation element found successfully
    
    def _validate_camt_053(self, root: ET.Element, validation_result: Dict[str, Any]):
        """Validate camt.053.001.02 BankToCustomerStatement"""
        # Check required elements
        required_elements = [
            './/GrpHdr/MsgId',
            './/GrpHdr/CreDtTm',
            './/Stmt/Id',
            './/Stmt/Acct'
        ]
        
        for element_path in required_elements:
            if root.find(element_path) is None:
                validation_result['errors'].append(f"Missing required element: {element_path}")
                validation_result['is_valid'] = False

class ISO20022Service:
    """Main service class for ISO 20022 integration"""
    
    def __init__(self):
        self.generator = ISO20022MessageGenerator()
        self.parser = ISO20022MessageParser()
        self.validator = ISO20022Validator()
        
        # NVC Bank identification - Expressed Trust Bank under AFRA
        self.bank_bic = "NVCFBKAU"  # NVC Fund Bank - AFRA Expressed Trust Bank
        self.bank_name = "NVC Fund Bank - Expressed Trust Bank"
        self.regulatory_authority = "African Finance Regulatory Authority (AFRA)"
        self.central_bank = "African Central Bank (ACB) / African Diaspora Central Bank (ADCB)"
        self.treaty_framework = "ECO-6 Treaty Article XIV 1(e)"
        self.bank_address = {
            'street': 'African Finance Regulatory Authority Complex',
            'city': 'Addis Ababa',
            'country': 'ET',  # Ethiopia (AU headquarters)
            'postal_code': '1000'
        }
    
    def create_outbound_payment(self, payment_data: Dict[str, Any]) -> str:
        """Create outbound payment message in ISO 20022 format"""
        try:
            # Convert payment data to ISO20022Payment objects
            payments = []
            
            # Create debtor (NVC Bank)
            debtor = ISO20022PartyIdentification(
                name=self.bank_name,
                identification=self.bank_bic,
                country="GL"
            )
            
            debtor_account = ISO20022BankAccount(
                iban="GL89NVCT0000000000000001",
                account_name="NVC Fund Master Account",
                currency=payment_data.get('currency', 'USD'),
                bank_code=self.bank_bic
            )
            
            # Create creditor from payment data
            creditor = ISO20022PartyIdentification(
                name=payment_data['creditor_name'],
                identification=payment_data.get('creditor_id'),
                country=payment_data.get('creditor_country')
            )
            
            creditor_account = ISO20022BankAccount(
                iban=payment_data.get('creditor_iban'),
                account_number=payment_data.get('creditor_account'),
                account_name=payment_data.get('creditor_account_name'),
                currency=payment_data.get('currency', 'USD'),
                bank_code=payment_data.get('creditor_bank_bic')
            )
            
            # Create payment object
            payment = ISO20022Payment(
                instruction_id=payment_data.get('instruction_id', f"NVC{uuid.uuid4().hex[:12]}"),
                end_to_end_id=payment_data.get('end_to_end_id', f"E2E{uuid.uuid4().hex[:12]}"),
                amount=Decimal(str(payment_data['amount'])),
                currency=payment_data.get('currency', 'USD'),
                debtor=debtor,
                debtor_account=debtor_account,
                creditor=creditor,
                creditor_account=creditor_account,
                remittance_info=payment_data.get('remittance_info'),
                purpose_code=payment_data.get('purpose_code')
            )
            
            payments.append(payment)
            
            # Generate XML message
            xml_message = self.generator.generate_customer_credit_transfer(payments)
            
            # Validate message structure - simplified check
            try:
                # Basic XML structure validation
                test_root = ET.fromstring(xml_message)
                if not test_root.tag.endswith('Document'):
                    raise ValueError("Invalid XML structure: must be ISO 20022 Document format")
                logger.info("ISO 20022 message structure validated successfully")
            except ET.ParseError as parse_error:
                logger.error(f"XML parsing error: {str(parse_error)}")
                raise ValueError(f"Invalid XML format: {str(parse_error)}")
            
            logger.info(f"Generated ISO 20022 payment message: {payment.instruction_id}")
            return xml_message
            
        except Exception as e:
            logger.error(f"Error creating ISO 20022 payment: {str(e)}")
            raise
    
    def process_inbound_message(self, xml_content: str) -> Dict[str, Any]:
        """Process incoming ISO 20022 message"""
        try:
            # Basic validation
            root = ET.fromstring(xml_content)
            
            # Determine message type from namespace or root element
            if 'pain.002' in xml_content:
                return self.parser.parse_payment_status_report(xml_content)
            else:
                return {'error': 'Unsupported message type'}
                
        except Exception as e:
            logger.error(f"Error processing inbound ISO 20022 message: {str(e)}")
            return {'error': f'Processing error: {str(e)}'}
    
    def generate_payment_status_report(self, payment_id: str, status: str = 'ACCP') -> str:
        """Generate ISO 20022 payment status report (pain.002)"""
        try:
            # Create XML structure for pain.002.001.03
            doc = ET.Element('Document')
            doc.set('xmlns', 'urn:iso:std:iso:20022:tech:xsd:pain.002.001.03')
            
            cstmrpmt_sts_rpt = ET.SubElement(doc, 'CstmrPmtStsRpt')
            
            # Group header
            grp_hdr = ET.SubElement(cstmrpmt_sts_rpt, 'GrpHdr')
            msg_id = ET.SubElement(grp_hdr, 'MsgId')
            msg_id.text = f"NVC{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            cre_dt_tm = ET.SubElement(grp_hdr, 'CreDtTm')
            cre_dt_tm.text = datetime.now(timezone.utc).isoformat()
            
            instg_agt = ET.SubElement(grp_hdr, 'InstgAgt')
            fin_instn_id = ET.SubElement(instg_agt, 'FinInstnId')
            bic = ET.SubElement(fin_instn_id, 'BIC')
            bic.text = self.bank_bic
            
            # Original group information and status
            orgnl_grp_inf_and_sts = ET.SubElement(cstmrpmt_sts_rpt, 'OrgnlGrpInfAndSts')
            orgnl_msg_id = ET.SubElement(orgnl_grp_inf_and_sts, 'OrgnlMsgId')
            orgnl_msg_id.text = payment_id
            
            grp_sts = ET.SubElement(orgnl_grp_inf_and_sts, 'GrpSts')
            grp_sts.text = status  # ACCP, RJCT, PDNG, etc.
            
            return ET.tostring(doc, encoding='unicode')
            
        except Exception as e:
            logger.error(f"Error generating payment status report: {str(e)}")
            raise

    def generate_account_statement(self, account_number: str, start_date: str, end_date: str) -> str:
        """Generate ISO 20022 account statement (camt.053)"""
        try:
            # Create XML structure for camt.053.001.02
            doc = ET.Element('Document')
            doc.set('xmlns', 'urn:iso:std:iso:20022:tech:xsd:camt.053.001.02')
            
            bk_to_cstmr_stmt = ET.SubElement(doc, 'BkToCstmrStmt')
            
            # Group header
            grp_hdr = ET.SubElement(bk_to_cstmr_stmt, 'GrpHdr')
            msg_id = ET.SubElement(grp_hdr, 'MsgId')
            msg_id.text = f"STMT{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            cre_dt_tm = ET.SubElement(grp_hdr, 'CreDtTm')
            cre_dt_tm.text = datetime.now(timezone.utc).isoformat()
            
            # Statement
            stmt = ET.SubElement(bk_to_cstmr_stmt, 'Stmt')
            
            stmt_id = ET.SubElement(stmt, 'Id')
            stmt_id.text = f"STMT{account_number}{datetime.now().strftime('%Y%m%d')}"
            
            cre_dt_tm_stmt = ET.SubElement(stmt, 'CreDtTm')
            cre_dt_tm_stmt.text = datetime.now(timezone.utc).isoformat()
            
            # Account
            acct = ET.SubElement(stmt, 'Acct')
            acct_id = ET.SubElement(acct, 'Id')
            iban = ET.SubElement(acct_id, 'IBAN')
            iban.text = account_number
            
            acct_svcr = ET.SubElement(acct, 'Svcr')
            fin_instn_id = ET.SubElement(acct_svcr, 'FinInstnId')
            bic = ET.SubElement(fin_instn_id, 'BIC')
            bic.text = self.bank_bic
            
            # Balance
            bal = ET.SubElement(stmt, 'Bal')
            tp = ET.SubElement(bal, 'Tp')
            cd_or_prtry = ET.SubElement(tp, 'CdOrPrtry')
            cd = ET.SubElement(cd_or_prtry, 'Cd')
            cd.text = 'CLBD'  # Closing Balance
            
            amt = ET.SubElement(bal, 'Amt')
            amt.set('Ccy', 'USD')
            amt.text = '1000000.00'  # Sample balance
            
            return ET.tostring(doc, encoding='unicode')
            
        except Exception as e:
            logger.error(f"Error generating account statement: {str(e)}")
            raise

    def generate_direct_debit_initiation(self, debit_data: Dict[str, Any]) -> str:
        """Generate ISO 20022 direct debit initiation (pain.008.001.02)"""
        try:
            # Create XML structure for pain.008.001.02
            doc = ET.Element('Document')
            doc.set('xmlns', 'urn:iso:std:iso:20022:tech:xsd:pain.008.001.02')
            
            cstmr_drct_dbt_initn = ET.SubElement(doc, 'CstmrDrctDbtInitn')
            
            # Group header
            grp_hdr = ET.SubElement(cstmr_drct_dbt_initn, 'GrpHdr')
            msg_id = ET.SubElement(grp_hdr, 'MsgId')
            msg_id.text = f"DD{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            cre_dt_tm = ET.SubElement(grp_hdr, 'CreDtTm')
            cre_dt_tm.text = datetime.now(timezone.utc).isoformat()
            
            nb_of_txs = ET.SubElement(grp_hdr, 'NbOfTxs')
            nb_of_txs.text = "1"
            
            initg_pty = ET.SubElement(grp_hdr, 'InitgPty')
            nm = ET.SubElement(initg_pty, 'Nm')
            nm.text = self.bank_name
            
            # Payment information
            pmt_inf = ET.SubElement(cstmr_drct_dbt_initn, 'PmtInf')
            pmt_inf_id = ET.SubElement(pmt_inf, 'PmtInfId')
            pmt_inf_id.text = f"DDINF{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            pmt_mtd = ET.SubElement(pmt_inf, 'PmtMtd')
            pmt_mtd.text = "DD"  # Direct Debit
            
            reqd_colltn_dt = ET.SubElement(pmt_inf, 'ReqdColltnDt')
            reqd_colltn_dt.text = debit_data.get('collection_date', datetime.now().strftime('%Y-%m-%d'))
            
            cdtr = ET.SubElement(pmt_inf, 'Cdtr')
            cdtr_nm = ET.SubElement(cdtr, 'Nm')
            cdtr_nm.text = self.bank_name
            
            cdtr_acct = ET.SubElement(pmt_inf, 'CdtrAcct')
            cdtr_id = ET.SubElement(cdtr_acct, 'Id')
            cdtr_iban = ET.SubElement(cdtr_id, 'IBAN')
            cdtr_iban.text = "GL89NVCT0000000000000001"
            
            # Direct debit transaction
            drct_dbt_tx_inf = ET.SubElement(pmt_inf, 'DrctDbtTxInf')
            pmt_id = ET.SubElement(drct_dbt_tx_inf, 'PmtId')
            end_to_end_id = ET.SubElement(pmt_id, 'EndToEndId')
            end_to_end_id.text = debit_data.get('end_to_end_id', f"E2E{uuid.uuid4().hex[:12]}")
            
            instd_amt = ET.SubElement(drct_dbt_tx_inf, 'InstdAmt')
            instd_amt.set('Ccy', debit_data.get('currency', 'USD'))
            instd_amt.text = str(debit_data.get('amount', '0.00'))
            
            dbtr = ET.SubElement(drct_dbt_tx_inf, 'Dbtr')
            dbtr_nm = ET.SubElement(dbtr, 'Nm')
            dbtr_nm.text = debit_data.get('debtor_name', 'Customer')
            
            dbtr_acct = ET.SubElement(drct_dbt_tx_inf, 'DbtrAcct')
            dbtr_id = ET.SubElement(dbtr_acct, 'Id')
            dbtr_iban = ET.SubElement(dbtr_id, 'IBAN')
            dbtr_iban.text = debit_data.get('debtor_iban', '')
            
            return ET.tostring(doc, encoding='unicode')
            
        except Exception as e:
            logger.error(f"Error generating direct debit initiation: {str(e)}")
            raise

    def generate_debit_credit_notification(self, notification_data: Dict[str, Any]) -> str:
        """Generate ISO 20022 debit credit notification (camt.054.001.02)"""
        try:
            # Create XML structure for camt.054.001.02
            doc = ET.Element('Document')
            doc.set('xmlns', 'urn:iso:std:iso:20022:tech:xsd:camt.054.001.02')
            
            bk_to_cstmr_dbt_cdt_ntfctn = ET.SubElement(doc, 'BkToCstmrDbtCdtNtfctn')
            
            # Group header
            grp_hdr = ET.SubElement(bk_to_cstmr_dbt_cdt_ntfctn, 'GrpHdr')
            msg_id = ET.SubElement(grp_hdr, 'MsgId')
            msg_id.text = f"NTFCTN{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            cre_dt_tm = ET.SubElement(grp_hdr, 'CreDtTm')
            cre_dt_tm.text = datetime.now(timezone.utc).isoformat()
            
            # Notification
            ntfctn = ET.SubElement(bk_to_cstmr_dbt_cdt_ntfctn, 'Ntfctn')
            
            ntfctn_id = ET.SubElement(ntfctn, 'Id')
            ntfctn_id.text = f"NTF{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            cre_dt_tm_ntf = ET.SubElement(ntfctn, 'CreDtTm')
            cre_dt_tm_ntf.text = datetime.now(timezone.utc).isoformat()
            
            # Account
            acct = ET.SubElement(ntfctn, 'Acct')
            acct_id = ET.SubElement(acct, 'Id')
            iban = ET.SubElement(acct_id, 'IBAN')
            iban.text = notification_data.get('account_iban', 'GL89NVCT0000000000000001')
            
            acct_svcr = ET.SubElement(acct, 'Svcr')
            fin_instn_id = ET.SubElement(acct_svcr, 'FinInstnId')
            bic = ET.SubElement(fin_instn_id, 'BIC')
            bic.text = self.bank_bic
            
            # Entry
            ntry = ET.SubElement(ntfctn, 'Ntry')
            amt = ET.SubElement(ntry, 'Amt')
            amt.set('Ccy', notification_data.get('currency', 'USD'))
            amt.text = str(notification_data.get('amount', '0.00'))
            
            cdt_dbt_ind = ET.SubElement(ntry, 'CdtDbtInd')
            cdt_dbt_ind.text = notification_data.get('credit_debit_indicator', 'CRDT')  # CRDT or DBIT
            
            sts = ET.SubElement(ntry, 'Sts')
            sts.text = 'BOOK'  # Booked
            
            book_dt = ET.SubElement(ntry, 'BookgDt')
            dt = ET.SubElement(book_dt, 'Dt')
            dt.text = datetime.now().strftime('%Y-%m-%d')
            
            val_dt = ET.SubElement(ntry, 'ValDt')
            val_dt_dt = ET.SubElement(val_dt, 'Dt')
            val_dt_dt.text = datetime.now().strftime('%Y-%m-%d')
            
            return ET.tostring(doc, encoding='unicode')
            
        except Exception as e:
            logger.error(f"Error generating debit credit notification: {str(e)}")
            raise

    def generate_account_statement_iso20022(self, account_number: str, 
                                          transactions: List[Dict]) -> str:
        """Generate ISO 20022 account statement"""
        try:
            statement_id = f"STMT{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Calculate balance (simplified)
            balance = Decimal('0')
            for tx in transactions:
                if tx.get('type') == 'CRDT':
                    balance += Decimal(str(tx['amount']))
                else:
                    balance -= Decimal(str(tx['amount']))
            
            xml_statement = self.generator.generate_account_statement(
                account_number, statement_id, transactions, balance
            )
            
            logger.info(f"Generated ISO 20022 statement: {statement_id}")
            return xml_statement
            
        except Exception as e:
            logger.error(f"Error generating ISO 20022 statement: {str(e)}")
            raise

# Global service instance
iso20022_service = ISO20022Service()

def create_iso20022_payment_message(payment_data: Dict[str, Any]) -> str:
    """Convenience function to create ISO 20022 payment message"""
    return iso20022_service.create_outbound_payment(payment_data)

def process_iso20022_message(xml_content: str) -> Dict[str, Any]:
    """Convenience function to process ISO 20022 message"""
    return iso20022_service.process_inbound_message(xml_content)