from app.models import Appointment, Service, User, environment, SCHEMA, db
from sqlalchemy.sql import text
from datetime import datetime, date, time


def seed_appointments():
    appointment1 = Appointment(
        user_id=1,
        service_id=1,
        appointment_date=datetime(2025, 10, 1, 10, 0),  # 2025-10-01 10:00 AM
        status='pending'
    )
    appointment2 = Appointment(
        user_id=2,
        service_id=2,
        appointment_date=datetime(2025, 10, 2, 14, 30),  # 2025-10-02 2:30 PM
        status='pending'
    )
    appointment3 = Appointment(
        user_id=3,
        service_id=3,
        appointment_date=datetime(2025, 10, 3, 9, 15),  # 2025-10-03 9:15 AM
        status='pending'
    )
    appointment4 = Appointment(
        user_id=1,
        service_id=4,
        appointment_date=datetime(2025, 6, 7, 11, 0),  # 2025-06-07 11:00 AM
        status='pending'
    )

    db.session.add_all([appointment1, appointment2, appointment3, appointment4])
    db.session.commit()

def undo_appointments():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.appointments RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM appointments"))

    db.session.commit()
