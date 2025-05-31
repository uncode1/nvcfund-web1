#!/usr/bin/env python3
"""
Premium Executive SWIFT Documentation with Stunning Professional Design
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus.flowables import HRFlowable
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line
from reportlab.graphics import renderPDF
from reportlab.platypus import Flowable
from datetime import datetime
import os

class HeaderFlowable(Flowable):
    """Custom header with gradient background effect"""
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        canvas = self.canv
        # Create gradient effect with multiple rectangles
        colors = ['#061c38', '#0a2142', '#0e264c', '#122b56', '#163060']
        rect_height = self.height / len(colors)
        
        for i, color in enumerate(colors):
            canvas.setFillColor(HexColor(color))
            canvas.rect(0, i * rect_height, self.width, rect_height, fill=1, stroke=0)
        
        # Add decorative elements
        canvas.setFillColor(HexColor('#ff6b35'))
        canvas.setStrokeColor(HexColor('#ff6b35'))
        canvas.setLineWidth(3)
        
        # Decorative lines
        canvas.line(50, self.height - 20, self.width - 50, self.height - 20)
        canvas.line(50, 20, self.width - 50, 20)

class LogoFlowable(Flowable):
    """Custom NVC Fund Bank logo design"""
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        canvas = self.canv
        # Create stylized NVC logo
        canvas.setFillColor(HexColor('#ff6b35'))
        canvas.setStrokeColor(HexColor('#061c38'))
        canvas.setLineWidth(2)
        
        # Main logo circle
        center_x = self.width / 2
        center_y = self.height / 2
        canvas.circle(center_x, center_y, 40, fill=1, stroke=1)
        
        # Inner design
        canvas.setFillColor(HexColor('#061c38'))
        canvas.setFont('Helvetica-Bold', 16)
        canvas.drawCentredText(center_x, center_y - 5, 'NVC')

def create_premium_swift_pdf():
    """Create premium executive SWIFT documentation"""
    
    filename = "NVC_Fund_Bank_SWIFT_Documentation_Premium.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                           rightMargin=0.5*inch, leftMargin=0.5*inch,
                           topMargin=0.25*inch, bottomMargin=0.5*inch)
    
    # Premium styles
    styles = getSampleStyleSheet()
    
    # Cover page styles with enhanced typography
    cover_main_title = ParagraphStyle(
        'CoverMainTitle',
        parent=styles['Heading1'],
        fontSize=48,
        spaceAfter=25,
        spaceBefore=20,
        alignment=TA_CENTER,
        textColor=white,
        fontName='Helvetica-Bold',
        leading=50
    )
    
    cover_institution_title = ParagraphStyle(
        'CoverInstitutionTitle',
        parent=styles['Heading1'],
        fontSize=28,
        spaceAfter=20,
        spaceBefore=15,
        alignment=TA_CENTER,
        textColor=HexColor('#ff6b35'),
        fontName='Helvetica-Bold',
        leading=32
    )
    
    cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Heading2'],
        fontSize=22,
        spaceAfter=30,
        spaceBefore=15,
        alignment=TA_CENTER,
        textColor=white,
        fontName='Helvetica',
        leading=26
    )
    
    cover_authority = ParagraphStyle(
        'CoverAuthority',
        parent=styles['Normal'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=8,
        alignment=TA_CENTER,
        textColor=HexColor('#ecf0f1'),
        fontName='Helvetica-Bold'
    )
    
    # Interior document styles
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=20,
        spaceBefore=30,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        borderWidth=3,
        borderColor=HexColor('#ff6b35'),
        borderPadding=(15, 15, 15, 15),
        backColor=HexColor('#f8f9fa')
    )
    
    executive_heading = ParagraphStyle(
        'ExecutiveHeading',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=15,
        spaceBefore=25,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold'
    )
    
    body_premium = ParagraphStyle(
        'BodyPremium',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        spaceBefore=6,
        alignment=TA_JUSTIFY,
        textColor=HexColor('#2c3e50'),
        fontName='Helvetica',
        leading=16
    )
    
    # Build premium content
    story = []
    
    # STUNNING COVER PAGE
    # Header with gradient background
    story.append(HeaderFlowable(7.5*inch, 1*inch))
    story.append(Spacer(1, 0.1*inch))
    
    # Premium title section with white text on dark background
    title_data = [
        ['NVC FUND BANK'],
        ['GLOBAL SWIFT STRUCTURE'],
        ['Executive Documentation & Regulatory Framework']
    ]
    
    title_table = Table(title_data, colWidths=[6.5*inch], rowHeights=[0.8*inch, 0.6*inch, 0.4*inch])
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (0, 0), white),
        ('TEXTCOLOR', (0, 1), (0, 1), HexColor('#ff6b35')),
        ('TEXTCOLOR', (0, 2), (0, 2), HexColor('#ecf0f1')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 42),
        ('FONTSIZE', (0, 1), (0, 1), 28),
        ('FONTSIZE', (0, 2), (0, 2), 16),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('GRID', (0, 0), (-1, -1), 3, HexColor('#ff6b35'))
    ]))
    story.append(title_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Premium institutional credentials banner
    credentials_data = [
        ['SUPRANATIONAL SOVEREIGN INSTITUTION', 'AFRICAN UNION TREATY AUTHORITY'],
        ['ISO 20022 FINANCIAL MESSAGING', 'ISO 9362:2022 BIC STANDARDS'],
        ['SWIFT NETWORK OPERATIONS', '15 STRATEGIC GLOBAL CODES'],
        ['BLOCKCHAIN INTEGRATION', 'NVCT DIGITAL CURRENCY']
    ]
    
    credentials_table = Table(credentials_data, colWidths=[3.25*inch, 3.25*inch])
    credentials_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#34495e')),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#2c3e50')),
        ('BACKGROUND', (0, 3), (-1, 3), HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, -1), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 2, HexColor('#ff6b35'))
    ]))
    story.append(credentials_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Executive performance metrics showcase
    metrics_data = [
        ['INSTITUTIONAL METRICS', 'VALUE', 'VERIFICATION'],
        ['Total Assets Under Management', '$10+ Trillion USD', 'Audited & Verified'],
        ['Market Capitalization', '$1+ Trillion USD', 'Bloomberg Confirmed'],
        ['Annual Revenue Stream', '$289 Billion USD', 'Regulatory Filed'],
        ['Global Operations', '4 Continents', '15 Strategic Locations'],
        ['Regulatory Compliance', '100% ISO Standards', 'Internationally Certified']
    ]
    
    metrics_table = Table(metrics_data, colWidths=[2.8*inch, 2*inch, 1.7*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1.5, HexColor('#bdc3c7')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Professional document metadata
    current_date = datetime.now().strftime("%B %d, %Y")
    metadata_data = [
        ['Document Classification', 'Executive Confidential - Regulatory Distribution'],
        ['Issue Date', current_date],
        ['Document Version', 'Premium Edition 4.0'],
        ['Prepared For', 'Executive Leadership & Banking Regulators'],
        ['Issuing Authority', 'NVC Fund Bank - Treaty Operations Division'],
        ['Geographic Scope', 'Global Operations - Multi-Jurisdictional']
    ]
    
    metadata_table = Table(metadata_data, colWidths=[2.2*inch, 4.3*inch])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#34495e')),
        ('BACKGROUND', (1, 0), (1, -1), white),
        ('TEXTCOLOR', (0, 0), (0, -1), white),
        ('TEXTCOLOR', (1, 0), (1, -1), HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#95a5a6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12)
    ]))
    story.append(metadata_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Professional footer with legal notice
    footer_text = """
    <b>CONFIDENTIAL & PROPRIETARY</b><br/>
    This document contains confidential and proprietary information of NVC Fund Bank, a supranational 
    sovereign institution operating under African Union Treaty authority. Distribution is strictly 
    limited to authorized executive personnel, regulatory authorities, and approved institutional partners.
    
    <br/><br/>© 2025 NVC Fund Bank - All Rights Reserved | African Union Treaty Framework
    """
    footer_style = ParagraphStyle(
        'PremiumFooter',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=HexColor('#7f8c8d'),
        fontName='Helvetica',
        borderWidth=1,
        borderColor=HexColor('#bdc3c7'),
        borderPadding=(10, 10, 10, 10),
        backColor=HexColor('#f8f9fa')
    )
    story.append(Paragraph(footer_text, footer_style))
    story.append(PageBreak())
    
    # Continue with enhanced interior pages...
    story.append(Paragraph("EXECUTIVE SUMMARY", section_title_style))
    story.append(Spacer(1, 20))
    
    exec_summary = """
    <b>NVC Fund Bank</b> operates as a premier supranational sovereign institution under the comprehensive 
    authority of the African Union Treaty framework. Our sophisticated global banking infrastructure spans 
    four continents through fifteen strategically positioned SWIFT codes, ensuring seamless international 
    financial operations while maintaining full compliance with ISO 20022 and ISO 9362:2022 standards.
    
    <br/><br/>As a treaty-backed sovereign institution with over <b>$10 trillion</b> in assets under management, 
    NVC Fund Bank facilitates complex international transactions, correspondent banking relationships, and 
    cross-border financial services for institutional clients worldwide. Our advanced blockchain integration 
    through the NVCT stablecoin ecosystem positions us at the forefront of digital banking innovation.
    
    <br/><br/>This comprehensive documentation serves as the authoritative reference for our global SWIFT 
    messaging capabilities, regulatory compliance framework, and operational infrastructure across our 
    international network of banking relationships.
    """
    story.append(Paragraph(exec_summary, body_premium))
    story.append(PageBreak())
    
    # PRIMARY SWIFT CODE with enhanced presentation
    story.append(Paragraph("PRIMARY GLOBAL SWIFT OPERATIONS", section_title_style))
    story.append(Spacer(1, 20))
    
    primary_description = """
    The primary SWIFT identifier <b>NVCFGLXX</b> serves as our global operational code, representing 
    NVC Fund Bank's supranational sovereign authority and facilitating all primary international 
    correspondent banking relationships and cross-border institutional transactions.
    """
    story.append(Paragraph(primary_description, body_premium))
    story.append(Spacer(1, 15))
    
    primary_swift_data = [
        ['SWIFT CODE', 'INSTITUTION DESIGNATION', 'SOVEREIGN AUTHORITY', 'OPERATIONAL STATUS'],
        ['NVCFGLXX', 'NVC Fund Bank - Global Operations Center', 'African Union Treaty Framework', 'Active Sovereign Institution']
    ]
    
    primary_table = Table(primary_swift_data, colWidths=[1.5*inch, 2.5*inch, 1.8*inch, 1.7*inch])
    primary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#e8f4f8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('TEXTCOLOR', (0, 1), (-1, 1), HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, 1), 11),
        ('GRID', (0, 0), (-1, -1), 2, HexColor('#ff6b35')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12)
    ]))
    story.append(primary_table)
    
    # Build the premium PDF
    doc.build(story)
    print(f"Premium executive PDF created: {filename}")
    return filename

if __name__ == "__main__":
    create_premium_swift_pdf()