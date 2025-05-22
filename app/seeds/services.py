from app.models import db, User, environment, SCHEMA, Service
from sqlalchemy.sql import text

def seed_services():

    service1 = Service(
        name='All Natural',
        description='Enhances your natural beauty using clean, skin-friendly products free of harsh chemicals. We focus on creating a fresh, radiant look that feels light and effortless, perfect for everyday wear or special occasions. Ideal for sensitive skin or those seeking a more mindful approach to beauty.',
        price=25.00,
        # duration=30,
    )
    service2 = Service(
        name='Brows & Lashes',
        description='Designed to define and enhance your natural features with precision and care. We shape brows to complement your face and offer lash treatments that add subtle lift, length, or volume—no heavy makeup needed. Perfect for a polished, low-maintenance look that lasts.',
        price=50.00,
        # duration=60,
    )
    service3 = Service(
        name='instagram Baddie',
        description='For those who love a bold, glamorous look that stands out on social media. This service includes dramatic eye makeup, flawless skin, and perfectly sculpted features. Ideal for photoshoots, events, or anyone wanting to make a statement with their makeup.',
        price=150.00,
        # duration=120,
    )
    service4 = Service(
        name='1 on 1 Makeup Lesson',
        description='A personalized session where you learn makeup techniques tailored to your style and preferences. We cover everything from skincare prep to advanced application methods, ensuring you leave with the skills and confidence to recreate your favorite looks at home.',
        price=200.00,
        # duration=180,
    )

    db.session.add(service1)
    db.session.add(service2)
    db.session.add(service3)
    db.session.add(service4)



    db.session.commit()

def undo_services():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.services RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM services"))

    db.session.commit()
