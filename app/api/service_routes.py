from flask import Blueprint, jsonify, request
from app import db
from app.models import Service, User
from flask_login import login_required, current_user

service_routes = Blueprint('services', __name__)

@service_routes.route('/')
def get_all_services():
    """
    Get all services
    """
    services = Service.query.all()
    return jsonify([service.to_dict() for service in services]), 200

@service_routes.route('/<int:service_id>')
def get_service(service_id):
    """
    Get a specific service by ID
    """
    if not isinstance(service_id, int) or service_id <= 0:
        return jsonify({"error": "Invalid service ID"}), 400

    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    return jsonify(service.to_dict()), 200


