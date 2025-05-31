"""
PDF Download Routes for NVC Banking Platform
"""
from flask import Blueprint, send_file, flash, redirect, url_for
import os

pdf_download_bp = Blueprint('pdf_download', __name__)

@pdf_download_bp.route('/download/swift-documentation')
def download_swift_pdf():
    """Download SWIFT Documentation PDF directly"""
    try:
        # Check both possible locations for the PDF
        pdf_locations = [
            'NVC_Fund_Bank_SWIFT_Documentation.pdf',
            'static/NVC_Fund_Bank_SWIFT_Documentation.pdf'
        ]
        
        for pdf_path in pdf_locations:
            if os.path.exists(pdf_path):
                return send_file(
                    pdf_path, 
                    as_attachment=True, 
                    download_name='NVC_Fund_Bank_SWIFT_Documentation.pdf',
                    mimetype='application/pdf'
                )
        
        # If PDF not found, return error message
        flash('SWIFT Documentation PDF not found. Please generate it first.', 'error')
        return redirect('/')
        
    except Exception as e:
        flash(f'Error downloading PDF: {str(e)}', 'error')
        return redirect('/')