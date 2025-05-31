"""
Direct SWIFT PDF Download Route - Bypasses All Caching
"""
from flask import Blueprint, send_file, make_response
import os
from datetime import datetime

swift_pdf_bp = Blueprint('swift_pdf', __name__)

@swift_pdf_bp.route('/download-capacity-report')
def download_capacity_report():
    """Download NVC Fund Bank Capacity and Capability Report"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path = os.path.join('static', 'NVC_Fund_Bank_Capacity_Report_Branded.pdf')
        
        if os.path.exists(pdf_path):
            response = make_response(
                send_file(
                    pdf_path,
                    as_attachment=True,
                    download_name=f'NVC_Fund_Bank_Capacity_Report_{timestamp}.pdf',
                    mimetype='application/pdf'
                )
            )
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
        else:
            return "Capacity report not found", 404
    except Exception as e:
        return f"Error downloading report: {str(e)}", 500

@swift_pdf_bp.route('/download-swift-pdf-new')
def download_new_swift_pdf():
    """Force download of the latest SWIFT documentation with timestamp"""
    try:
        # Get current timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Path to the branded professional PDF
        pdf_path = os.path.join('static', 'NVC_Fund_Bank_SWIFT_Documentation_Branded.pdf')
        
        if os.path.exists(pdf_path):
            # Create response with forced download
            response = make_response(
                send_file(
                    pdf_path,
                    as_attachment=True,
                    download_name=f'NVC_Fund_Bank_SWIFT_Documentation_Professional_{timestamp}.pdf',
                    mimetype='application/pdf'
                )
            )
            
            # Strong cache-busting headers
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            response.headers['ETag'] = f'swift-pdf-{timestamp}'
            response.headers['Last-Modified'] = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
            
            return response
        else:
            return "Professional SWIFT PDF not found", 404
            
    except Exception as e:
        return f"Error downloading PDF: {str(e)}", 500