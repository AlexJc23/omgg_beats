
from app.models import db, User, environment, SCHEMA, Service, ServiceImage
from sqlalchemy.sql import text

def seed_service_images():
    service1 = Service.query.filter(Service.name == 'All Natural').first()
    service2 = Service.query.filter(Service.name == 'Brows & Lashes').first()
    service3 = Service.query.filter(Service.name == 'instagram Baddie').first()
    service4 = Service.query.filter(Service.name == '1 on 1 Makeup Lesson').first()

    image1 = ServiceImage(
        service_id=1,
        s3_url='https://omggbeats.s3.us-east-1.amazonaws.com/Images/allnat.jpg'
    )
    image2 = ServiceImage(
        service_id=1,
        s3_url='https://omggbeats.s3.us-east-1.amazonaws.com/Images/allnat2.jpg'
    )
    image3 = ServiceImage(
        service_id=1,
        s3_url='https://omggbeats.s3.us-east-1.amazonaws.com/Images/allnat3.avif'
    )
    image4 = ServiceImage(
        service_id=2,
        s3_url='https://omggbeats.s3.us-east-1.amazonaws.com/Images/brows.avif'
    )
    image5 = ServiceImage(
        service_id=2,
        s3_url='https://omggbeats.s3.us-east-1.amazonaws.com/Images/brows2.avif'
    )
    image6 = ServiceImage(
        service_id=2,
        s3_url='https://omggbeats.s3.us-east-1.amazonaws.com/Images/brows3.avif'
    )
    image7 = ServiceImage(
        service_id=3,
        s3_url='https://omggbeats.s3.us-east-1.amazonaws.com/Images/instabad1.avif'
    )
    image8 = ServiceImage(
        service_id=3,
        s3_url='https://omggbeats.s3.us-east-1.amazonaws.com/Images/instabad2.avif'
    )
    image9 = ServiceImage(
        service_id=3,
        s3_url='https://omggbeats.s3.us-east-1.amazonaws.com/Images/instabad3.avif'
    )
    image10 = ServiceImage(
        service_id=4,
        s3_url='https://omggbeats.s3.us-east-1.amazonaws.com/Images/class.avif'
    )
    image11 = ServiceImage(
        service_id=4,
        s3_url='https://omggbeats.s3.us-east-1.amazonaws.com/Images/class2.avif'
    )

    db.session.add(image1)
    db.session.add(image2)
    db.session.add(image3)
    db.session.add(image4)
    db.session.add(image5)
    db.session.add(image6)
    db.session.add(image7)
    db.session.add(image8)
    db.session.add(image9)
    db.session.add(image10)
    db.session.add(image11)

    db.session.commit()

def undo_service_images():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.service_images RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM service_images"))

    db.session.commit()
