"""
Health check endpoint for the flight service.
Add this to your Flask application to verify deployment status.
"""
from flask import Blueprint, jsonify
import os
from datetime import datetime

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring and deployment verification.
    Returns service status and basic information.
    """
    return jsonify({
        'status': 'healthy',
        'service': 'flight-service',
        'environment': os.getenv('FLASK_ENV', 'unknown'),
        'timestamp': datetime.utcnow().isoformat(),
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'server': 'gunicorn' if os.getenv('FLASK_ENV') == 'production' else 'werkzeug'
    }), 200

@health_bp.route('/health/ready', methods=['GET'])
def readiness_check():
    """
    Readiness check - verifies if the service is ready to accept traffic.
    Checks database connectivity.
    """
    checks = {
        'database': False
    }
    
    try:
        # Check database connection
        from app import db
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        checks['database'] = True
    except Exception as e:
        pass
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return jsonify({
        'ready': all_healthy,
        'checks': checks,
        'timestamp': datetime.utcnow().isoformat()
    }), status_code

@health_bp.route('/health/live', methods=['GET'])
def liveness_check():
    """
    Liveness check - verifies if the service is alive.
    Simple check that always returns 200 if the app is running.
    """
    return jsonify({
        'alive': True,
        'timestamp': datetime.utcnow().isoformat()
    }), 200
