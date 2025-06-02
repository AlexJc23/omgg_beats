from flask import Blueprint, jsonify, request
from app import db
from app.models import Service, User, ServiceImage
from flask_login import login_required, current_user
from app.forms import ServiceForm
from app.api.s3_helper import upload_file_tos3, get_unique_filename, remove_file_from_s3

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

    if form.validate_on_submit():
        # Check if a service with the same name already exists
        existing_service = Service.query.filter_by(name=form.data['name']).first()
        if existing_service:
            return jsonify({"error": "A service with this name already exists."}), 409

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


@service_routes.route('/<int:service_id>', methods=['DELETE'])
@login_required
def delete_service(service_id):
    """
    Delete a service by ID
    """
    if current_user.role != 'admin' and current_user.role != 'owner':
        return jsonify({"error": "Unauthorized"}), 403

    if not isinstance(service_id, int) or service_id <= 0:
        return jsonify({"error": "Invalid service ID"}), 400

    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    # Remove associated images from S3
    images = ServiceImage.query.filter_by(service_id=service.id).all()
    if not images:
        pass
    for image in images:
        if image.s3_url:
            remove_response = remove_file_from_s3(image.s3_url)
            if isinstance(remove_response, dict) and "errors" in remove_response:
                db.session.rollback()
                return jsonify({"error": "Failed to delete image from S3", "details": remove_response["errors"]}), 500
        db.session.delete(image)
    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted successfully"}), 200

@service_routes.route('/<int:service_id>', methods=['PUT'])
@login_required
def edit_service(service_id):
    """
    Edit a service by ID
    """
    try:
        if current_user.role != 'admin' and current_user.role != 'owner':
            return jsonify({"error": "Unauthorized"}), 403

        if not isinstance(service_id, int) or service_id <= 0:
            return jsonify({"error": "Invalid service ID"}), 400

        service = db.session.query(Service).get(service_id)
        if not service:
            return jsonify({"error": "Service not found"}), 404


        form = ServiceForm()
        form['csrf_token'].data = request.cookies.get('csrf_token')

        if form.validate_on_submit():
            # Check if a service with the same name already exists
            existing_service = Service.query.filter(Service.name == form.data['name'], Service.id != service_id).first()

            if existing_service:
                return jsonify({"error": "A service with this name already exists."}), 409

            try:
                service.name = form.data['name']
                service.description = form.data['description']
                service.price = form.data['price']
                service.details = form.data['details']
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": "Failed to update service", "details": str(e)}), 500


            if form.data.get('image'):
                image = form.data['image']
                image.filename = get_unique_filename(image.filename)
                upload_response = upload_file_tos3(image)

                if "url" not in upload_response:
                    db.session.rollback()
                    return jsonify({"error": "Failed to upload image", "details": upload_response.get("errors", "Unknown error")}), 500

                # Remove old images from S3
                images = ServiceImage.query.filter_by(service_id=service.id).all()
                for img in images:
                    img_by_id = ServiceImage.query.get(img.id)
                    if img.s3_url:
                        remove_response = remove_file_from_s3(img.s3_url)
                        if isinstance(remove_response, dict) and "errors" in remove_response:
                            db.session.rollback()
                            return jsonify({"error": "Failed to delete old image from S3", "details": remove_response["errors"]}), 500
                    db.session.delete(img_by_id)
                    db.session.commit()

                # Add new image
                new_image = ServiceImage(
                    service_id=service.id,
                    s3_url=upload_response['url']
                )
                db.session.add(new_image)
                db.session.commit()
            else:
                # If no new image is uploaded, keep the existing images
                pass
            return jsonify(service.to_dict()), 200
        else:
            return jsonify({"error": "Validation failed", "details": form.errors}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
