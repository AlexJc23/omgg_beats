from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app import db
from app.models import Appointment, Service
from sqlalchemy import extract, func
from datetime import datetime, timedelta
import calendar


analytics_routes = Blueprint('analytics', __name__)

@analytics_routes.route('/monthly', methods=['GET'])
@login_required
def get_appointment_count():
    """
    Get the total number of completed appointments and revenue for the current user for a given month.
    """
    if current_user.role not in {'admin', 'owner'}:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json(silent=True) or {}
    selected_month = data.get('date')
    if not selected_month:
        return jsonify({"error": "Missing 'date' parameter (format: YYYY-MM)"}), 400

    try:
        year, month = map(int, selected_month.split('-'))
        start_date = datetime(year, month, 1)
        last_day = calendar.monthrange(year, month)[1]
        end_date = datetime(year, month, last_day, 23, 59, 59)
    except Exception:
        return jsonify({"error": "Invalid 'date' format. Use YYYY-MM."}), 400

    try:
        daily_revenue = (
            db.session.query(
                func.date(Appointment.appointment_date).label('day'),
                func.sum(Service.price).label('total')
            )
            .join(Service)
            .filter(
                Appointment.appointment_date.between(start_date, end_date),
                Appointment.status == 'completed'
            )
            .group_by('day')
            .order_by('day')
            .all()
        )
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    if not daily_revenue:
        return jsonify({"error": "No data found for the selected month"}), 404

    try:
        sales_data = [
            {"date": str(day), "total": float(total)}
            for day, total in daily_revenue
        ]

        monthly_data = {
            "sales_count": len(sales_data),
            "sales_total": sum(item['total'] for item in sales_data),
            "sales": sales_data
        }
    except Exception as e:
        return jsonify({"error": "Data processing error", "details": str(e)}), 500

    return jsonify({"summary": monthly_data}), 200
