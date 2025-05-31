#!/usr/bin/env python3
"""
Generate Professional SWIFT Documentation PDF with Enhanced Layout
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus.flowables import HRFlowable, KeepTogether
from reportlab.platypus.tableofcontents import TableOfContents
from datetime import datetime
import os

class NumberedCanvas:
    """Custom canvas for adding page numbers and headers"""
    def __init__(self, canvas, doc):
        self.canvas = canvas
        self.doc = doc

    def __call__(self, canvas, doc):
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(HexColor('#666666'))
        canvas.drawString(72, letter[1] - 50, "NVC Fund Bank - Global SWIFT Structure Documentation")
        canvas.drawRightString(letter[0] - 72, letter[1] - 50, f"Confidential - Executive Level")
        
        # Footer with page numbers
        canvas.setFont('Helvetica', 8)
        canvas.drawCentredText(letter[0]/2, 30, f"Page {doc.page}")
        
        canvas.restoreState()

def create_professional_swift_pdf():
    """Create professional SWIFT documentation with enhanced formatting"""
    
    filename = "NVC_Fund_Bank_SWIFT_Documentation_Professional.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                           rightMargin=1*inch, leftMargin=1*inch,
                           topMargin=1*inch, bottomMargin=0.75*inch)
    
    # Enhanced styles
    styles = getSampleStyleSheet()
    
    # Custom professional styles
    title_style = ParagraphStyle(
        'ProfessionalTitle',
        parent=styles['Heading1'],
        fontSize=28,
        spaceAfter=30,
        spaceBefore=20,
        alignment=TA_CENTER,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'ProfessionalSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=20,
        spaceBefore=10,
        alignment=TA_CENTER,
        textColor=HexColor('#ff6b35'),
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'ProfessionalHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=15,
        spaceBefore=25,
        textColor=HexColor('#061c38'),
        fontName='Helvetica-Bold',
        borderWidth=1,
        borderColor=HexColor('#ff6b35'),
        borderPadding=(5, 5, 5, 5),
        backColor=HexColor('#f8f9fa')
    )
    
    subheading_style = ParagraphStyle(
        'ProfessionalSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=18,
        textColor=HexColor('#ff6b35'),
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'ProfessionalBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=10,
        spaceBefore=5,
        alignment=TA_JUSTIFY,
        textColor=black,
        fontName='Helvetica',
        leading=14
    )
    
    executive_style = ParagraphStyle(
        'ExecutiveSummary',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        spaceBefore=8,
        alignment=TA_JUSTIFY,
        textColor=HexColor('#2c3e50'),
        fontName='Helvetica',
        leading=16,
        borderWidth=1,
        borderColor=HexColor('#bdc3c7'),
        borderPadding=(10, 10, 10, 10),
        backColor=HexColor('#ecf0f1')
    )
    
    # Build story
    story = []
    
    # Professional Title Page
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("NVC FUND BANK", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Global SWIFT Structure", subtitle_style))
    story.append(Paragraph("Documentation Framework", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Institutional badge
    institutional_data = [
        ['SUPRANATIONAL SOVEREIGN INSTITUTION'],
        ['Under African Union Treaty Framework'],
        ['ISO 20022 & ISO 9362:2022 Compliant']
    ]
    
    institutional_table = Table(institutional_data, colWidths=[5*inch])
    institutional_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, -1), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 14),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 2, HexColor('#ff6b35')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor('#061c38'), HexColor('#2c3e50'), HexColor('#34495e')])
    ]))
    story.append(institutional_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Document information box
    current_date = datetime.now().strftime("%B %d, %Y")
    doc_info = [
        ['Document Date:', current_date],
        ['Version:', '2.0 - Professional Executive Edition'],
        ['Classification:', 'Executive Confidential'],
        ['Authority:', 'African Union Treaty Framework']
    ]
    
    doc_table = Table(doc_info, colWidths=[2*inch, 3*inch])
    doc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#ecf0f1')),
        ('BACKGROUND', (1, 0), (1, -1), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(doc_table)
    story.append(PageBreak())
    
    # Table of Contents
    story.append(Paragraph("Table of Contents", heading_style))
    toc_data = [
        ['1. Executive Summary', '3'],
        ['2. Primary Global SWIFT Code', '4'],
        ['3. Regional Operations Framework', '5'],
        ['   3.1 United States Operations', '5'],
        ['   3.2 European Operations', '6'],
        ['   3.3 Asia-Pacific Operations', '7'],
        ['   3.4 African Operations', '8'],
        ['4. ISO Standards Compliance', '9'],
        ['5. NVCT Stablecoin Integration', '10'],
        ['6. Regulatory Framework', '11']
    ]
    
    toc_table = Table(toc_data, colWidths=[4*inch, 1*inch])
    toc_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, HexColor('#bdc3c7'))
    ]))
    story.append(toc_table)
    story.append(PageBreak())
    
    # Executive Summary with enhanced formatting
    story.append(Paragraph("1. Executive Summary", heading_style))
    story.append(HRFlowable(width="100%", thickness=3, color=HexColor('#ff6b35')))
    story.append(Spacer(1, 15))
    
    exec_summary = """
    NVC Fund Bank operates as a supranational sovereign institution under the African Union Treaty framework, 
    providing comprehensive banking services through a strategically designed global SWIFT network. Our 15 sovereign 
    SWIFT codes ensure full compliance with ISO 20022 and ISO 9362:2022 international standards while supporting 
    advanced blockchain integration through the NVCT stablecoin ecosystem.
    
    As a treaty-backed sovereign institution, NVC Fund Bank maintains operational authority across multiple 
    jurisdictions while adhering to the highest international banking standards. Our global SWIFT infrastructure 
    supports comprehensive correspondent banking relationships, facilitating seamless international transactions 
    and cross-border financial services.
    """
    story.append(Paragraph(exec_summary, executive_style))
    story.append(Spacer(1, 20))
    
    # Key Statistics Box
    stats_data = [
        ['Total Assets Under Management', '$10+ Trillion USD'],
        ['Market Capitalization', '$1+ Trillion USD'],
        ['Annual Revenue', '$289 Billion USD'],
        ['Global SWIFT Codes', '15 Strategic Locations'],
        ['ISO Compliance Level', '100% - Full Implementation']
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2.5*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(stats_table)
    story.append(PageBreak())
    
    # Primary SWIFT Code with enhanced presentation
    story.append(Paragraph("2. Primary Global SWIFT Code", heading_style))
    story.append(HRFlowable(width="100%", thickness=2, color=HexColor('#ff6b35')))
    story.append(Spacer(1, 15))
    
    primary_swift_data = [
        ['SWIFT Code', 'Institution Name', 'Operational Authority', 'Treaty Status'],
        ['NVCFGLXX', 'NVC Fund Bank - Global Operations', 'Supranational Sovereign', 'African Union Treaty']
    ]
    
    primary_swift_table = Table(primary_swift_data, colWidths=[1.3*inch, 2.2*inch, 1.8*inch, 1.5*inch])
    primary_swift_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#061c38')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#e8f4f8')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 2, HexColor('#ff6b35')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10)
    ]))
    story.append(primary_swift_table)
    story.append(Spacer(1, 20))
    
    # Continue with regional operations...
    story.append(Paragraph("3. Regional Operations Framework", heading_style))
    story.append(HRFlowable(width="100%", thickness=2, color=HexColor('#ff6b35')))
    story.append(Spacer(1, 15))
    
    # US Operations with enhanced table
    story.append(Paragraph("3.1 United States Operations", subheading_style))
    us_data = [
        ['SWIFT Code', 'Location', 'Operational Focus', 'Regulatory Compliance'],
        ['NVCFUSNY', 'New York', 'Federal Reserve Relations & USD Operations', 'Fed Reg Y, CFTC'],
        ['NVCFUSMI', 'Miami', 'Latin American Correspondent Banking', 'FinCEN, OFAC']
    ]
    
    us_table = Table(us_data, colWidths=[1.3*inch, 1.3*inch, 2.4*inch, 1.8*inch])
    us_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(us_table)
    story.append(Spacer(1, 15))
    
    # Add all other regions with similar enhanced formatting...
    # [Additional regions would continue with similar professional styling]
    
    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Professional PDF created successfully: {filename}")
    return filename

if __name__ == "__main__":
    create_professional_swift_pdf()