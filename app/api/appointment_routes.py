from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app import db
from app.models import Appointment, Service, User
from datetime import datetime, date, time, timedelta
from app.forms import AppointmentForm

appointment_routes = Blueprint('appointments', __name__)




@appointment_routes.route('/')
@login_required
def get_appointments():
    """
    Get all appointments for the current user, optionally filtered by a date range.
    """

    # Get query parameters
    begin_date_str = request.args.get('begin_date')
    end_date_str = request.args.get('end_date')

    # Parse or default date range
    try:
        begin_date = datetime.fromisoformat(begin_date_str).date() if begin_date_str else datetime.utcnow().date()
        end_date = datetime.fromisoformat(end_date_str).date() if end_date_str else begin_date + timedelta(weeks=2)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Base query
    query = Appointment.query.filter(
        Appointment.appointment_date >= begin_date,
        Appointment.appointment_date <= end_date
    )

    # Filter by user if not admin
    if current_user.role == 'user':
        query = query.filter_by(user_id=current_user.id)

    appointments = query.all()

    if not appointments:
        return jsonify({"error": "No appointments found"}), 404

    # Convert appointments to a list of dictionaries
    appointments_list = [
        {
            "id": appt.id,
            "user_id": appt.user_id,
            "service_id": appt.service_id,
            "appointment_date": appt.appointment_date.isoformat(),
            "status": appt.status,
            "created_at": appt.created_at.isoformat(),
            "updated_at": appt.updated_at.isoformat(),
            "service_name": appt.service.name if appt.service else None,
        } for appt in appointments
    ]

    return jsonify(appointments_list), 200


@appointment_routes.route('/<int:id>', methods=['POST'])
@login_required
def create_appointment(id):
    """
    Create a new appointment for the current user.
    """
    service = Service.query.get(id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    form = AppointmentForm()
    form['csrf_token'].data = request.cookies.get('csrf_token')

    if form.validate_on_submit():
        # Parse the datetime string from the form
        try:
            appointment_datetime = datetime.strptime(form.data['appointment_date'], "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({"error": "Invalid datetime format. Use 'YYYY-MM-DD HH:MM'."}), 400

        # Check for existing appointment at the same datetime for the user
        existing = Appointment.query.filter_by(
            appointment_date=appointment_datetime
        ).first()

        if existing:
            return jsonify({"error": "This time slot is unavailable"}), 400

        try:
            appointment = Appointment(
                user_id=current_user.id,
                service_id=id,
                appointment_date=appointment_datetime,
                status='pending'
            )
            db.session.add(appointment)
            db.session.commit()
            return jsonify(appointment.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Failed to create appointment", "details": str(e)}), 500
    else:
        return jsonify({"errors": form.errors}), 400


@appointment_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_appointment(id):
    """
    Update an existing appointment.
    """
    appoint_by_id = Appointment.query.get(id)
    if not appoint_by_id:
        return jsonify({"error": "Appointment not found"}), 404
    if appoint_by_id.user_id != current_user.id and current_user.role != 'admin':
        return jsonify({"error": "Unauthorized to update this appointment"}), 403

    data = request.get_json(silent=True) or {}
    appointment_status = data.get('status')
    if appointment_status not in {'pending', 'completed', 'cancelled'}:
        return jsonify({"error": "Invalid status"}), 400

    try:
        appoint_by_id.status = appointment_status
        db.session.commit()
        return jsonify({"message": "Appointment updated successfully", "appointment": appoint_by_id.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update appointment", "details": str(e)}), 500
