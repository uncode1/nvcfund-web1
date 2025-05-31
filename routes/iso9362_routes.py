"""
ISO 9362:2022 BIC Management Routes for NVC Banking Platform
Enhanced SWIFT Business Identifier Code functionality
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from iso9362_implementation import (
    ISO9362Validator, BICRegistry, SWIFTMessageRouter, 
    BICInfo, BICType, BICStatus, initialize_nvc_bic_registry
)
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
iso9362_bp = Blueprint('iso9362', __name__, url_prefix='/iso9362')

# Initialize BIC registry
try:
    bic_registry = initialize_nvc_bic_registry()
    swift_router = SWIFTMessageRouter(bic_registry)
    logger.info("ISO 9362:2022 BIC registry initialized successfully")
except Exception as e:
    logger.error(f"Error initializing BIC registry: {str(e)}")
    bic_registry = None
    swift_router = None

@iso9362_bp.route('/')
def bic_dashboard():
    """BIC management dashboard"""
    try:
        # Get BIC statistics
        stats = {
            'total_bics': 0,
            'active_bics': 0,
            'countries': 0,
            'institution_types': 0
        }
        
        if bic_registry:
            # In a real implementation, you'd query the database for stats
            stats = {
                'total_bics': 5,  # NVC + 4 correspondent banks
                'active_bics': 5,
                'countries': 4,   # GL, US, DE, GB
                'institution_types': 2  # Institution, Correspondent
            }
        
        return render_template('iso9362/dashboard.html', stats=stats)
    except Exception as e:
        logger.error(f"Error loading BIC dashboard: {str(e)}")
        flash('Error loading BIC dashboard', 'error')
        return redirect(url_for('main.index'))

@iso9362_bp.route('/validate', methods=['GET', 'POST'])
def validate_bic():
    """BIC validation tool"""
    validation_result = None
    
    if request.method == 'POST':
        bic_code = request.form.get('bic_code', '').strip().upper()
        
        if bic_code:
            try:
                # Validate BIC format
                is_valid, message = ISO9362Validator.validate_bic(bic_code)
                
                # Parse BIC components if valid
                components = None
                registry_info = None
                
                if is_valid:
                    components = ISO9362Validator.parse_bic(bic_code)
                    if bic_registry:
                        registry_info = bic_registry.lookup_bic(bic_code)
                
                validation_result = {
                    'bic_code': bic_code,
                    'is_valid': is_valid,
                    'message': message,
                    'components': components,
                    'registry_info': registry_info
                }
                
            except Exception as e:
                logger.error(f"Error validating BIC {bic_code}: {str(e)}")
                validation_result = {
                    'bic_code': bic_code,
                    'is_valid': False,
                    'message': f'Validation error: {str(e)}',
                    'components': None,
                    'registry_info': None
                }
    
    return render_template('iso9362/validate.html', result=validation_result)

@iso9362_bp.route('/lookup/<bic_code>')
def lookup(bic_code):
    """Lookup BIC information"""
    try:
        if not bic_registry:
            return jsonify({'error': 'BIC registry not available'}), 500
        
        # Validate BIC format first
        is_valid, message = ISO9362Validator.validate_bic(bic_code)
        if not is_valid:
            return jsonify({'error': f'Invalid BIC format: {message}'}), 400
        
        # Lookup in registry
        bic_info = bic_registry.lookup_bic(bic_code)
        
        if bic_info:
            return jsonify({
                'bic_code': bic_info.bic_code,
                'institution_name': bic_info.institution_name,
                'country_code': bic_info.country_code,
                'location_code': bic_info.location_code,
                'branch_code': bic_info.branch_code,
                'bic_type': bic_info.bic_type.value,
                'status': bic_info.status.value,
                'services': bic_info.services,
                'connectivity_status': bic_info.connectivity_status,
                'last_updated': bic_info.last_updated.isoformat()
            })
        else:
            return jsonify({'error': 'BIC not found in registry'}), 404
            
    except Exception as e:
        logger.error(f"Error looking up BIC {bic_code}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@iso9362_bp.route('/register', methods=['GET', 'POST'])
def register_bic():
    """Register new BIC code"""
    if request.method == 'POST':
        try:
            # Get form data
            bic_code = request.form.get('bic_code', '').strip().upper()
            institution_name = request.form.get('institution_name', '').strip()
            bic_type = request.form.get('bic_type', BICType.INSTITUTION.value)
            services = request.form.getlist('services')
            connectivity_status = request.form.get('connectivity_status', 'PENDING')
            
            # Validate required fields
            if not all([bic_code, institution_name]):
                flash('BIC code and institution name are required', 'error')
                return render_template('iso9362/register.html')
            
            # Validate BIC format
            is_valid, message = ISO9362Validator.validate_bic(bic_code)
            if not is_valid:
                flash(f'Invalid BIC format: {message}', 'error')
                return render_template('iso9362/register.html')
            
            # Parse BIC components
            components = ISO9362Validator.parse_bic(bic_code)
            
            # Create BIC info object
            bic_info = BICInfo(
                bic_code=bic_code,
                institution_name=institution_name,
                institution_code=components['institution_code'],
                country_code=components['country_code'],
                location_code=components['location_code'],
                branch_code=components['branch_code'],
                bic_type=BICType(bic_type),
                status=BICStatus.ACTIVE,
                registration_date=datetime.now(),
                last_updated=datetime.now(),
                services=services,
                connectivity_status=connectivity_status
            )
            
            # Register in registry
            if bic_registry and bic_registry.register_bic(bic_info):
                flash(f'BIC {bic_code} registered successfully', 'success')
                return redirect(url_for('iso9362.lookup_bic', bic_code=bic_code))
            else:
                flash('Error registering BIC', 'error')
                
        except Exception as e:
            logger.error(f"Error registering BIC: {str(e)}")
            flash(f'Registration error: {str(e)}', 'error')
    
    return render_template('iso9362/register.html')

@iso9362_bp.route('/search')
def search_bics():
    """Search BIC codes"""
    country_code = request.args.get('country', '').strip().upper()
    results = []
    
    if country_code and bic_registry:
        try:
            results = bic_registry.search_by_country(country_code)
        except Exception as e:
            logger.error(f"Error searching BICs by country {country_code}: {str(e)}")
            flash('Error searching BIC codes', 'error')
    
    return render_template('iso9362/search.html', 
                         country_code=country_code, 
                         results=results)

@iso9362_bp.route('/routing', methods=['GET', 'POST'])
def swift_routing():
    """SWIFT message routing tool"""
    routing_result = None
    
    if request.method == 'POST':
        sender_bic = request.form.get('sender_bic', '').strip().upper()
        receiver_bic = request.form.get('receiver_bic', '').strip().upper()
        message_type = request.form.get('message_type', 'MT103')
        
        if sender_bic and receiver_bic and swift_router:
            try:
                routing_result = swift_router.route_message(
                    sender_bic, receiver_bic, message_type
                )
            except Exception as e:
                logger.error(f"Error routing message: {str(e)}")
                routing_result = {
                    'status': 'error',
                    'errors': [f'Routing error: {str(e)}']
                }
    
    return render_template('iso9362/routing.html', result=routing_result)

@iso9362_bp.route('/api/validate/<bic_code>')
def api_validate_bic(bic_code):
    """API endpoint for BIC validation"""
    try:
        is_valid, message = ISO9362Validator.validate_bic(bic_code)
        
        response = {
            'bic_code': bic_code.upper(),
            'is_valid': is_valid,
            'message': message
        }
        
        if is_valid:
            response['components'] = ISO9362Validator.parse_bic(bic_code)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'bic_code': bic_code,
            'is_valid': False,
            'message': f'Validation error: {str(e)}'
        }), 500

@iso9362_bp.route('/api/route', methods=['POST'])
def api_route_message():
    """API endpoint for SWIFT message routing"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['sender_bic', 'receiver_bic']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if not swift_router:
            return jsonify({'error': 'SWIFT router not available'}), 500
        
        routing_result = swift_router.route_message(
            data['sender_bic'],
            data['receiver_bic'],
            data.get('message_type', 'MT103')
        )
        
        return jsonify(routing_result)
        
    except Exception as e:
        logger.error(f"API routing error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@iso9362_bp.route('/correspondent-banks')
def correspondent_banks():
    """View correspondent banking relationships"""
    try:
        # Get correspondent banks (BIC type = CORRESPONDENT)
        correspondents = []
        
        if bic_registry:
            # In a full implementation, you'd query the database
            # For now, return the correspondent banks we registered
            correspondent_bics = ['CHASUS33', 'CITIUS33', 'DEUTDEFF', 'HSBCGB2L']
            
            for bic_code in correspondent_bics:
                bic_info = bic_registry.lookup_bic(bic_code)
                if bic_info:
                    correspondents.append(bic_info)
        
        return render_template('iso9362/correspondents.html', 
                             correspondents=correspondents)
        
    except Exception as e:
        logger.error(f"Error loading correspondent banks: {str(e)}")
        flash('Error loading correspondent banks', 'error')
        return redirect(url_for('iso9362.bic_dashboard'))

# Error handlers
@iso9362_bp.errorhandler(404)
def not_found_error(error):
    return render_template('iso9362/error.html', 
                         error_code=404, 
                         error_message="Page not found"), 404

@iso9362_bp.errorhandler(500)
def internal_error(error):
    return render_template('iso9362/error.html', 
                         error_code=500, 
                         error_message="Internal server error"), 500