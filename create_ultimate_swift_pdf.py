#!/usr/bin/env python3
"""
Ultimate Professional SWIFT Documentation with Perfect Layout
"""
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from datetime import datetime

def create_ultimate_swift_pdf():
    """Create the ultimate professional SWIFT documentation with perfect layout"""
    
    filename = "NVC_Fund_Bank_SWIFT_Documentation_Ultimate.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Enhanced professional styles
    styles = getSampleStyleSheet()
    
    # Cover page main title - large and bold
    main_title = ParagraphStyle(
        'MainTitle',
        parent=styles['Title'],
        fontSize=42,
        spaceAfter=20,
        spaceBefore=30,
        alignment=TA_CENTER,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold',
        leading=45
    )
    
    # Cover page subtitle - prominent but smaller
    subtitle = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading1'],
        fontSize=26,
        spaceAfter=15,
        spaceBefore=10,
        alignment=TA_CENTER,
        textColor=HexColor('#ff6b35'),
        fontName='Helvetica-Bold',
        leading=30
    )
    
    # Institution description
    institution_desc = ParagraphStyle(
        'InstitutionDesc',
        parent=styles['Normal'],
        fontSize=16,
        spaceAfter=25,
        spaceBefore=15,
        alignment=TA_CENTER,
        textColor=HexColor('#2c3e50'),
        fontName='Helvetica-Bold'
    )
    
    # Section headers - professional and prominent
    section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=25,
        spaceBefore=35,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        borderWidth=2,
        borderColor=HexColor('#ff6b35'),
        borderPadding=12,
        backColor=HexColor('#f8f9fa')
    )
    
    # Body text - clear and readable
    body_text = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=15,
        spaceBefore=8,
        alignment=TA_JUSTIFY,
        textColor=HexColor('#2c3e50'),
        fontName='Helvetica',
        leading=16
    )
    
    # Highlighted text for important information
    highlight_text = ParagraphStyle(
        'HighlightText',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=20,
        spaceBefore=15,
        alignment=TA_CENTER,
        textColor=HexColor('#ff6b35'),
        fontName='Helvetica-Bold',
        backColor=HexColor('#f8f9fa'),
        borderWidth=1,
        borderColor=HexColor('#ff6b35'),
        borderPadding=10
    )
    
    # Build content
    story = []
    
    # === PROFESSIONAL COVER PAGE ===
    story.append(Spacer(1, 0.3*inch))
    
    # Main institutional title
    story.append(Paragraph("NVC FUND BANK", main_title))
    story.append(Spacer(1, 0.1*inch))
    
    # Professional divider line
    divider_table = Table([['']], colWidths=[6*inch], rowHeights=[0.05*inch])
    divider_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#ff6b35')),
        ('GRID', (0, 0), (-1, -1), 0, white)
    ]))
    story.append(divider_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Document title
    story.append(Paragraph("Global SWIFT Structure", subtitle))
    story.append(Paragraph("Executive Documentation", subtitle))
    story.append(Spacer(1, 0.3*inch))
    
    # Institutional authority
    story.append(Paragraph("Supranational Sovereign Institution", institution_desc))
    story.append(Paragraph("Under African Union Treaty Framework", institution_desc))
    story.append(Spacer(1, 0.4*inch))
    
    # Executive summary box with key metrics
    key_metrics_data = [
        ['INSTITUTIONAL OVERVIEW', ''],
        ['Total Assets Under Management', '$10+ Trillion USD'],
        ['Market Capitalization', '$1+ Trillion USD'],
        ['Annual Revenue', '$289 Billion USD'],
        ['Global SWIFT Codes', '15 Strategic Locations'],
        ['ISO Standards Compliance', '20022 & 9362:2022 Certified'],
        ['Primary Operations Code', 'NVCFGLXX (Global Authority)'],
        ['Blockchain Integration', 'NVCT Stablecoin Ready']
    ]
    
    metrics_table = Table(key_metrics_data, colWidths=[3*inch, 3*inch])
    metrics_table.setStyle(TableStyle([
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('SPAN', (0, 0), (1, 0)),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Data styling
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2c3e50')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        
        # General formatting
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1.5, HexColor('#dee2e6')),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15)
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Document metadata in professional format
    current_date = datetime.now().strftime("%B %d, %Y")
    metadata_data = [
        ['DOCUMENT INFORMATION', ''],
        ['Issue Date', current_date],
        ['Version', '6.0 Ultimate Professional Edition'],
        ['Classification', 'Executive Confidential'],
        ['Distribution', 'Banking Regulators & Executive Partners'],
        ['Geographic Scope', 'Global Multi-Jurisdictional Operations'],
        ['Issuing Authority', 'NVC Fund Bank Treaty Operations']
    ]
    
    metadata_table = Table(metadata_data, colWidths=[2.5*inch, 3.5*inch])
    metadata_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('SPAN', (0, 0), (1, 0)),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Data
        ('BACKGROUND', (0, 1), (-1, -1), white),
        ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2c3e50')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12)
    ]))
    story.append(metadata_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Legal footer with proper formatting
    footer_text = """
    <para alignment="center">
    <b>CONFIDENTIAL & PROPRIETARY DOCUMENT</b><br/>
    This document contains confidential and proprietary information of NVC Fund Bank, 
    a supranational sovereign institution operating under African Union Treaty authority. 
    Distribution is strictly restricted to authorized executive personnel, regulatory authorities, 
    and approved institutional partners only.
    <br/><br/>
    <i>© 2025 NVC Fund Bank - All Rights Reserved | African Union Treaty Framework</i>
    </para>
    """
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=HexColor('#7f8c8d'),
        fontName='Helvetica',
        borderWidth=1,
        borderColor=HexColor('#bdc3c7'),
        borderPadding=12,
        backColor=HexColor('#f8f9fa')
    )
    story.append(Paragraph(footer_text, footer_style))
    story.append(PageBreak())
    
    # === EXECUTIVE SUMMARY PAGE ===
    story.append(Paragraph("EXECUTIVE SUMMARY", section_header))
    story.append(Spacer(1, 25))
    
    # Enhanced executive summary with better formatting
    summary_paragraphs = [
        """<b>NVC Fund Bank</b> operates as a premier supranational sovereign institution under the comprehensive authority of the African Union Treaty framework. With over <b>$10 trillion</b> in assets under management and annual revenue exceeding <b>$289 billion</b>, we represent one of the world's largest financial institutions.""",
        
        """Our sophisticated global banking infrastructure spans <b>four continents</b> through <b>fifteen strategically positioned SWIFT codes</b>, ensuring seamless international banking operations while maintaining full compliance with ISO 20022 and ISO 9362:2022 international standards.""",
        
        """The primary SWIFT code <b>NVCFGLXX</b> serves as our global sovereign identifier, facilitating complex correspondent banking relationships, cross-border institutional transactions, and international financial services for governments, central banks, and major financial institutions worldwide.""",
        
        """Our advanced blockchain integration through the <b>NVCT stablecoin ecosystem</b> positions NVC Fund Bank at the forefront of digital banking innovation, bridging traditional sovereign banking with next-generation financial technology."""
    ]
    
    for para in summary_paragraphs:
        story.append(Paragraph(para, body_text))
        story.append(Spacer(1, 15))
    
    story.append(PageBreak())
    
    # === PRIMARY SWIFT CODE SECTION ===
    story.append(Paragraph("PRIMARY GLOBAL SWIFT OPERATIONS", section_header))
    story.append(Spacer(1, 25))
    
    story.append(Paragraph("Global Sovereign Authority Code", highlight_text))
    story.append(Spacer(1, 15))
    
    primary_description = """
    The primary SWIFT identifier <b>NVCFGLXX</b> represents NVC Fund Bank's supranational sovereign 
    authority and serves as our principal code for all international banking operations, correspondent 
    banking relationships, and cross-border institutional financial services across global markets.
    """
    story.append(Paragraph(primary_description, body_text))
    story.append(Spacer(1, 20))
    
    # Primary SWIFT table with better formatting
    primary_data = [
        ['SWIFT CODE', 'INSTITUTION DESIGNATION', 'SOVEREIGN AUTHORITY', 'OPERATIONAL STATUS'],
        ['NVCFGLXX', 'NVC Fund Bank\nGlobal Operations Center', 'African Union Treaty\nFramework Authority', 'Active Sovereign\nInstitution']
    ]
    
    primary_table = Table(primary_data, colWidths=[1.4*inch, 2.4*inch, 1.8*inch, 1.4*inch])
    primary_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Data
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#e8f4f8')),
        ('TEXTCOLOR', (0, 1), (-1, 1), HexColor('#2c3e50')),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 10),
        ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
        
        # General
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 2, HexColor('#ff6b35')),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(primary_table)
    story.append(Spacer(1, 35))
    
    # === REGIONAL OPERATIONS SECTION ===
    story.append(Paragraph("STRATEGIC REGIONAL OPERATIONS", section_header))
    story.append(Spacer(1, 25))
    
    regional_intro = """
    NVC Fund Bank maintains strategic regional presence through specialized SWIFT codes positioned 
    across key financial centers and regulatory jurisdictions worldwide, ensuring comprehensive 
    coverage of global banking markets and regulatory compliance frameworks.
    """
    story.append(Paragraph(regional_intro, body_text))
    story.append(Spacer(1, 20))
    
    # Enhanced regional table with better data
    regional_data = [
        ['REGION', 'SWIFT CODE', 'OPERATIONAL CENTER', 'SPECIALIZATION'],
        ['North America', 'NVCFUSXX', 'United States Operations\nNew York & Dallas', 'Correspondent Banking\n& Federal Reserve Relations'],
        ['Europe', 'NVCFGBXX', 'United Kingdom Hub\nLondon Financial District', 'European Markets\n& ECB Coordination'],
        ['Asia Pacific', 'NVCFSGXX', 'Singapore Center\nASEAN Financial Hub', 'Asian Operations\n& Regional Banking'],
        ['Australia/Oceania', 'NVCFAUXX', 'Australian Division\nSydney & Melbourne', 'Pacific Region\n& APRA Relations'],
        ['Middle East', 'NVCFAEXX', 'UAE Operations\nDubai International', 'MENA Markets\n& Islamic Banking'],
        ['Africa', 'NVCFZAXX', 'South African Hub\nJohannesburg Centre', 'Continental Operations\n& Development Finance']
    ]
    
    regional_table = Table(regional_data, colWidths=[1.6*inch, 1.2*inch, 2*inch, 2.2*inch])
    regional_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Data
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2c3e50')),
        ('FONTNAME', (0, 1), (1, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        
        # General
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6)
    ]))
    story.append(regional_table)
    
    # Build the PDF
    doc.build(story)
    print(f"Ultimate professional PDF created: {filename}")
    return filename

if __name__ == "__main__":
    create_ultimate_swift_pdf()