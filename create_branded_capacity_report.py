#!/usr/bin/env python3
"""
Branded NVC Fund Bank Capacity and Capability Report with Logo
"""
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

def create_branded_capacity_report():
    """Create branded capacity report with NVC Fund logo"""
    
    filename = "NVC_Fund_Bank_Capacity_Report_Branded.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.5*inch, bottomMargin=0.75*inch)
    
    # Professional styles
    styles = getSampleStyleSheet()
    
    main_title = ParagraphStyle(
        'MainTitle',
        parent=styles['Title'],
        fontSize=28,
        spaceAfter=15,
        spaceBefore=20,
        alignment=TA_CENTER,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold'
    )
    
    section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        spaceBefore=25,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        borderWidth=2,
        borderColor=HexColor('#ff6b35'),
        borderPadding=10,
        backColor=HexColor('#f8f9fa')
    )
    
    body_text = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        spaceBefore=6,
        alignment=TA_JUSTIFY,
        textColor=HexColor('#2c3e50'),
        fontName='Helvetica',
        leading=14
    )
    
    # Build report content
    story = []
    
    # === BRANDED COVER PAGE ===
    story.append(Spacer(1, 0.15*inch))
    
    # Add NVC Fund logo with white background
    logo_path = 'static/nvc_fund_logo.png'
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2.5*inch, height=0.75*inch)
        logo.hAlign = 'CENTER'
        
        # Create container with logo on white background
        logo_container_data = [[logo]]
        logo_container_table = Table(logo_container_data, colWidths=[3*inch], rowHeights=[1*inch])
        logo_container_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0, white)
        ]))
        
        story.append(logo_container_table)
        story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("NVC FUND BANK", main_title))
    story.append(Paragraph("INSTITUTIONAL CAPACITY & CAPABILITY", main_title))
    story.append(Paragraph("STATUS REPORT", main_title))
    story.append(Spacer(1, 0.15*inch))
    
    # Report metadata with enhanced styling
    current_date = datetime.now().strftime("%B %d, %Y")
    cover_info = [
        ['REPORT INFORMATION', ''],
        ['Report Date', current_date],
        ['Reporting Period', 'Q2 2025 Current Status'],
        ['Document Classification', 'Executive Confidential'],
        ['Prepared By', 'NVC Fund Bank Operations Division'],
        ['Distribution', 'Board of Directors & Regulatory Authorities'],
        ['Authority', 'African Union Treaty Framework']
    ]
    
    cover_table = Table(cover_info, colWidths=[2.5*inch, 3.5*inch])
    cover_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('SPAN', (0, 0), (1, 0)),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Data
        ('BACKGROUND', (0, 1), (0, -1), HexColor('#34495e')),
        ('BACKGROUND', (1, 1), (1, -1), white),
        ('TEXTCOLOR', (0, 1), (0, -1), white),
        ('TEXTCOLOR', (1, 1), (1, -1), HexColor('#2c3e50')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12)
    ]))
    story.append(cover_table)
    story.append(PageBreak())
    
    # === EXECUTIVE SUMMARY ===
    story.append(Paragraph("EXECUTIVE SUMMARY", section_header))
    story.append(Spacer(1, 10))
    
    exec_summary = """
    NVC Fund Bank operates as a fully operational supranational sovereign institution with comprehensive 
    banking capabilities spanning global markets. As of Q2 2025, the institution maintains active 
    operations across four continents with assets under management exceeding $10 trillion and annual 
    revenue of $289 billion.
    
    Our institutional infrastructure supports a complete range of banking services including correspondent 
    banking, custody services, treasury management, payment processing, currency exchange, and blockchain 
    integration through the NVCT ecosystem. The bank maintains full regulatory compliance with international 
    standards including ISO 20022 and ISO 9362:2022 frameworks.
    """
    story.append(Paragraph(exec_summary, body_text))
    story.append(Spacer(1, 10))
    
    # === INSTITUTIONAL CAPACITY ===
    story.append(Paragraph("INSTITUTIONAL CAPACITY", section_header))
    story.append(Spacer(1, 8))
    
    # Financial capacity table
    financial_capacity = [
        ['FINANCIAL METRICS', 'CURRENT STATUS', 'CAPACITY RATING'],
        ['Total Assets Under Management', '$10+ Trillion USD', 'Tier 1 Global'],
        ['Market Capitalization', '$1+ Trillion USD', 'Supranational Scale'],
        ['Annual Revenue', '$289 Billion USD', 'Major Institution'],
        ['Liquidity Reserves', 'Multi-Billion USD', 'Highly Liquid'],
        ['Credit Rating', 'AAA Sovereign', 'Highest Grade'],
        ['Capital Adequacy', 'Treaty Backed', 'Sovereign Authority'],
        ['Risk Management', 'Advanced Systems', 'Enterprise Grade']
    ]
    
    capacity_table = Table(financial_capacity, colWidths=[2.5*inch, 2.2*inch, 1.8*inch])
    capacity_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2c3e50')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(capacity_table)
    story.append(Spacer(1, 12))
    
    # === OPERATIONAL CAPABILITIES ===
    story.append(Paragraph("OPERATIONAL CAPABILITIES", section_header))
    story.append(Spacer(1, 8))
    
    services_capability = [
        ['SERVICE CATEGORY', 'OPERATIONAL STATUS', 'CAPABILITY LEVEL'],
        ['SWIFT Network Operations', '15 Global Codes Active', 'Full Global Coverage'],
        ['Correspondent Banking', 'Multi-Jurisdictional', 'Tier 1 Relationships'],
        ['Payment Processing', 'Stripe, PayPal, ACH, Wire', 'Multi-Gateway Active'],
        ['Currency Exchange', '62+ Currency Pairs', 'Real-Time Processing'],
        ['Custody Services', 'Institutional Grade', 'Sovereign Backing'],
        ['Treasury Management', 'Multi-Billion Capacity', 'Advanced Systems'],
        ['Blockchain Integration', 'NVCT Ecosystem', 'Digital Ready'],
        ['ISO Compliance', '20022 & 9362:2022', 'Fully Certified'],
        ['Loan Origination', '$10M - $10B Range', 'Large Scale Capability'],
        ['Investment Banking', 'Institutional Focus', 'Global Markets']
    ]
    
    services_table = Table(services_capability, colWidths=[2.3*inch, 2.3*inch, 2*inch])
    services_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2c3e50')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(services_table)
    story.append(PageBreak())
    
    # === CONCLUSION ===
    story.append(Paragraph("CONCLUSION & READINESS ASSESSMENT", section_header))
    story.append(Spacer(1, 15))
    
    conclusion_text = """
    NVC Fund Bank demonstrates comprehensive institutional capacity and operational capability across 
    all major banking functions. With $10+ trillion in assets under management, $289 billion in annual 
    revenue, and full operational infrastructure spanning four continents, the institution is positioned 
    as a major player in global financial markets.
    
    The bank's technology infrastructure, regulatory compliance framework, and strategic partnerships 
    provide a solid foundation for continued growth and expansion. Our supranational sovereign status 
    under African Union Treaty authority, combined with full SWIFT network integration and multi-gateway 
    payment processing capabilities, enables us to serve the most demanding institutional clients worldwide.
    
    <b>Current operational readiness:</b> Fully Operational<br/>
    <b>Institutional capacity rating:</b> Tier 1 Global Institution<br/>
    <b>Technology capability:</b> Next-Generation Ready<br/>
    <b>Regulatory status:</b> Fully Compliant
    """
    story.append(Paragraph(conclusion_text, body_text))
    
    # Build the report
    doc.build(story)
    print(f"Branded capacity report created: {filename}")
    return filename

if __name__ == "__main__":
    create_branded_capacity_report()