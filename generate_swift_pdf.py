#!/usr/bin/env python3
"""
Generate PDF version of NVC Fund Bank SWIFT Documentation
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus.flowables import HRFlowable
from datetime import datetime

def create_swift_pdf():
    """Create comprehensive PDF documentation for NVC Fund Bank SWIFT structure"""
    
    # Create PDF document
    filename = "NVC_Fund_Bank_SWIFT_Documentation.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Get styles and create custom styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=HexColor('#061c38')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=HexColor('#ff6b35')
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
        textColor=HexColor('#061c38')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        textColor=black
    )
    
    # Build story (content)
    story = []
    
    # Title page
    story.append(Paragraph("NVC Fund Bank", title_style))
    story.append(Paragraph("Global SWIFT Structure Documentation", heading_style))
    story.append(Spacer(1, 20))
    
    # Institutional information
    story.append(Paragraph("Supranational Sovereign Institution", subheading_style))
    story.append(Paragraph("Under African Union Treaty Framework", body_style))
    story.append(Spacer(1, 30))
    
    # Date and version
    current_date = datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(f"Document Date: {current_date}", body_style))
    story.append(Paragraph("Version: 1.0 - Executive Edition", body_style))
    story.append(PageBreak())
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(HRFlowable(width="100%", thickness=2, color=HexColor('#ff6b35')))
    story.append(Spacer(1, 12))
    
    summary_text = """
    NVC Fund Bank operates as a supranational sovereign institution under the African Union Treaty framework, 
    providing comprehensive banking services through a strategic global SWIFT network. Our 15 sovereign SWIFT codes 
    ensure full compliance with ISO 20022 and ISO 9362:2022 standards while supporting advanced blockchain integration 
    through the NVCT stablecoin ecosystem.
    """
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 20))
    
    # Primary SWIFT Code
    story.append(Paragraph("Primary Global SWIFT Code", heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#ff6b35')))
    story.append(Spacer(1, 12))
    
    primary_data = [
        ['SWIFT Code', 'Institution', 'Authority'],
        ['NVCFGLXX', 'NVC Fund Bank - Global Operations', 'African Union Treaty Authority']
    ]
    
    primary_table = Table(primary_data, colWidths=[2*inch, 3*inch, 2.5*inch])
    primary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, black)
    ]))
    story.append(primary_table)
    story.append(Spacer(1, 20))
    
    # Regional SWIFT Codes
    story.append(Paragraph("Strategic Regional SWIFT Codes", heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#ff6b35')))
    story.append(Spacer(1, 12))
    
    # United States Operations
    story.append(Paragraph("United States Operations", subheading_style))
    us_data = [
        ['SWIFT Code', 'Location', 'Specialization'],
        ['NVCFUSNY', 'New York', 'USD operations and Federal Reserve relationships'],
        ['NVCFUSMI', 'Miami', 'Latin American correspondent banking hub']
    ]
    
    us_table = Table(us_data, colWidths=[2*inch, 2*inch, 3.5*inch])
    us_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, black)
    ]))
    story.append(us_table)
    story.append(Spacer(1, 15))
    
    # European Operations
    story.append(Paragraph("European Operations", subheading_style))
    eu_data = [
        ['SWIFT Code', 'Location', 'Specialization'],
        ['NVCFGBLX', 'Luxembourg', 'EU regulatory compliance and euro operations'],
        ['NVCFCHZU', 'Zurich', 'Swiss franc operations and wealth management'],
        ['NVCFFRPA', 'Paris', 'Euro zone institutional banking'],
        ['NVCFGBLO', 'London', 'UK financial markets and sterling operations']
    ]
    
    eu_table = Table(eu_data, colWidths=[2*inch, 2*inch, 3.5*inch])
    eu_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, black)
    ]))
    story.append(eu_table)
    story.append(Spacer(1, 15))
    
    # Asia-Pacific Operations
    story.append(Paragraph("Asia-Pacific Operations", subheading_style))
    ap_data = [
        ['SWIFT Code', 'Location', 'Specialization'],
        ['NVCFSGSI', 'Singapore', 'Asian financial hub and trade finance'],
        ['NVCFHKHO', 'Hong Kong', 'Chinese market access and trade corridors'],
        ['NVCFJPTO', 'Tokyo', 'Japanese yen operations and technology integration'],
        ['NVCFAUSY', 'Sydney', 'Australian dollar operations and mining finance']
    ]
    
    ap_table = Table(ap_data, colWidths=[2*inch, 2*inch, 3.5*inch])
    ap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, black)
    ]))
    story.append(ap_table)
    story.append(PageBreak())
    
    # African Operations
    story.append(Paragraph("African Operations", subheading_style))
    af_data = [
        ['SWIFT Code', 'Location', 'Specialization'],
        ['NVCFZAJO', 'Johannesburg', 'Southern African Development Community hub'],
        ['NVCFNGLA', 'Lagos', 'West African financial center and oil trade'],
        ['NVCFKENA', 'Nairobi', 'East African Community operations'],
        ['NVCFEGCA', 'Cairo', 'North African operations and Islamic banking']
    ]
    
    af_table = Table(af_data, colWidths=[2*inch, 2*inch, 3.5*inch])
    af_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, black)
    ]))
    story.append(af_table)
    story.append(Spacer(1, 20))
    
    # ISO Standards Compliance
    story.append(Paragraph("ISO Standards Compliance Framework", heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#ff6b35')))
    story.append(Spacer(1, 12))
    
    # ISO 9362:2022 section
    story.append(Paragraph("ISO 9362:2022 - Business Identifier Codes (BIC)", subheading_style))
    iso_text1 = """
    NVC Fund Bank's SWIFT codes fully comply with ISO 9362:2022 standards for Business Identifier Codes (BIC). 
    Our implementation includes:
    
    • BIC8 Format: Primary institutional codes (8 characters)
    • BIC11 Format: Extended branch and service codes (11 characters)  
    • Validation Standards: Full compliance with ISO checksum algorithms
    • Registry Management: Real-time SWIFT network integration
    """
    story.append(Paragraph(iso_text1, body_style))
    story.append(Spacer(1, 15))
    
    # ISO 20022 section
    story.append(Paragraph("ISO 20022 - Universal Financial Industry Message Scheme", subheading_style))
    iso_text2 = """
    Our platform supports all six major ISO 20022 message categories:
    
    • Customer Credit Transfer (pacs.008)
    • Financial Institution Credit Transfer (pacs.009)
    • Payment Return (pacs.004)
    • Payment Status Report (pacs.002)
    • Account Reporting (camt.053)
    • Liquidity Credit Transfer (camt.050)
    """
    story.append(Paragraph(iso_text2, body_style))
    story.append(Spacer(1, 20))
    
    # NVCT Integration
    story.append(Paragraph("NVCT Stablecoin Integration", heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#ff6b35')))
    story.append(Spacer(1, 12))
    
    nvct_text = """
    The NVC Token (NVCT) serves as our primary digital currency, fully integrated with traditional SWIFT messaging:
    
    • 1:1 USD Peg: Maintained through comprehensive reserve backing
    • ERC-20 Standard: Deployed on Ethereum blockchain for maximum compatibility
    • SWIFT Integration: Seamless conversion between NVCT and traditional currencies
    • Regulatory Compliance: Full AML/KYC integration across all jurisdictions
    • Treasury Backing: Supported by $10+ trillion in verified assets
    """
    story.append(Paragraph(nvct_text, body_style))
    story.append(Spacer(1, 20))
    
    # Footer
    story.append(Paragraph("Document Classification: Executive - Confidential", 
                          ParagraphStyle('Footer', parent=styles['Normal'], 
                                       fontSize=10, alignment=TA_CENTER,
                                       textColor=HexColor('#666666'))))
    
    # Build PDF
    doc.build(story)
    print(f"PDF created successfully: {filename}")
    return filename

if __name__ == "__main__":
    create_swift_pdf()