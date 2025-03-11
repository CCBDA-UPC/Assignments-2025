import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

with open('./images/Lab04-sampleImage.jpeg', 'rb') as fd:
    image = fd.read()

recognize = boto3.client('rekognition',
                         region_name=os.getenv('AWS_REGION'),
                         aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                         aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                         aws_session_token=os.getenv('AWS_SESSION_TOKEN'))
labels_list = recognize.detect_labels(Image={'Bytes': image}, MaxLabels=10, MinConfidence=70)
print(json.dumps(labels_list, indent=4))
