import boto3
import json

with open('sample.jpeg', 'rb') as fd:
    image = fd.read()

recognize = boto3.client('rekognition')
labels_list = recognize.detect_labels(Image={'Bytes': image}, MaxLabels=10, MinConfidence=70)
print(json.dumps(labels_list, indent=4))
