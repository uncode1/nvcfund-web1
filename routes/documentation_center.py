"""
NVC Fund Bank Documentation Center Routes
Centralized access to all documentation, reports, and guides
"""
from flask import Blueprint, render_template, send_file, current_app
import os
from datetime import datetime

documentation_center_bp = Blueprint('documentation_center', __name__)

@documentation_center_bp.route('/documentation-center')
def documentation_center():
    """Main documentation center page"""
    
    # Available dual-format documents (HTML + PDF)
    dual_format_docs = [
        {
            'title': 'SWIFT Documentation',
            'description': 'Global SWIFT Structure and Operations Manual',
            'html_url': '/documentation-center/swift-documentation',
            'pdf_file': 'NVC_Fund_Bank_SWIFT_Documentation_Branded.pdf',
            'category': 'Technical Documentation'
        },
        {
            'title': 'Capacity & Capability Report',
            'description': 'Institutional Capacity and Operational Status Assessment',
            'html_url': '/documentation-center/capacity-report',
            'pdf_file': 'NVC_Fund_Bank_Capacity_Report_Branded.pdf',
            'category': 'Institutional Reports'
        }
    ]
    
    # Available operational guides (HTML + PDF)
    operational_guides = [
        {
            'title': 'NVC Funds Transfer Guide',
            'description': 'Complete guide for funds transfer operations',
            'html_url': '/documentation-center/funds-transfer',
            'pdf_file': 'NVC_Funds_Transfer_Guide.pdf',
            'category': 'Operational Guides'
        },
        {
            'title': 'Server-to-Server Integration',
            'description': 'Technical integration guide for developers',
            'html_url': '/documentation-center/server-integration',
            'pdf_file': 'NVC_Server_Integration_Guide.pdf',
            'category': 'Technical Integration'
        },
        {
            'title': 'Transaction Settlement Explainer',
            'description': 'Understanding transaction settlement processes',
            'html_url': '/documentation-center/transaction-settlement',
            'pdf_file': 'NVC_Transaction_Settlement_Guide.pdf',
            'category': 'Operational Guides'
        },
        {
            'title': 'NVC Tokenomics',
            'description': 'NVCT token economics and blockchain integration',
            'html_url': '/documentation-center/tokenomics',
            'pdf_file': 'NVC_Tokenomics_Guide.pdf',
            'category': 'Blockchain & Digital Assets'
        }
    ]
    
    # System documentation
    system_docs = [
        {
            'title': 'ISO 20022 Financial Messaging',
            'description': 'Financial messaging standards implementation',
            'url': '/iso20022',
            'category': 'Compliance & Standards'
        },
        {
            'title': 'ISO 9362:2022 BIC Management',
            'description': 'Business Identifier Code registry and management',
            'url': '/iso9362',
            'category': 'Compliance & Standards'
        },
        {
            'title': 'SWIFT Structure Documentation',
            'description': 'NVC Fund Bank global SWIFT network structure',
            'url': '/documentation-center/swift-structure',
            'category': 'Banking Infrastructure'
        }
    ]
    
    return render_template('documentation_center_new.html',
                         dual_format_docs=dual_format_docs,
                         operational_guides=operational_guides,
                         system_docs=system_docs)

@documentation_center_bp.route('/documentation-center/funds-transfer')
def funds_transfer_guide():
    """NVC Funds Transfer Guide"""
    return render_template('documentation/funds_transfer.html')

@documentation_center_bp.route('/documentation-center/server-integration')
def server_integration_guide():
    """Server-to-Server Integration Guide"""
    return render_template('documentation/server_integration.html')

@documentation_center_bp.route('/documentation-center/transaction-settlement')
def transaction_settlement_guide():
    """Transaction Settlement Explainer"""
    return render_template('documentation/transaction_settlement.html')

@documentation_center_bp.route('/documentation-center/tokenomics')
def tokenomics_guide():
    """NVC Tokenomics Guide"""
    return render_template('documentation/tokenomics.html')

@documentation_center_bp.route('/documentation-center/swift-structure')
def swift_structure_guide():
    """SWIFT Structure Documentation"""
    return render_template('documentation/swift_structure.html')

@documentation_center_bp.route('/documentation-center/swift-documentation')
def swift_documentation():
    """SWIFT Documentation HTML Version"""
    current_date = datetime.now().strftime("%B %d, %Y")
    return render_template('documentation/swift_documentation.html', current_date=current_date)

@documentation_center_bp.route('/documentation-center/capacity-report')
def capacity_report():
    """Capacity Report HTML Version"""
    current_date = datetime.now().strftime("%B %d, %Y")
    return render_template('documentation/capacity_report.html', current_date=current_date)

@documentation_center_bp.route('/download-pdf/<filename>')
def download_pdf(filename):
    """Download PDF documents"""
    try:
        pdf_path = os.path.join('static', filename)
        if os.path.exists(pdf_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f'{filename.replace(".pdf", "")}_{timestamp}.pdf',
                mimetype='application/pdf'
            )
        else:
            return "Document not found", 404
    except Exception as e:
        current_app.logger.error(f"Error downloading PDF {filename}: {str(e)}")
        return f"Error downloading document: {str(e)}", 500