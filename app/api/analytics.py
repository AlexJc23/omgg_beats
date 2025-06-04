from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app import db
from app.models import Appointment, Service
from sqlalchemy import extract, func
from datetime import datetime
import calendar

analytics_routes = Blueprint('analytics', __name__)

def parse_date_param(date_str, fmt):
    try:
        if fmt == 'month':
            year, month = map(int, date_str.split('-'))
            start_date = datetime(year, month, 1)
            last_day = calendar.monthrange(year, month)[1]
            end_date = datetime(year, month, last_day, 23, 59, 59)
        elif fmt == 'year':
            year = int(date_str)
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31, 23, 59, 59)
        else:
            raise ValueError
        return start_date, end_date
    except Exception:
        return None, None

def check_admin_owner():
    if current_user.role not in {'admin', 'owner'}:
        return jsonify({"error": "Unauthorized"}), 403
    return None

def get_request_date(fmt):
    data = request.get_json(silent=True) or {}
    date_param = data.get('date')
    if not date_param:
        return None, jsonify({"error": f"Missing 'date' parameter (format: {'YYYY-MM' if fmt == 'month' else 'YYYY'})"}), 400
    start_date, end_date = parse_date_param(date_param, fmt)
    if not start_date:
        return None, jsonify({"error": f"Invalid 'date' format. Use {'YYYY-MM' if fmt == 'month' else 'YYYY'}."}), 400
    return (start_date, end_date), None, None

@analytics_routes.route('/monthly', methods=['GET'])
@login_required
def get_monthly_analytics():
    unauthorized = check_admin_owner()
    if unauthorized:
        return unauthorized

    (dates, err_resp, err_code) = get_request_date('month')
    if err_resp:
        return err_resp, err_code
    start_date, end_date = dates

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

@analytics_routes.route('/services', methods=['GET'])
@login_required
def get_daily_analytics():
    unauthorized = check_admin_owner()
    if unauthorized:
        return unauthorized

    (dates, err_resp, err_code) = get_request_date('month')
    if err_resp:
        return err_resp, err_code
    start_date, end_date = dates

    daily_services = (
        db.session.query(Appointment, Service.name).filter(
            Appointment.appointment_date.between(start_date, end_date),
            Appointment.status == 'completed'
        )).join(Service).all()

    if not daily_services:
        return jsonify({"error": "No data found for the selected month"}), 404

    service_names = db.session.query(Service.name).all()
    hashmap = {service[0]: 0 for service in service_names}

    for service in daily_services:
        if service[1] in hashmap:
            hashmap[service[1]] += 1

    return jsonify({"service_analytics": hashmap}), 200

@analytics_routes.route('/yearly', methods=['GET'])
@login_required
def get_yearly_analytics():
    unauthorized = check_admin_owner()
    if unauthorized:
        return unauthorized

    (dates, err_resp, err_code) = get_request_date('year')
    if err_resp:
        return err_resp, err_code
    start_date, end_date = dates

    try:
        monthly_revenue = (
            db.session.query(
                extract('month', Appointment.appointment_date).label('month'),
                func.sum(Service.price).label('total')
            )
            .join(Service)
            .filter(
                Appointment.appointment_date.between(start_date, end_date),
                Appointment.status == 'completed'
            )
            .group_by('month')
            .order_by('month')
            .all()
        )
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    if not monthly_revenue:
        return jsonify({"error": "No data found for the selected year"}), 404

    try:
        sales_data = [
            {"month": month, "total": float(total)}
            for month, total in monthly_revenue
        ]
        yearly_data = {
            "sales_count": len(sales_data),
            "sales_total": sum(item['total'] for item in sales_data),
            "sales": sales_data
        }
    except Exception as e:
        return jsonify({"error": "Data processing error", "details": str(e)}), 500

    return jsonify({"summary": yearly_data}), 200
