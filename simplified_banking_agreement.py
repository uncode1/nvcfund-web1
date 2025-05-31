"""
Script to generate a simplified Correspondent Banking Agreement PDF for NVC Fund Bank.
This version uses continuous flow without forced page breaks.
"""

import os
from datetime import datetime
from fpdf import FPDF

class PDFWithPageNumbers(FPDF):
    """Custom PDF class with page numbers"""
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_correspondent_banking_agreement():
    """Generate a PDF for the NVC Fund Bank Correspondent Banking Agreement."""
    # Initialize PDF
    pdf = PDFWithPageNumbers()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Set document information
    pdf.set_title("NVC Fund Bank Correspondent Banking Agreement")
    pdf.set_author("NVC Fund Bank")
    
    # Add title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "CORRESPONDENT BANKING AGREEMENT", 0, 1, "C")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "NVC FUND BANK", 0, 1, "C")
    
    # Introduction
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "AGREEMENT", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "THIS CORRESPONDENT BANKING AGREEMENT (the \"Agreement\") is made and entered into as of the Effective Date set forth below, by and between:")
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, "NVC Fund Bank", 0, 1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "a Supranational Sovereign Financial Institution established under the African Union Treaty framework with SWIFT code NVCFBKAU and ACH Routing Number 031176110, (hereinafter referred to as \"NVC Fund Bank\")")
    
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, "AND", 0, 1, "C")
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, "[RESPONDENT BANK NAME]", 0, 1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "a [type of institution] organized and existing under the laws of [jurisdiction], with its principal place of business at [address], with SWIFT code [SWIFT code] (hereinafter referred to as the \"Respondent Bank\")")
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "(each a \"Party\" and collectively the \"Parties\").")
    
    # Recitals
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "RECITALS", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "WHEREAS, NVC Fund Bank is a Supranational Sovereign Financial Institution with over $10 trillion in balance sheet assets and maintains a global settlement infrastructure for facilitating cross-border payments, currency exchanges, and other financial services;")
    
    pdf.multi_cell(0, 6, "WHEREAS, NVC Fund Bank has established a proprietary settlement system utilizing its NVC Token Stablecoin (NVCT) as the native currency for transactions, which maintains a 1:1 USD peg and is fully backed by cash and cash equivalent assets;")
    
    pdf.multi_cell(0, 6, "WHEREAS, the Respondent Bank wishes to establish a correspondent banking relationship with NVC Fund Bank to access its settlement infrastructure, services, and global payment capabilities;")
    
    pdf.multi_cell(0, 6, "WHEREAS, the Parties wish to set forth the terms and conditions governing their correspondent banking relationship;")
    
    pdf.multi_cell(0, 6, "NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein, and for other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the Parties hereby agree as follows:")
    
    # Definitions
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. DEFINITIONS", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "In this Agreement, unless the context otherwise requires, the following terms shall have the following meanings:")
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(60, 6, "\"Applicable Law\"", 0, 0)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "means all laws, regulations, rules, orders, directives, guidelines, and standards applicable to the Parties and the services provided under this Agreement, including but not limited to banking, anti-money laundering, counter-terrorism financing, and sanctions laws.")
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(60, 6, "\"Business Day\"", 0, 0)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "means a day (other than a Saturday, Sunday, or public holiday) on which banks are open for general business in the respective jurisdictions of the Parties.")
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(60, 6, "\"Confidential Information\"", 0, 0)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "means any information, whether in written, oral, electronic, or other form, that is designated as confidential or that reasonably should be understood to be confidential given the nature of the information and the circumstances of disclosure.")
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(60, 6, "\"Correspondent Account\"", 0, 0)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "means the account(s) established by NVC Fund Bank for the Respondent Bank pursuant to this Agreement.")
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(60, 6, "\"Effective Date\"", 0, 0)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "means the date on which this Agreement is executed by both Parties.")
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(60, 6, "\"NVCT\"", 0, 0)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "means the NVC Token Stablecoin, a digital currency issued by NVC Fund Bank with a 1:1 USD peg and fully backed by cash and cash equivalent assets.")
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(60, 6, "\"Services\"", 0, 0)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "means the correspondent banking services to be provided by NVC Fund Bank to the Respondent Bank as set forth in this Agreement.")
    
    # Scope of Services
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. SCOPE OF SERVICES", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "2.1 NVC Fund Bank shall provide the following Services to the Respondent Bank:")
    
    # Services list
    bullet = chr(127)
    pdf.cell(10, 6, bullet, 0, 0)
    pdf.multi_cell(0, 6, "Maintenance of a Correspondent Account for the Respondent Bank in one or more of the following currencies: USD, EUR, GBP, NVCT, AFD1, SFN, and other currencies as mutually agreed upon.")
    
    pdf.cell(10, 6, bullet, 0, 0)
    pdf.multi_cell(0, 6, "Processing of international wire transfers through SWIFT messaging (MT103, MT202, MT760, etc.)")
    
    pdf.cell(10, 6, bullet, 0, 0)
    pdf.multi_cell(0, 6, "Facilitation of foreign exchange transactions at competitive rates.")
    
    pdf.cell(10, 6, bullet, 0, 0)
    pdf.multi_cell(0, 6, "Access to the NVC Fund Bank settlement system for real-time gross settlement (RTGS) capabilities.")
    
    pdf.cell(10, 6, bullet, 0, 0)
    pdf.multi_cell(0, 6, "Issuance and redemption of NVCT for settlement purposes.")
    
    pdf.cell(10, 6, bullet, 0, 0)
    pdf.multi_cell(0, 6, "Access to NVC Fund Bank's global payment network.")
    
    pdf.cell(10, 6, bullet, 0, 0)
    pdf.multi_cell(0, 6, "Cash management services.")
    
    pdf.cell(10, 6, bullet, 0, 0)
    pdf.multi_cell(0, 6, "Trade finance services, including letters of credit.")
    
    pdf.cell(10, 6, bullet, 0, 0)
    pdf.multi_cell(0, 6, "Such other services as the Parties may agree upon in writing from time to time.")
    
    pdf.multi_cell(0, 6, "2.2 The Respondent Bank shall provide NVC Fund Bank with all necessary information and documentation required for the provision of the Services, including but not limited to customer identification, transaction details, and regulatory reporting information.")
    
    pdf.multi_cell(0, 6, "2.3 The Parties agree to cooperate with each other in good faith to ensure the efficient provision of the Services in accordance with this Agreement and Applicable Law.")
    
    # Account Opening and Operation
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "3. ACCOUNT OPENING AND OPERATION", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "3.1 NVC Fund Bank shall open and maintain a Correspondent Account for the Respondent Bank in accordance with its standard account opening procedures and subject to satisfactory completion of all required due diligence.")
    
    pdf.multi_cell(0, 6, "3.2 The Correspondent Account shall be operated in accordance with the terms and conditions set forth in this Agreement and the applicable account documentation provided by NVC Fund Bank.")
    
    pdf.multi_cell(0, 6, "3.3 The Respondent Bank shall provide NVC Fund Bank with a list of authorized signatories and any specific instructions for the operation of the Correspondent Account.")
    
    pdf.multi_cell(0, 6, "3.4 The Respondent Bank shall maintain sufficient funds in the Correspondent Account to cover all transactions and fees associated with the Services.")
    
    pdf.multi_cell(0, 6, "3.5 NVC Fund Bank shall provide the Respondent Bank with periodic account statements and transaction confirmations in accordance with its standard practices or as otherwise agreed by the Parties.")
    
    # Fees and Charges
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "4. FEES AND CHARGES", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "4.1 The Respondent Bank shall pay NVC Fund Bank the fees and charges for the Services as set forth in Schedule A attached hereto, which may be amended from time to time by mutual agreement of the Parties.")
    
    pdf.multi_cell(0, 6, "4.2 NVC Fund Bank shall have the right to debit the Correspondent Account for any fees, charges, or other amounts owed by the Respondent Bank under this Agreement.")
    
    pdf.multi_cell(0, 6, "4.3 All fees and charges are exclusive of any applicable taxes, which shall be borne by the Respondent Bank.")
    
    pdf.multi_cell(0, 6, "4.4 In addition to the fees and charges set forth in Schedule A, the Respondent Bank shall reimburse NVC Fund Bank for any out-of-pocket expenses incurred in connection with the provision of the Services, including but not limited to telecommunications, postage, and courier charges.")
    
    # Compliance and AML Requirements
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "5. COMPLIANCE AND AML REQUIREMENTS", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "5.1 Each Party shall comply with all Applicable Law in the performance of its obligations under this Agreement, including but not limited to laws and regulations relating to anti-money laundering, counter-terrorism financing, sanctions, and data protection.")
    
    pdf.multi_cell(0, 6, "5.2 The Respondent Bank shall implement and maintain adequate policies, procedures, and controls to ensure compliance with Applicable Law, including but not limited to customer due diligence, transaction monitoring, and suspicious activity reporting.")
    
    pdf.multi_cell(0, 6, "5.3 The Respondent Bank shall provide NVC Fund Bank with such information and documentation as NVC Fund Bank may reasonably request to fulfill its compliance obligations under Applicable Law.")
    
    pdf.multi_cell(0, 6, "5.4 Each Party shall promptly notify the other Party of any material changes in its compliance policies, procedures, or controls that may affect the provision of the Services under this Agreement.")
    
    pdf.multi_cell(0, 6, "5.5 NVC Fund Bank may refuse to process any transaction that it reasonably believes may violate Applicable Law or its internal policies and procedures.")
    
    pdf.multi_cell(0, 6, "5.6 Each Party shall notify the other promptly if it becomes aware of any actual or suspected breach of Applicable Law in connection with the Services or this Agreement.")
    
    # Term and Termination
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "6. TERM AND TERMINATION", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "6.1 This Agreement shall commence on the Effective Date and shall continue until terminated in accordance with this Section 6.")
    
    pdf.multi_cell(0, 6, "6.2 Either Party may terminate this Agreement without cause by giving the other Party ninety (90) days' prior written notice.")
    
    pdf.multi_cell(0, 6, "6.3 Either Party may terminate this Agreement with immediate effect by giving written notice to the other Party if:")
    
    pdf.cell(10, 6, "a)", 0, 0)
    pdf.multi_cell(0, 6, "The other Party commits a material breach of this Agreement and, in the case of a breach capable of remedy, fails to remedy such breach within thirty (30) days after receiving written notice to do so;")
    
    pdf.cell(10, 6, "b)", 0, 0)
    pdf.multi_cell(0, 6, "The other Party becomes insolvent, is placed under administration or receivership, or undergoes any similar event;")
    
    pdf.cell(10, 6, "c)", 0, 0)
    pdf.multi_cell(0, 6, "The other Party's banking license is revoked or suspended;")
    
    pdf.cell(10, 6, "d)", 0, 0)
    pdf.multi_cell(0, 6, "The other Party is subject to sanctions or enforcement actions by a regulatory authority;")
    
    pdf.cell(10, 6, "e)", 0, 0)
    pdf.multi_cell(0, 6, "Continuation of the Agreement would cause either Party to violate Applicable Law.")
    
    pdf.multi_cell(0, 6, "6.4 Upon termination of this Agreement:")
    
    pdf.cell(10, 6, "a)", 0, 0)
    pdf.multi_cell(0, 6, "NVC Fund Bank shall prepare a final account statement and settle the Correspondent Account in accordance with the Respondent Bank's instructions, subject to any applicable legal or regulatory restrictions;")
    
    pdf.cell(10, 6, "b)", 0, 0)
    pdf.multi_cell(0, 6, "Each Party shall return or destroy all Confidential Information of the other Party in its possession, except as required to be retained by Applicable Law;")
    
    pdf.cell(10, 6, "c)", 0, 0)
    pdf.multi_cell(0, 6, "All outstanding obligations of the Parties shall be performed or discharged;")
    
    pdf.cell(10, 6, "d)", 0, 0)
    pdf.multi_cell(0, 6, "Any accrued rights, obligations, or liabilities of the Parties shall not be affected.")
    
    pdf.multi_cell(0, 6, "6.5 The provisions of Sections 5 (Compliance and AML Requirements), 7 (Confidentiality), 8 (Data Protection), 9 (Liability and Indemnification), and 12 (Governing Law and Dispute Resolution) shall survive the termination of this Agreement.")
    
    # Additional Sections (summarized for brevity)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "7. CONFIDENTIALITY", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "7.1 Each Party shall maintain the confidentiality of all Confidential Information of the other Party and shall not disclose such Confidential Information to any third party except as required by Applicable Law or with the prior written consent of the disclosing Party.")
    
    pdf.multi_cell(0, 6, "7.2 Each Party shall use the Confidential Information of the other Party solely for the purpose of performing its obligations under this Agreement.")
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "8. DATA PROTECTION", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "8.1 Each Party shall comply with all applicable data protection laws and regulations in the performance of its obligations under this Agreement.")
    
    pdf.multi_cell(0, 6, "8.2 Each Party shall implement appropriate technical and organizational measures to protect personal data processed in connection with this Agreement.")
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "9. LIABILITY AND INDEMNIFICATION", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "9.1 Each Party shall indemnify and hold harmless the other Party from and against any and all losses, damages, claims, liabilities, costs, and expenses (including reasonable attorneys' fees) arising from or in connection with any breach of this Agreement by the indemnifying Party or its negligence or willful misconduct.")
    
    pdf.multi_cell(0, 6, "9.2 Neither Party shall be liable to the other Party for any indirect, special, incidental, consequential, or punitive damages arising out of or in connection with this Agreement, whether based on contract, tort, or any other legal theory.")
    
    pdf.multi_cell(0, 6, "9.3 NVC Fund Bank's liability to the Respondent Bank under this Agreement shall be limited to the amount of fees paid by the Respondent Bank to NVC Fund Bank during the twelve (12) months preceding the event giving rise to such liability.")
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "10. FORCE MAJEURE", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "10.1 Neither Party shall be liable for any delay or failure to perform its obligations under this Agreement to the extent that such delay or failure is caused by events beyond its reasonable control, including but not limited to acts of God, natural disasters, war, terrorism, riots, civil unrest, government actions, power failures, or telecommunications failures.")
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "11. NOTICES", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "11.1 All notices and other communications under this Agreement shall be in writing and shall be delivered by hand, by courier, by registered mail, or by email to the addresses set forth below or to such other addresses as may be designated by the Parties in writing.")
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "12. GOVERNING LAW AND DISPUTE RESOLUTION", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "12.1 This Agreement shall be governed by and construed in accordance with the laws of [jurisdiction], without giving effect to any choice of law or conflict of law provisions.")
    
    pdf.multi_cell(0, 6, "12.2 Any dispute, controversy, or claim arising out of or in connection with this Agreement, or the breach, termination, or invalidity thereof, shall be finally settled by arbitration in accordance with the Rules of the International Chamber of Commerce by one or more arbitrators appointed in accordance with the said Rules. The place of arbitration shall be [city, country]. The language of the arbitration shall be English.")
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "13. MISCELLANEOUS", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, "13.1 This Agreement constitutes the entire agreement between the Parties with respect to the subject matter hereof and supersedes all prior or contemporaneous agreements, understandings, or representations, whether oral or written.")
    
    pdf.multi_cell(0, 6, "13.2 This Agreement may not be amended or modified except by a written instrument signed by both Parties.")
    
    pdf.multi_cell(0, 6, "13.3 Neither Party may assign this Agreement or any of its rights or obligations hereunder without the prior written consent of the other Party.")
    
    pdf.multi_cell(0, 6, "13.4 If any provision of this Agreement is found to be invalid or unenforceable, the remaining provisions shall remain in full force and effect.")
    
    pdf.multi_cell(0, 6, "13.5 The failure of either Party to enforce any right or provision of this Agreement shall not constitute a waiver of such right or provision.")
    
    pdf.multi_cell(0, 6, "13.6 This Agreement may be executed in counterparts, each of which shall be deemed an original, but all of which together shall constitute one and the same instrument.")
    
    # Signature Block
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "IN WITNESS WHEREOF, the Parties have executed this Agreement as of the Effective Date.", 0, 1)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(90, 6, "NVC FUND BANK", 0, 0)
    pdf.cell(90, 6, "RESPONDENT BANK", 0, 1)
    
    pdf.cell(90, 6, "By: ________________________", 0, 0)
    pdf.cell(90, 6, "By: ________________________", 0, 1)
    
    pdf.cell(90, 6, "Name: _____________________", 0, 0)
    pdf.cell(90, 6, "Name: _____________________", 0, 1)
    
    pdf.cell(90, 6, "Title: ______________________", 0, 0)
    pdf.cell(90, 6, "Title: ______________________", 0, 1)
    
    pdf.cell(90, 6, "Date: ______________________", 0, 0)
    pdf.cell(90, 6, "Date: ______________________", 0, 1)
    
    # Create the directory if it doesn't exist
    os.makedirs("static/documents", exist_ok=True)
    
    # Save the PDF
    pdf_path = "static/documents/NVC_Fund_Bank_Correspondent_Banking_Agreement.pdf"
    pdf.output(pdf_path)
    
    print(f"Correspondent Banking Agreement PDF generated at {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    generate_correspondent_banking_agreement()