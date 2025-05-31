#!/usr/bin/env python3
"""
Final Professional SWIFT Documentation with Guaranteed Working Design
"""
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

def create_final_swift_pdf():
    """Create the final professional SWIFT documentation"""
    
    filename = "NVC_Fund_Bank_SWIFT_Documentation_Final.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.5*inch, bottomMargin=0.75*inch)
    
    # Professional styles
    styles = getSampleStyleSheet()
    
    # Cover page title
    cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Title'],
        fontSize=36,
        spaceAfter=30,
        spaceBefore=40,
        alignment=TA_CENTER,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold'
    )
    
    # Cover subtitle
    cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=25,
        spaceBefore=20,
        alignment=TA_CENTER,
        textColor=HexColor('#ff6b35'),
        fontName='Helvetica-Bold'
    )
    
    # Section headers
    section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=20,
        spaceBefore=30,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold',
        alignment=TA_CENTER
    )
    
    # Body text
    body_text = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        spaceBefore=6,
        alignment=TA_JUSTIFY,
        textColor=black,
        fontName='Helvetica',
        leading=15
    )
    
    # Build content
    story = []
    
    # PROFESSIONAL COVER PAGE
    story.append(Spacer(1, 0.5*inch))
    
    # Main title
    story.append(Paragraph("NVC FUND BANK", cover_title))
    story.append(Spacer(1, 0.2*inch))
    
    # Subtitle
    story.append(Paragraph("Global SWIFT Structure", cover_subtitle))
    story.append(Paragraph("Executive Documentation", cover_subtitle))
    story.append(Spacer(1, 0.4*inch))
    
    # Professional institutional information table
    cover_info_data = [
        ['INSTITUTIONAL CLASSIFICATION', 'DETAILS'],
        ['Institution Type', 'Supranational Sovereign Bank'],
        ['Legal Authority', 'African Union Treaty Framework'],
        ['Primary SWIFT Code', 'NVCFGLXX (Global Operations)'],
        ['Total Assets', '$10+ Trillion USD'],
        ['Market Cap', '$1+ Trillion USD'],
        ['Annual Revenue', '$289 Billion USD'],
        ['ISO Compliance', '20022 & 9362:2022 Certified'],
        ['Global Presence', '15 Strategic SWIFT Codes'],
        ['Blockchain Integration', 'NVCT Stablecoin Ready']
    ]
    
    cover_table = Table(cover_info_data, colWidths=[2.5*inch, 3.5*inch])
    cover_table.setStyle(TableStyle([
        # Header row styling
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        
        # Data rows styling
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2c3e50')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        
        # General styling
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 2, HexColor('#ff6b35')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12)
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Document metadata
    current_date = datetime.now().strftime("%B %d, %Y")
    metadata_data = [
        ['Document Date', current_date],
        ['Version', '5.0 Final Professional Edition'],
        ['Classification', 'Executive Confidential'],
        ['Prepared For', 'Banking Regulators & Executive Partnerships'],
        ['Geographic Scope', 'Global Multi-Jurisdictional Operations']
    ]
    
    metadata_table = Table(metadata_data, colWidths=[2.2*inch, 3.8*inch])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#34495e')),
        ('BACKGROUND', (1, 0), (1, -1), white),
        ('TEXTCOLOR', (0, 0), (0, -1), white),
        ('TEXTCOLOR', (1, 0), (1, -1), HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(metadata_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Legal footer
    footer_text = """
    <b>CONFIDENTIAL EXECUTIVE DOCUMENT</b><br/>
    This document contains proprietary information of NVC Fund Bank, operating under 
    African Union Treaty authority. Distribution restricted to authorized personnel only.
    <br/><br/>© 2025 NVC Fund Bank - All Rights Reserved
    """
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=HexColor('#7f8c8d'),
        fontName='Helvetica-Oblique'
    )
    story.append(Paragraph(footer_text, footer_style))
    story.append(PageBreak())
    
    # EXECUTIVE SUMMARY PAGE
    story.append(Paragraph("EXECUTIVE SUMMARY", section_header))
    story.append(Spacer(1, 20))
    
    summary_text = """
    <b>NVC Fund Bank</b> operates as a supranational sovereign institution under the African Union Treaty 
    framework, managing over <b>$10 trillion</b> in assets across global markets. Our comprehensive SWIFT 
    network consists of <b>15 strategic codes</b> positioned across four continents, ensuring seamless 
    international banking operations while maintaining full compliance with ISO 20022 and ISO 9362:2022 standards.
    
    <br/><br/>Our primary SWIFT code <b>NVCFGLXX</b> serves as the global identifier for our sovereign banking 
    operations, facilitating correspondent banking relationships and cross-border institutional transactions. 
    The institution's annual revenue of <b>$289 billion</b> reflects our significant role in international 
    finance and our commitment to providing world-class banking services.
    
    <br/><br/>This documentation provides comprehensive details of our global SWIFT infrastructure, regulatory 
    compliance framework, and operational capabilities across all jurisdictions where we maintain banking 
    relationships and sovereign authority.
    """
    story.append(Paragraph(summary_text, body_text))
    story.append(PageBreak())
    
    # PRIMARY SWIFT CODE SECTION
    story.append(Paragraph("PRIMARY GLOBAL SWIFT CODE", section_header))
    story.append(Spacer(1, 20))
    
    primary_text = """
    The primary SWIFT code <b>NVCFGLXX</b> represents NVC Fund Bank's global sovereign authority 
    and serves as our principal identifier for international banking operations, correspondent 
    relationships, and cross-border financial services.
    """
    story.append(Paragraph(primary_text, body_text))
    story.append(Spacer(1, 15))
    
    # Primary SWIFT table
    primary_data = [
        ['SWIFT CODE', 'INSTITUTION NAME', 'AUTHORITY', 'STATUS'],
        ['NVCFGLXX', 'NVC Fund Bank - Global Operations', 'African Union Treaty', 'Active Sovereign']
    ]
    
    primary_table = Table(primary_data, colWidths=[1.5*inch, 2.5*inch, 1.8*inch, 1.2*inch])
    primary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#e8f4f8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('TEXTCOLOR', (0, 1), (-1, 1), HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, 1), 11),
        ('GRID', (0, 0), (-1, -1), 2, HexColor('#ff6b35')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12)
    ]))
    story.append(primary_table)
    story.append(Spacer(1, 30))
    
    # REGIONAL OPERATIONS
    story.append(Paragraph("REGIONAL SWIFT OPERATIONS", section_header))
    story.append(Spacer(1, 20))
    
    regional_text = """
    NVC Fund Bank maintains strategic regional presence through specialized SWIFT codes 
    positioned across key financial centers and jurisdictions worldwide.
    """
    story.append(Paragraph(regional_text, body_text))
    story.append(Spacer(1, 15))
    
    # Regional SWIFT codes table
    regional_data = [
        ['REGION', 'SWIFT CODE', 'LOCATION', 'SPECIALIZATION'],
        ['North America', 'NVCFUSXX', 'United States Operations', 'Correspondent Banking'],
        ['Europe', 'NVCFGBXX', 'United Kingdom Hub', 'European Markets'],
        ['Asia Pacific', 'NVCFSGXX', 'Singapore Center', 'Asian Operations'],
        ['Australia', 'NVCFAUXX', 'Australian Division', 'Pacific Region'],
        ['Middle East', 'NVCFAEXX', 'UAE Operations', 'MENA Markets'],
        ['Africa', 'NVCFZAXX', 'South African Hub', 'Continental Operations']
    ]
    
    regional_table = Table(regional_data, colWidths=[1.8*inch, 1.3*inch, 1.9*inch, 1.8*inch])
    regional_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(regional_table)
    
    # Build the PDF
    doc.build(story)
    print(f"Final professional PDF created: {filename}")
    return filename

if __name__ == "__main__":
    create_final_swift_pdf()