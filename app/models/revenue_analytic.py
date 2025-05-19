from datetime import datetime
from .db import db, environment, SCHEMA, add_prefix_for_prod


class RevenueAnalytic(db.Model):
    __tablename__ = 'revenue_analytics'

    if environment == "production":
        __table_args__ = (
            db.UniqueConstraint('service_id', 'date', name='unique_service_date'),
            {'schema': SCHEMA}
        )
    else:
        __table_args__ = (
            db.UniqueConstraint('service_id', 'date', name='unique_service_date'),
        )

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('services.id')), nullable=False)
    revenue = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=datetime.now, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now, nullable=False)

    service = db.relationship("Service", back_populates="revenue_analytics")

    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'revenue': self.revenue,
            'date': self.date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
