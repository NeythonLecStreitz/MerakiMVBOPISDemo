import boto3
import re
import json
import urllib.parse

def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    photo = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    
    plate_num = detect_text(photo,bucket)
    print("License #: " + plate_num)
    
    return {
            'Response' : 200,
            'Body' : plate_num
    }

def detect_text(photo, bucket):

    # Connects to Rekognition client
    client=boto3.client('rekognition')

    # Detects text in specified Bucket + Image
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})

    # Saves detections into list of dicts                    
    textDetections=response['TextDetections']

    # For each detection, check to ensure detection is a LINE with at least 98% confidence
    print ('\nDetecting license plate\n----------')
    for text in textDetections:
        if (text['Type'] == 'LINE') and (text['Confidence'] > 97.99):
            # If detection valid, regex to verify License
            if (re.search('[A-Z0-9]{1,3}\s[A-Z0-9]{1,5}', text['DetectedText'])):
                plate_num = text['DetectedText']

    # Return 
    return plate_num
