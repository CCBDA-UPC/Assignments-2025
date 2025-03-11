import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Define the name of the S3 bucket
BUCKET = 'lab04-main.ccbda.upc.edu'

# Create an S3 client using boto3 and credentials loaded from environment variables
s3 = boto3.client(
    's3',  # Specify that it is an S3 client
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN')
)

# Specify the name of the object to be uploaded to S3
objectName = 'sample_image.jpg'

# Open the file located at './images/Lab04-sampleImage.jpeg' in binary read mode
with open('./images/Lab04-sampleImage.jpeg', 'rb') as fd:
    # Read the content of the file as binary data
    image = fd.read()
    # Upload the binary data (image) to the specified S3 bucket with the given object name
    s3.put_object(Bucket=BUCKET, Body=image, Key=objectName)

# Open (or create) a file named 'downloaded.jpeg' in binary write mode to save the downloaded object
with open('./downloaded.jpeg', 'wb') as fd:
    # Retrieve the object from the S3 bucket using its key
    response = s3.get_object(Bucket=BUCKET, Key=objectName)
    # Write the content of the downloaded object to the local file
    fd.write(response['Body'].read())