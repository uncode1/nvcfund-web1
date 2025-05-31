"""
Routes package for NVC Banking Platform
"""

from flask import Blueprint

# Import API routes
from routes.api.blockchain_routes import blockchain_api
from routes.api.xrp_routes import xrp_api
from routes.api.ha_routes import ha_api
from routes.api.status_routes import status_bp
from routes.api.form_data_routes import form_data
from routes.api.form_save_routes import form_save
from routes.api.token_exchange_routes import token_exchange_api
from routes.api.treasury_api import treasury_api_bp
from routes.high_availability_routes import ha_web
from routes.main_routes import main
from routes.swift_routes import swift
from routes.ach_routes import ach
from routes.api_access_routes import api_access_bp
from routes.institutional_routes import institutional_bp
from routes.correspondent_banking_routes import correspondent
from routes.recapitalization_routes import recapitalization
from routes.sblc_routes import sblc_bp  # Import our new SBLC routes

# Import payment and transaction routes
from routes.payment_history_routes import payment_history_bp
from routes.pdf_receipt_routes import pdf_receipt_bp

# Import PHP Bridge routes
from api_bridge import php_bridge

# Temporarily disabled RTGS routes
# from routes.rtgs_routes import rtgs_routes

# Create API blueprint
api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# Create Web blueprint (for pages that should be under a prefix)
web_blueprint = Blueprint('web', __name__)

# Register API route blueprints
api_blueprint.register_blueprint(blockchain_api, url_prefix='/blockchain')
api_blueprint.register_blueprint(xrp_api, url_prefix='/v1/xrp')
api_blueprint.register_blueprint(ha_api, url_prefix='/v1/ha')
api_blueprint.register_blueprint(status_bp)
api_blueprint.register_blueprint(php_bridge, url_prefix='/php-bridge')
api_blueprint.register_blueprint(form_data)
api_blueprint.register_blueprint(form_save)
api_blueprint.register_blueprint(token_exchange_api, url_prefix='/v1/token-exchange')
api_blueprint.register_blueprint(treasury_api_bp, url_prefix='/treasury')

# Register Web route blueprints
web_blueprint.register_blueprint(ha_web, url_prefix='/ha')
web_blueprint.register_blueprint(main, url_prefix='/main')
web_blueprint.register_blueprint(swift, url_prefix='/swift')
web_blueprint.register_blueprint(ach, url_prefix='/ach')
web_blueprint.register_blueprint(correspondent, url_prefix='/correspondent')
web_blueprint.register_blueprint(institutional_bp, url_prefix='/institutional')
# SBLC routes are registered directly in app.py, not here
web_blueprint.register_blueprint(payment_history_bp)
web_blueprint.register_blueprint(pdf_receipt_bp)