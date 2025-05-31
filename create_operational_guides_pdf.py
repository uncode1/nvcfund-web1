#!/usr/bin/env python3
"""
Create PDF versions of all operational guides and system documentation
Ensures consistency between HTML and PDF formats
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

def create_funds_transfer_guide_pdf():
    """Create PDF for NVC Funds Transfer Guide"""
    filename = "NVC_Funds_Transfer_Guide.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#061c38'),
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=15,
        spaceBefore=20,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold'
    )
    
    subsection_style = ParagraphStyle(
        'SubSection',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
        textColor=HexColor('#2c3e50'),
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    story = []
    
    # Logo and header
    story.append(Spacer(1, 0.5*inch))
    
    # Add logo with white background
    logo_path = 'static/nvc_fund_logo.png'
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2.5*inch, height=0.75*inch)
        logo_container = Table([[logo]], colWidths=[3*inch], rowHeights=[1*inch])
        logo_container.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(logo_container)
        story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("NVC FUND BANK", title_style))
    story.append(Paragraph("Funds Transfer Operations Guide", title_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Document info
    current_date = datetime.now().strftime("%B %d, %Y")
    info_data = [
        ['Document Type', 'Operational Guide'],
        ['Issue Date', current_date],
        ['Classification', 'Internal Use'],
        ['Version', '2.0 Professional Edition']
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(info_table)
    story.append(PageBreak())
    
    # Content sections
    story.append(Paragraph("Overview", section_style))
    story.append(Paragraph("""
    The NVC Fund Bank funds transfer system provides secure, efficient, and compliant 
    mechanisms for moving funds between accounts, institutions, and across borders. This 
    guide covers all operational procedures for processing fund transfers through our 
    multi-gateway payment infrastructure.
    """, body_style))
    
    story.append(Paragraph("Transfer Types", section_style))
    
    transfer_types = [
        ['Transfer Type', 'Processing Time', 'Fee Structure', 'Limits'],
        ['Internal Transfer', 'Instant', 'No Fee', 'Up to $50M'],
        ['Domestic Wire', '1-2 Business Days', '$25-50', 'Up to $10M'],
        ['International Wire', '2-5 Business Days', '$50-100', 'Up to $5M'],
        ['SWIFT Transfer', '1-3 Business Days', '$75-150', 'Up to $25M'],
        ['ACH Transfer', '1-3 Business Days', '$5-15', 'Up to $1M'],
        ['Correspondent Bank', '2-4 Business Days', 'Negotiated', 'Up to $100M']
    ]
    
    transfer_table = Table(transfer_types, colWidths=[1.5*inch, 1.3*inch, 1.2*inch, 1.2*inch])
    transfer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(transfer_table)
    
    story.append(Paragraph("Processing Procedures", section_style))
    story.append(Paragraph("1. Transaction Initiation", subsection_style))
    story.append(Paragraph("""
    All fund transfers must be properly authenticated and authorized before processing. 
    This includes verification of account ownership, available balances, and compliance 
    with applicable regulations.
    """, body_style))
    
    story.append(Paragraph("2. Risk Assessment", subsection_style))
    story.append(Paragraph("""
    Each transfer undergoes automated risk screening including AML checks, sanctions 
    screening, and fraud detection protocols before approval.
    """, body_style))
    
    story.append(Paragraph("3. Execution and Settlement", subsection_style))
    story.append(Paragraph("""
    Approved transfers are executed through the appropriate payment rail and tracked 
    through completion with full audit trail maintenance.
    """, body_style))
    
    # Build PDF
    doc.build(story)
    print(f"Funds Transfer Guide PDF created: {filename}")
    return filename

def create_server_integration_guide_pdf():
    """Create PDF for Server Integration Guide"""
    filename = "NVC_Server_Integration_Guide.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Use same styles as above
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#061c38'),
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=15,
        spaceBefore=20,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    story = []
    
    # Logo and header
    story.append(Spacer(1, 0.5*inch))
    
    # Add logo with white background
    logo_path = 'static/nvc_fund_logo.png'
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2.5*inch, height=0.75*inch)
        logo_container = Table([[logo]], colWidths=[3*inch], rowHeights=[1*inch])
        logo_container.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(logo_container)
        story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("NVC FUND BANK", title_style))
    story.append(Paragraph("Server-to-Server Integration Guide", title_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Content
    story.append(Paragraph("API Overview", section_style))
    story.append(Paragraph("""
    The NVC Fund Bank API provides comprehensive server-to-server integration capabilities 
    for financial institutions, payment processors, and enterprise clients. Our RESTful 
    API supports real-time transactions, account management, and reporting functions.
    """, body_style))
    
    story.append(Paragraph("Authentication", section_style))
    story.append(Paragraph("""
    API authentication uses industry-standard OAuth 2.0 with JWT tokens. All requests 
    must include proper authentication headers and are secured with TLS 1.3 encryption.
    """, body_style))
    
    story.append(Paragraph("Available Endpoints", section_style))
    
    # API endpoints table
    api_data = [
        ['Endpoint', 'Method', 'Purpose'],
        ['/api/v1/accounts', 'GET/POST', 'Account management'],
        ['/api/v1/transfers', 'POST', 'Initiate transfers'],
        ['/api/v1/transactions', 'GET', 'Transaction history'],
        ['/api/v1/exchange', 'GET/POST', 'Currency exchange'],
        ['/api/v1/balances', 'GET', 'Account balances'],
        ['/api/v1/notifications', 'GET', 'Status updates']
    ]
    
    api_table = Table(api_data, colWidths=[2.5*inch, 1*inch, 2*inch])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(api_table)
    
    # Build PDF
    doc.build(story)
    print(f"Server Integration Guide PDF created: {filename}")
    return filename

def create_transaction_settlement_pdf():
    """Create PDF for Transaction Settlement Guide"""
    filename = "NVC_Transaction_Settlement_Guide.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#061c38'),
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=15,
        spaceBefore=20,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    story = []
    
    # Logo and header
    story.append(Spacer(1, 0.5*inch))
    
    # Add logo with white background
    logo_path = 'static/nvc_fund_logo.png'
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2.5*inch, height=0.75*inch)
        logo_container = Table([[logo]], colWidths=[3*inch], rowHeights=[1*inch])
        logo_container.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(logo_container)
        story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("NVC FUND BANK", title_style))
    story.append(Paragraph("Transaction Settlement Explainer", title_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Content
    story.append(Paragraph("Settlement Overview", section_style))
    story.append(Paragraph("""
    Transaction settlement is the process of finalizing financial transactions between 
    parties. NVC Fund Bank operates a sophisticated settlement infrastructure that 
    handles multiple currencies, payment methods, and regulatory jurisdictions.
    """, body_style))
    
    story.append(Paragraph("Settlement Cycles", section_style))
    story.append(Paragraph("""
    Different transaction types follow specific settlement cycles based on payment 
    method, currency, and regulatory requirements. Real-time settlement is available 
    for internal transfers and select correspondent banking relationships.
    """, body_style))
    
    # Build PDF
    doc.build(story)
    print(f"Transaction Settlement Guide PDF created: {filename}")
    return filename

def create_tokenomics_guide_pdf():
    """Create PDF for NVCT Tokenomics Guide"""
    filename = "NVC_Tokenomics_Guide.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#061c38'),
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=15,
        spaceBefore=20,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    story = []
    
    # Logo and header
    story.append(Spacer(1, 0.5*inch))
    
    # Add logo with white background
    logo_path = 'static/nvc_fund_logo.png'
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2.5*inch, height=0.75*inch)
        logo_container = Table([[logo]], colWidths=[3*inch], rowHeights=[1*inch])
        logo_container.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(logo_container)
        story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("NVC FUND BANK", title_style))
    story.append(Paragraph("NVCT Tokenomics Guide", title_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Content
    story.append(Paragraph("NVCT Token Overview", section_style))
    story.append(Paragraph("""
    The NVC Token (NVCT) is a blockchain-based digital asset designed to facilitate 
    efficient, secure, and transparent financial transactions within the NVC Fund Bank 
    ecosystem. Built on Ethereum, NVCT maintains a 1:1 peg to the US Dollar through 
    comprehensive reserve backing.
    """, body_style))
    
    story.append(Paragraph("Token Economics", section_style))
    
    token_data = [
        ['Parameter', 'Value', 'Description'],
        ['Total Supply', '10 Billion NVCT', 'Maximum tokens that can exist'],
        ['USD Peg', '1:1 Ratio', 'Maintained through reserves'],
        ['Blockchain', 'Ethereum', 'ERC-20 standard compliance'],
        ['Backing', '100% Reserved', 'Full USD reserve backing'],
        ['Governance', 'Bank Controlled', 'Centralized management'],
        ['Use Cases', 'Payments & Settlement', 'Primary transaction medium']
    ]
    
    token_table = Table(token_data, colWidths=[1.5*inch, 1.5*inch, 2.5*inch])
    token_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(token_table)
    
    # Build PDF
    doc.build(story)
    print(f"NVCT Tokenomics Guide PDF created: {filename}")
    return filename

def main():
    """Generate all operational guide PDFs"""
    print("Generating operational guide PDFs...")
    
    # Create all PDF guides
    files_created = []
    files_created.append(create_funds_transfer_guide_pdf())
    files_created.append(create_server_integration_guide_pdf())
    files_created.append(create_transaction_settlement_pdf())
    files_created.append(create_tokenomics_guide_pdf())
    
    print("\nAll operational guide PDFs created successfully:")
    for file in files_created:
        print(f"- {file}")
    
    return files_created

if __name__ == "__main__":
    main()