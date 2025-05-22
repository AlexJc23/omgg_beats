from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_users():
    demo = User(
        first_name='Heather', last_name='Carl', email='demo@aa.io', password='password', phone_number='1234567890', profile_image='https://omggbeats.s3.us-east-1.amazonaws.com/Images/model1.webp')
    demo2 = User(
        first_name='Jane', last_name='Doe', email='jane@aa.io', password='password', phone_number='0987654321', profile_image='https://omggbeats.s3.us-east-1.amazonaws.com/Images/model2.jpeg')
    demo3 = User(
        first_name='Autumn', last_name='Carl', email="demmon@aa.io", password='password', phone_number='1234567890', profile_image='https://omggbeats.s3.us-east-1.amazonaws.com/Images/model3.webp')

    db.session.add(demo)
    db.session.add(demo2)
    db.session.add(demo3)

    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))

    db.session.commit()
