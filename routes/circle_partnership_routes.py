"""
Circle Partnership Routes for NVC Banking Platform
Provides access to Circle strategic partnership materials and presentations
"""

from flask import Blueprint, render_template, send_file, jsonify, request
from flask_login import login_required
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint
circle_bp = Blueprint('circle_partnership', __name__, url_prefix='/circle')

@circle_bp.route('/')
def partnership_overview():
    """Circle partnership overview and materials access"""
    try:
        return render_template('circle_partnership/overview.html',
                             title="Circle Strategic Partnership")
    except Exception as e:
        logger.error(f"Error loading Circle partnership overview: {str(e)}")
        return render_template('error.html', 
                             error="Unable to load Circle partnership materials"), 500

@circle_bp.route('/presentation')
def interactive_presentation():
    """Interactive HTML presentation for Circle partnership"""
    try:
        return render_template('circle_presentation.html',
                             title="Circle Strategic Partnership Presentation")
    except Exception as e:
        logger.error(f"Error loading Circle presentation: {str(e)}")
        return render_template('error.html', 
                             error="Unable to load presentation"), 500

@circle_bp.route('/powerpoint')
@login_required
@require_role(['ADMIN', 'OPERATOR'])
def powerpoint_presentation():
    """PowerPoint-style presentation for Circle partnership"""
    try:
        return render_template('circle_presentation.pptx.html',
                             title="Circle Partnership - PowerPoint Format")
    except Exception as e:
        logger.error(f"Error loading PowerPoint presentation: {str(e)}")
        return render_template('error.html', 
                             error="Unable to load PowerPoint presentation"), 500

@circle_bp.route('/documents')
@login_required
@require_role(['ADMIN', 'OPERATOR'])
def partnership_documents():
    """Access to all Circle partnership documents"""
    try:
        documents = [
            {
                'name': 'Strategic Partnership Analysis',
                'description': 'Comprehensive analysis of Circle company and partnership opportunities',
                'file': 'circle_partnership_analysis.md',
                'type': 'Analysis'
            },
            {
                'name': 'Acquisition & Partnership Term Sheet',
                'description': 'Detailed term sheets for acquisition and partnership options',
                'file': 'circle_acquisition_partnership_termsheet.md',
                'type': 'Legal'
            },
            {
                'name': 'Executive Presentation Materials',
                'description': 'Complete presentation materials for Circle leadership outreach',
                'file': 'circle_executive_presentation.md',
                'type': 'Presentation'
            },
            {
                'name': 'CEO Talking Points',
                'description': 'Strategic talking points for CEO-level conversations',
                'file': 'circle_ceo_talking_points.md',
                'type': 'Strategy'
            }
        ]
        
        return render_template('circle_partnership/documents.html',
                             title="Circle Partnership Documents",
                             documents=documents)
    except Exception as e:
        logger.error(f"Error loading Circle documents: {str(e)}")
        return render_template('error.html', 
                             error="Unable to load partnership documents"), 500

@circle_bp.route('/download/<filename>')
@login_required
@require_role(['ADMIN', 'OPERATOR'])
def download_document(filename):
    """Download Circle partnership documents"""
    try:
        # Security check - only allow specific files
        allowed_files = [
            'circle_partnership_analysis.md',
            'circle_acquisition_partnership_termsheet.md',
            'circle_executive_presentation.md',
            'circle_ceo_talking_points.md'
        ]
        
        if filename not in allowed_files:
            return jsonify({'error': 'File not found'}), 404
        
        file_path = os.path.join('.', filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'File not found'}), 404
            
    except Exception as e:
        logger.error(f"Error downloading Circle document {filename}: {str(e)}")
        return jsonify({'error': 'Download failed'}), 500

@circle_bp.route('/valuation-calculator')
@login_required
@require_role(['ADMIN', 'OPERATOR'])
def valuation_calculator():
    """Interactive valuation calculator for Circle acquisition"""
    try:
        return render_template('circle_partnership/valuation_calculator.html',
                             title="Circle Valuation Calculator")
    except Exception as e:
        logger.error(f"Error loading valuation calculator: {str(e)}")
        return render_template('error.html', 
                             error="Unable to load valuation calculator"), 500

@circle_bp.route('/api/calculate-valuation', methods=['POST'])
@login_required
@require_role(['ADMIN', 'OPERATOR'])
def calculate_valuation():
    """API endpoint for Circle valuation calculations"""
    try:
        data = request.get_json()
        
        # Get parameters
        usdc_circulation = float(data.get('usdc_circulation', 40000000000))  # $40B default
        annual_revenue = float(data.get('annual_revenue', 300000000))  # $300M default
        revenue_multiple = float(data.get('revenue_multiple', 12))  # 12x default
        strategic_premium = float(data.get('strategic_premium', 0.25))  # 25% default
        
        # Calculate base valuation
        revenue_valuation = annual_revenue * revenue_multiple
        aum_valuation = usdc_circulation * 0.02  # 2% of AUM
        base_valuation = max(revenue_valuation, aum_valuation)
        
        # Apply strategic premium
        strategic_valuation = base_valuation * (1 + strategic_premium)
        
        # Calculate deal structure
        cash_component = strategic_valuation * 0.42  # 42% cash
        equity_component = strategic_valuation * 0.33  # 33% equity
        earnout_component = strategic_valuation * 0.25  # 25% earnouts
        
        result = {
            'base_valuation': base_valuation,
            'strategic_valuation': strategic_valuation,
            'deal_structure': {
                'total_value': strategic_valuation,
                'cash': cash_component,
                'equity': equity_component,
                'earnouts': earnout_component
            },
            'metrics': {
                'revenue_multiple': revenue_multiple,
                'aum_percentage': (aum_valuation / usdc_circulation) * 100,
                'strategic_premium_percentage': strategic_premium * 100
            }
        }
        
        logger.info(f"Circle valuation calculated: ${strategic_valuation:,.0f}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error calculating Circle valuation: {str(e)}")
        return jsonify({'error': 'Calculation failed'}), 500