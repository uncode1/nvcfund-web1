"""
Simple Circle Partnership Routes for NVC Banking Platform
"""

from flask import Blueprint, render_template, send_file, make_response
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
import io

# Create Blueprint
circle_bp = Blueprint('circle', __name__, url_prefix='/circle')

@circle_bp.route('/')
def partnership_overview():
    """Circle partnership overview and materials access"""
    return render_template('circle_partnership/overview.html',
                         title="Circle Strategic Partnership")

@circle_bp.route('/presentation')
def interactive_presentation():
    """Interactive HTML presentation for Circle partnership"""
    return render_template('circle_presentation.html',
                         title="Circle Strategic Partnership Presentation")

@circle_bp.route('/powerpoint')
def powerpoint_presentation():
    """PowerPoint-style presentation for Circle partnership"""
    return render_template('circle_presentation.pptx.html',
                         title="Circle Partnership - PowerPoint Format")

@circle_bp.route('/pdf')
def download_pdf():
    """Generate and download PDF version of Circle Strategic Partnership presentation"""
    buffer = io.BytesIO()
    
    # Create PDF document with professional formatting
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, 
                          topMargin=60, bottomMargin=60)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Clean, professional styles for executive presentation
    title_style = ParagraphStyle(
        'ExecutiveTitle',
        parent=styles['Heading1'],
        fontSize=24,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_CENTER,
        spaceAfter=30,
        spaceBefore=20
    )
    
    subtitle_style = ParagraphStyle(
        'ExecutiveSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        fontName='Helvetica',
        textColor=colors.HexColor('#34495e'),
        alignment=TA_CENTER,
        spaceAfter=25,
        spaceBefore=15
    )
    
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=16,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=15,
        spaceBefore=20,
        leftIndent=0,
        borderWidth=0,
        borderColor=colors.HexColor('#3498db'),
        borderPadding=0
    )
    
    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#2c5282'),
        spaceAfter=10,
        spaceBefore=15
    )
    
    body_style = ParagraphStyle(
        'ExecutiveBody',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica',
        textColor=colors.black,
        spaceAfter=8,
        spaceBefore=3,
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    bullet_style = ParagraphStyle(
        'ExecutiveBullet',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica',
        textColor=colors.black,
        leftIndent=25,
        bulletIndent=15,
        spaceAfter=8,
        spaceBefore=3,
        leading=14
    )
    
    highlight_style = ParagraphStyle(
        'FinancialHighlight',
        parent=styles['Normal'],
        fontSize=14,
        fontName='Helvetica-Bold',
        textColor=colors.white,
        backColor=colors.HexColor('#3498db'),
        alignment=TA_CENTER,
        spaceAfter=20,
        spaceBefore=15,
        borderPadding=12
    )
    
    metric_style = ParagraphStyle(
        'KeyMetric',
        parent=styles['Normal'],
        fontSize=20,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_CENTER,
        spaceAfter=10,
        spaceBefore=10
    )
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=5
    )
    
    # Build story with professional executive presentation layout
    story = []
    
    # Executive Cover Page
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("CIRCLE STRATEGIC PARTNERSHIP", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("NVC Fund Bank × Circle", subtitle_style))
    story.append(Spacer(1, 0.8*inch))
    
    # Key financial highlight box
    story.append(Paragraph("$1.5B Strategic Investment Opportunity", highlight_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("25% Equity Stake", metric_style))
    story.append(Spacer(1, 0.6*inch))
    
    story.append(Paragraph("Building the Future of Institutional Digital Finance", subtitle_style))
    story.append(Spacer(1, 1*inch))
    
    # Executive summary box
    exec_summary = """
    <para align="center">
    <b>CONFIDENTIAL EXECUTIVE PRESENTATION</b><br/>
    Prepared for Circle Financial Leadership<br/>
    Strategic Partnership Proposal<br/>
    May 2025
    </para>
    """
    story.append(Paragraph(exec_summary, body_style))
    story.append(PageBreak())
    
    # Executive Summary with enhanced formatting
    story.append(Paragraph("EXECUTIVE SUMMARY", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Investment overview box
    investment_overview = """
    <para align="center" bgcolor="#f8f9fa" borderColor="#1e3a5f" borderWidth="2" borderPadding="15">
    <b>STRATEGIC INVESTMENT PROPOSAL</b><br/>
    Investment Amount: <b>$1.5 Billion USD</b><br/>
    Equity Stake: <b>25% Strategic Partnership</b><br/>
    Projected ROI: <b>$480M Annual Revenue by Year 5</b>
    </para>
    """
    story.append(Paragraph(investment_overview, body_style))
    story.append(Spacer(1, 0.4*inch))
    
    # Two-column layout for Market Position and Strategic Value
    story.append(Paragraph("NVC Fund Bank Market Position", heading_style))
    market_data = [
        ['Asset Category', 'Value', 'Impact'],
        ['Managed Assets', '$10+ Trillion', 'Global institutional reach'],
        ['Market Capitalization', '$1+ Trillion', 'Proven financial strength'],
        ['Annual Revenue', '$289 Billion', 'Sustainable operations'],
        ['Geographic Reach', '200+ Countries', 'Worldwide presence'],
        ['Regulatory Status', 'African Union Treaty', 'International recognition']
    ]
    
    market_table = Table(market_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
    market_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8)
    ]))
    
    story.append(market_table)
    story.append(Spacer(1, 0.4*inch))
    
    story.append(Paragraph("Strategic Partnership Value Proposition", heading_style))
    value_data = [
        ['Integration Area', 'NVC Contribution', 'Circle Benefit'],
        ['USDC Infrastructure', 'Institutional distribution network', 'Expanded enterprise adoption'],
        ['DeFi Gateway', 'Regulatory compliance framework', 'Institutional market access'],
        ['Cross-border Payments', 'Global banking relationships', 'Enhanced settlement efficiency'],
        ['Revenue Generation', '$1.2B projected by Year 5', 'Shared growth opportunity']
    ]
    
    value_table = Table(value_data, colWidths=[2*inch, 2*inch, 2*inch])
    value_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8)
    ]))
    
    story.append(value_table)
    story.append(PageBreak())
    
    # Partnership Structure Options
    story.append(Paragraph("PARTNERSHIP STRUCTURE OPTIONS", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Recommended option highlight
    story.append(Paragraph("RECOMMENDED: Strategic Investment Partnership", highlight_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Enhanced partnership options table
    partnership_data = [
        ['Partnership Option', 'Investment Amount', 'Equity Position', 'Strategic Benefits', 'Timeline'],
        ['Strategic Investment\n(RECOMMENDED)', '$1.5 Billion', '25% Equity Stake', '• Board representation\n• Technology integration\n• Shared revenue (60/40)\n• Joint market expansion', 'Q1-Q4 2025'],
        ['Full Acquisition', '$6.0 Billion', '100% Ownership', '• Complete operational control\n• Brand integration\n• Asset consolidation\n• Direct revenue capture', 'Q2-Q4 2025'],
        ['Phased Approach', 'Variable\n($500M start)', 'Gradual Increase\n(5-25%)', '• Performance milestones\n• Reduced initial risk\n• Scalable investment\n• Flexible structure', '2025-2027']
    ]
    
    partnership_table = Table(partnership_data, colWidths=[1.4*inch, 1.2*inch, 1.2*inch, 2.0*inch, 1.0*inch])
    partnership_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#e8f5e8')),  # Highlight recommended
        ('BACKGROUND', (0, 2), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#e8f5e8'), colors.white, colors.HexColor('#f8f9fa')])
    ]))
    
    story.append(partnership_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Investment terms summary
    terms_summary = """
    <para align="center" bgcolor="#f0f8ff" borderColor="#219ebc" borderWidth="1" borderPadding="10">
    <b>STRATEGIC INVESTMENT TERMS SUMMARY</b><br/>
    • Initial Investment: $1.5B for 25% equity stake<br/>
    • Board Seats: 2 Circle representatives, 3 NVC representatives<br/>
    • Revenue Share: 60% NVC, 40% Circle on joint initiatives<br/>
    • Liquidity Events: Mutual approval required for major decisions<br/>
    • Integration Timeline: 12-month phased technology integration
    </para>
    """
    story.append(Paragraph(terms_summary, body_style))
    story.append(PageBreak())
    
    # Financial Projections & Market Opportunity
    story.append(Paragraph("FINANCIAL PROJECTIONS & ROI ANALYSIS", title_style))
    story.append(Paragraph("$1.2B Annual Revenue by Year 5", metric_style))
    story.append(Spacer(1, 0.3*inch))
    
    # 5-Year Revenue Projection Table
    revenue_data = [
        ['Year', 'Platform Revenue', 'NVC Share (60%)', 'Circle Share (40%)', 'Key Milestones'],
        ['2025', '$50M', '$30M', '$20M', 'Partnership launch, Initial integration'],
        ['2026', '$150M', '$90M', '$60M', 'Market expansion, Product scaling'],
        ['2027', '$400M', '$240M', '$160M', 'Scale achievement, Global reach'],
        ['2028', '$750M', '$450M', '$300M', 'Market leadership, Innovation'],
        ['2029', '$1.2B', '$720M', '$480M', 'Global dominance, Full potential']
    ]
    
    revenue_table = Table(revenue_data, colWidths=[0.8*inch, 1.2*inch, 1.2*inch, 1.2*inch, 2.4*inch])
    revenue_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f5e8')),  # Highlight final year
        ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    
    story.append(revenue_table)
    story.append(Spacer(1, 0.4*inch))
    
    # ROI Summary
    roi_summary = """
    <para align="center" bgcolor="#e8f5e8" borderColor="#28a745" borderWidth="2" borderPadding="12">
    <b>RETURN ON INVESTMENT SUMMARY</b><br/>
    Circle's $1.5B Investment generates $480M annual revenue by Year 5<br/>
    <b>32% Annual ROI</b> | <b>2.4B Total 5-Year Returns</b> | <b>60% ROI over 5 years</b>
    </para>
    """
    story.append(Paragraph(roi_summary, body_style))
    story.append(PageBreak())
    
    # Implementation Timeline
    story.append(Paragraph("IMPLEMENTATION TIMELINE", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Realistic timeline table with proper formatting
    timeline_data = [
        ['Phase', 'Timeline', 'Key Deliverables', 'Success Metrics'],
        ['Due Diligence &\nNegotiation', 'Q2-Q3 2025', '• Comprehensive financial audit\n• Legal framework development\n• Term sheet finalization\n• Regulatory review', '• Due diligence completion\n• Investment committee approval\n• Legal documentation signed'],
        ['Partnership\nFormation', 'Q4 2025 -\nQ1 2026', '• Final agreements executed\n• Capital injection completed\n• Board structure established\n• Integration planning', '• $1.5B investment secured\n• Governance framework active\n• Integration roadmap approved'],
        ['Technology\nIntegration', 'Q1-Q3 2026', '• USDC infrastructure deployment\n• API integration and testing\n• Staff onboarding and training\n• System optimization', '• 95% system compatibility\n• Zero downtime migration\n• Staff certification complete'],
        ['Market Launch\n& Scale', 'Q4 2026 -\nQ2 2027', '• Pilot program launch\n• Global market expansion\n• Service portfolio completion\n• Revenue generation at scale', '• 100+ institutional clients\n• $50M+ annual run rate\n• 500+ active institutions']
    ]
    
    timeline_table = Table(timeline_data, colWidths=[1.5*inch, 1.2*inch, 2.3*inch, 2.0*inch])
    timeline_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#219ebc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
    ]))
    
    story.append(timeline_table)
    story.append(PageBreak())
    
    # Next Steps & Contact
    story.append(Paragraph("NEXT STEPS & CONTACT INFORMATION", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Ready to Transform Digital Finance Together", highlight_style))
    story.append(Spacer(1, 0.4*inch))
    
    # Next steps table
    next_steps_data = [
        ['Action Item', 'Responsible Party', 'Timeline', 'Deliverable'],
        ['Executive Presentation', 'NVC Fund Bank', 'Immediate', 'Board-level meeting scheduled'],
        ['Due Diligence Initiation', 'Both Parties', 'Within 2 weeks', 'Comprehensive financial audit'],
        ['Legal Framework Development', 'Legal Teams', 'Within 30 days', 'Partnership agreement draft'],
        ['Integration Planning', 'Technical Teams', 'Within 45 days', 'Detailed implementation roadmap'],
        ['Final Agreement Execution', 'Executive Leadership', 'Q1 2025', 'Signed partnership agreement']
    ]
    
    next_steps_table = Table(next_steps_data, colWidths=[1.5*inch, 1.3*inch, 1.2*inch, 2.8*inch])
    next_steps_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    
    story.append(next_steps_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Contact information
    contact_info = """
    <para align="center" bgcolor="#f0f8ff" borderColor="#1e3a5f" borderWidth="1" borderPadding="15">
    <b>EXECUTIVE CONTACT INFORMATION</b><br/><br/>
    <b>NVC Fund Bank Strategic Partnership Division</b><br/>
    Email: Partnership@nvcfund.bank<br/>
    Executive Team: Available for immediate discussion<br/>
    Strategic Planning: Ready for due diligence process<br/><br/>
    <i>Confidential & Proprietary - Circle Financial Executive Review</i>
    </para>
    """
    story.append(Paragraph(contact_info, body_style))
    
    # Final call to action
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Let's Build the Future of Digital Finance Together", highlight_style))
    
    # Build PDF
    doc.build(story)
    
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=Circle_Strategic_Partnership_Presentation.pdf'
    
    return response