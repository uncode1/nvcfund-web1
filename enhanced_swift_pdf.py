#!/usr/bin/env python3
"""
Enhanced Professional SWIFT Documentation PDF Generator
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus.flowables import HRFlowable
from datetime import datetime

def create_enhanced_swift_pdf():
    """Create enhanced professional SWIFT documentation"""
    
    filename = "NVC_Fund_Bank_SWIFT_Documentation_Enhanced.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=1*inch, bottomMargin=0.75*inch)
    
    # Enhanced professional styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'EnhancedTitle',
        parent=styles['Heading1'],
        fontSize=26,
        spaceAfter=30,
        spaceBefore=20,
        alignment=TA_CENTER,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'EnhancedSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        spaceBefore=10,
        alignment=TA_CENTER,
        textColor=HexColor('#ff6b35'),
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'EnhancedHeading',
        parent=styles['Heading2'],
        fontSize=15,
        spaceAfter=12,
        spaceBefore=20,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'EnhancedSubHeading',
        parent=styles['Heading3'],
        fontSize=13,
        spaceAfter=8,
        spaceBefore=15,
        textColor=HexColor('#ff6b35'),
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'EnhancedBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        spaceBefore=4,
        alignment=TA_JUSTIFY,
        textColor=black,
        fontName='Helvetica',
        leading=14
    )
    
    # Build content
    story = []
    
    # Professional Title Page
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("NVC FUND BANK", title_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Global SWIFT Structure Documentation", subtitle_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Institution badge
    badge_data = [
        ['SUPRANATIONAL SOVEREIGN INSTITUTION'],
        ['African Union Treaty Framework'],
        ['ISO 20022 & ISO 9362:2022 Compliant']
    ]
    
    badge_table = Table(badge_data, colWidths=[5*inch])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, -1), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 13),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 2, HexColor('#ff6b35'))
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Document metadata
    current_date = datetime.now().strftime("%B %d, %Y")
    meta_data = [
        ['Document Date:', current_date],
        ['Version:', '2.0 Enhanced Executive Edition'],
        ['Classification:', 'Executive Confidential'],
        ['Status:', 'Official Banking Documentation']
    ]
    
    meta_table = Table(meta_data, colWidths=[1.8*inch, 2.8*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#f8f9fa')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
    ]))
    story.append(meta_table)
    story.append(PageBreak())
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(HRFlowable(width="100%", thickness=2, color=HexColor('#ff6b35')))
    story.append(Spacer(1, 12))
    
    exec_text = """
    NVC Fund Bank operates as a supranational sovereign institution under the African Union Treaty framework, 
    providing comprehensive banking services through a strategically designed global SWIFT network. Our 15 sovereign 
    SWIFT codes ensure full compliance with ISO 20022 and ISO 9362:2022 international standards while supporting 
    advanced blockchain integration through the NVCT stablecoin ecosystem.
    
    As a treaty-backed sovereign institution, NVC Fund Bank maintains operational authority across multiple 
    jurisdictions while adhering to the highest international banking standards. Our global infrastructure 
    facilitates seamless international transactions and cross-border financial services.
    """
    story.append(Paragraph(exec_text, body_style))
    story.append(Spacer(1, 20))
    
    # Primary SWIFT Code
    story.append(Paragraph("Primary Global SWIFT Code", heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#ff6b35')))
    story.append(Spacer(1, 10))
    
    primary_data = [
        ['SWIFT Code', 'Institution', 'Authority', 'Status'],
        ['NVCFGLXX', 'NVC Fund Bank - Global Operations', 'African Union Treaty', 'Active Sovereign']
    ]
    
    primary_table = Table(primary_data, colWidths=[1.3*inch, 2.2*inch, 1.5*inch, 1.2*inch])
    primary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(primary_table)
    story.append(Spacer(1, 20))
    
    # Regional Operations
    story.append(Paragraph("Strategic Regional Operations", heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#ff6b35')))
    story.append(Spacer(1, 10))
    
    # United States
    story.append(Paragraph("United States Operations", subheading_style))
    us_data = [
        ['SWIFT Code', 'Location', 'Operational Focus'],
        ['NVCFUSNY', 'New York', 'USD operations and Federal Reserve relationships'],
        ['NVCFUSMI', 'Miami', 'Latin American correspondent banking hub']
    ]
    
    us_table = Table(us_data, colWidths=[1.3*inch, 1.3*inch, 3.6*inch])
    us_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ecf0f1')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#95a5a6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
    ]))
    story.append(us_table)
    story.append(Spacer(1, 15))
    
    # European Operations
    story.append(Paragraph("European Operations", subheading_style))
    eu_data = [
        ['SWIFT Code', 'Location', 'Operational Focus'],
        ['NVCFGBLX', 'Luxembourg', 'EU regulatory compliance and euro operations'],
        ['NVCFCHZU', 'Zurich', 'Swiss franc operations and wealth management'],
        ['NVCFFRPA', 'Paris', 'Euro zone institutional banking'],
        ['NVCFGBLO', 'London', 'UK financial markets and sterling operations']
    ]
    
    eu_table = Table(eu_data, colWidths=[1.3*inch, 1.3*inch, 3.6*inch])
    eu_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ecf0f1')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#95a5a6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
    ]))
    story.append(eu_table)
    story.append(Spacer(1, 15))
    
    # Asia-Pacific Operations
    story.append(Paragraph("Asia-Pacific Operations", subheading_style))
    ap_data = [
        ['SWIFT Code', 'Location', 'Operational Focus'],
        ['NVCFSGSI', 'Singapore', 'Asian financial hub and trade finance'],
        ['NVCFHKHO', 'Hong Kong', 'Chinese market access and trade corridors'],
        ['NVCFJPTO', 'Tokyo', 'Japanese yen operations and technology integration'],
        ['NVCFAUSY', 'Sydney', 'Australian dollar operations and mining finance']
    ]
    
    ap_table = Table(ap_data, colWidths=[1.3*inch, 1.3*inch, 3.6*inch])
    ap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ecf0f1')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#95a5a6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
    ]))
    story.append(ap_table)
    story.append(PageBreak())
    
    # African Operations
    story.append(Paragraph("African Operations", subheading_style))
    af_data = [
        ['SWIFT Code', 'Location', 'Operational Focus'],
        ['NVCFZAJO', 'Johannesburg', 'Southern African Development Community hub'],
        ['NVCFNGLA', 'Lagos', 'West African financial center and oil trade'],
        ['NVCFKENA', 'Nairobi', 'East African Community operations'],
        ['NVCFEGCA', 'Cairo', 'North African operations and Islamic banking']
    ]
    
    af_table = Table(af_data, colWidths=[1.3*inch, 1.3*inch, 3.6*inch])
    af_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ecf0f1')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#95a5a6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
    ]))
    story.append(af_table)
    story.append(Spacer(1, 20))
    
    # ISO Standards Compliance
    story.append(Paragraph("ISO Standards Compliance Framework", heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#ff6b35')))
    story.append(Spacer(1, 10))
    
    iso_text = """
    <b>ISO 9362:2022 - Business Identifier Codes (BIC)</b><br/>
    NVC Fund Bank's SWIFT codes fully comply with ISO 9362:2022 standards for Business Identifier Codes (BIC). 
    Our implementation includes BIC8 Format (Primary institutional codes), BIC11 Format (Extended branch codes), 
    Validation Standards (Full ISO checksum compliance), and Registry Management (Real-time SWIFT integration).
    
    <br/><br/><b>ISO 20022 - Universal Financial Industry Message Scheme</b><br/>
    Our platform supports all six major ISO 20022 message categories: Customer Credit Transfer (pacs.008), 
    Financial Institution Credit Transfer (pacs.009), Payment Return (pacs.004), Payment Status Report (pacs.002), 
    Account Reporting (camt.053), and Liquidity Credit Transfer (camt.050).
    """
    story.append(Paragraph(iso_text, body_style))
    story.append(Spacer(1, 20))
    
    # NVCT Integration
    story.append(Paragraph("NVCT Stablecoin Integration", heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#ff6b35')))
    story.append(Spacer(1, 10))
    
    nvct_text = """
    The NVC Token (NVCT) serves as our primary digital currency, fully integrated with traditional SWIFT messaging:
    
    • <b>1:1 USD Peg:</b> Maintained through comprehensive reserve backing
    • <b>ERC-20 Standard:</b> Deployed on Ethereum blockchain for maximum compatibility
    • <b>SWIFT Integration:</b> Seamless conversion between NVCT and traditional currencies
    • <b>Regulatory Compliance:</b> Full AML/KYC integration across all jurisdictions
    • <b>Treasury Backing:</b> Supported by $10+ trillion in verified assets
    """
    story.append(Paragraph(nvct_text, body_style))
    story.append(Spacer(1, 30))
    
    # Footer
    footer_text = """
    <i>This document contains confidential and proprietary information of NVC Fund Bank. 
    Distribution is restricted to authorized personnel only. 
    
    Document Classification: Executive Confidential
    © 2025 NVC Fund Bank - All Rights Reserved</i>
    """
    story.append(Paragraph(footer_text, 
                          ParagraphStyle('Footer', parent=styles['Normal'], 
                                       fontSize=9, alignment=TA_CENTER,
                                       textColor=HexColor('#666666'),
                                       spaceAfter=0)))
    
    # Build PDF
    doc.build(story)
    print(f"Enhanced professional PDF created: {filename}")
    return filename

if __name__ == "__main__":
    create_enhanced_swift_pdf()