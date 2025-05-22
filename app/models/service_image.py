from datetime import datetime
from .db import db, environment, SCHEMA, add_prefix_for_prod

class ServiceImage(db.Model):
    __tablename__ = 'service_images'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('services.id')), nullable=False)
    s3_url = db.Column(db.String(255), nullable=False)
    image_file = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now, nullable=False)

    service = db.relationship("Service", back_populates="images")

    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            's3_url': self.s3_url,
            'image_file': self.image_file,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f"<ServiceImage {self.id} {self.service_id} {self.s3_url}>"
