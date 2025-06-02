from flask import Blueprint, jsonify, request
from app import db
from app.models import Service, User, ServiceImage
from flask_login import login_required, current_user
from app.forms import ServiceForm
from app.api.s3_helper import upload_file_tos3, get_unique_filename

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


@service_routes.route('/', methods=['POST'])
@login_required
def create_service():
    """
    Create a new service
    """
    form = ServiceForm()
    form['csrf_token'].data = request.cookies.get('csrf_token')
    print("Form data:", form.data)
    if form.validate_on_submit():
        try:
            service = Service(
                name=form.data['name'],
                description=form.data['description'],
                price=form.data['price'],
                details=form.data['details']
            )
            db.session.add(service)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Failed to create service", "details": str(e)}), 500

        # Handle image uploads from request.files (not form.data)
        if form.data['image']:
            image = form.data['image']
            image.filename = get_unique_filename(image.filename)
            upload_response = upload_file_tos3(image)
            print(upload_response)

            if "url" not in upload_response:
                    db.session.rollback()
                    return jsonify({"error": "Failed to upload image", "details": upload_response.get("errors", "Unknown error")}), 500

            service_image = ServiceImage(
                service_id=service.id,
                s3_url=upload_response['url']
            )

            db.session.add(service_image)
            db.session.commit()
        else:
            service_image = ServiceImage(
                service_id=service.id,
                s3_url=None
            )
            db.session.add(service_image)
            db.session.commit()
        return jsonify(service.to_dict()), 201
    return jsonify(form.errors), 400
