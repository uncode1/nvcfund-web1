"""
SWIFT Documentation Routes for NVC Fund Bank
Serves official documentation for global SWIFT structure
"""

from flask import Blueprint, render_template, make_response, request
from datetime import datetime
import pdfkit
import os

# Create blueprint
swift_docs_bp = Blueprint('swift_docs', __name__, url_prefix='/documentation')

@swift_docs_bp.route('/swift-structure')
def swift_structure_html():
    """Serve the NVC Fund Bank Global SWIFT Structure documentation as HTML"""
    current_date = datetime.now().strftime('%B %d, %Y')
    return render_template('nvc_swift_structure.html', current_date=current_date)

@swift_docs_bp.route('/swift-structure/pdf')
def swift_structure_pdf():
    """Generate and serve PDF version of the SWIFT structure documentation"""
    try:
        current_date = datetime.now().strftime('%B %d, %Y')
        
        # Render the HTML template
        html = render_template('nvc_swift_structure.html', current_date=current_date)
        
        # PDF generation options
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'print-media-type': None,
            'disable-smart-shrinking': None,
            'header-html': None,
            'footer-center': 'NVC Fund Bank - Global SWIFT Structure | Page [page] of [topage]',
            'footer-font-size': '9',
            'footer-spacing': '5'
        }
        
        # Generate PDF
        pdf = pdfkit.from_string(html, False, options=options)
        
        # Create response
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="NVC_Fund_Bank_Global_SWIFT_Structure_{datetime.now().strftime("%Y%m%d")}.pdf"'
        
        return response
        
    except Exception as e:
        # Fallback: serve HTML version if PDF generation fails
        current_date = datetime.now().strftime('%B %d, %Y')
        return render_template('nvc_swift_structure.html', current_date=current_date)

@swift_docs_bp.route('/swift-codes/summary')
def swift_codes_summary():
    """API endpoint returning summary of all NVC SWIFT codes"""
    from nvc_sovereign_swift_codes import get_sovereign_swift_summary
    
    summary = get_sovereign_swift_summary()
    return {
        'institution': 'NVC Fund Bank',
        'authority': 'African Union Supranational Sovereign Institution',
        'total_swift_codes': summary['total_codes'],
        'geographic_coverage': summary['geographic_coverage'],
        'service_capabilities': summary['service_capabilities'],
        'generated': datetime.now().isoformat()
    }