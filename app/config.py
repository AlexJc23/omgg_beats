import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_RUN_PORT = os.environ.get('FLASK_RUN_PORT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
    SQLALCHEMY_ECHO = True

    # S3 config
    AWS_ACCESS_KEY_ID = os.environ.get('S3_KEY')
    AWS_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET')
    AWS_S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
