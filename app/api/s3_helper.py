from dotenv import load_dotenv
import boto3
import botocore
import os
import uuid

load_dotenv()

BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
S3_LOCATION = f"http://{BUCKET_NAME}.s3.amazonaws.com/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

if not BUCKET_NAME:
    raise ValueError("S3_BUCKET_NAME environment variable is not set.")
if not os.environ.get('S3_KEY'):
    raise ValueError("S3_KEY environment variable is not set.")
if not os.environ.get('S3_SECRET'):
    raise ValueError("S3_SECRET environment variable is not set.")


# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('S3_KEY'),
    aws_secret_access_key=os.environ.get('S3_SECRET'),
)


def get_unique_filename(filename):
    """
    Generate a unique filename using UUID4.
    """
    ext = filename.rsplit('.', 1)[-1].lower()
    unique_filename = uuid.uuid4().hex
    return f"{unique_filename}.{ext}"

def upload_file_tos3(file, acl='public-read'):
    """"
    upload_file_tos3 function uploads a file to an S3 bucket
    and returns the URL of the uploaded file.
    """
    try:
        s3.upload_fileobj(
            file,
            BUCKET_NAME,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        return {"errors": str(e)}
    return {"url": f"{S3_LOCATION}{file.filename}"}

def remove_file_from_s3(image_url):
    """
    remove_file_from_s3 function removes a file from an S3 bucket
    using the file's URL.
    """
    key = image_url.rsplit("/", 1)[1]
    print(key)
    try:
        s3.delete_object(
        Bucket=BUCKET_NAME,
        Key=key
        )
    except Exception as e:
        return { "errors": str(e) }
    return True
