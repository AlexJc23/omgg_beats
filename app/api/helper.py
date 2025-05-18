from dotenv import load_dotenv
import boto3
import botocore
import os
import uuid


load_dotenv()
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('S3_KEY'),
    aws_secret_access_key=os.environ.get('S3_SECRET'),
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def get_unique_filename(filename):
    """
    Generate a unique filename using UUID4.
    """
    ext = filename.rsplit('.', 1)[-1].lower()
    unique_filename = uuid.uuid4().hex
    return f"{unique_filename}.{ext}"
