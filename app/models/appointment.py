from datetime import datetime
from .db import db, environment, SCHEMA, add_prefix_for_prod


class Appointment(db.Model):
    __tablename__ = 'appointments'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('services.id')), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now, nullable=False)

    user = db.relationship("User", back_populates="appointments")
    service = db.relationship("Service", back_populates="appointments")


    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "service_id": self.service_id,
            "appointment_date": self.appointment_date.strftime("%Y-%m-%d %H:%M"),
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "service_name": self.service.name if self.service else None,
        }
