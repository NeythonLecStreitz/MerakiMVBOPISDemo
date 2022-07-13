import requests
import json
import ast
import logging

#Instantiate logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    url = 'https://hooks-sandbox.imiconnect.io/events/NB0RASJO9B'
    
    # Parse customer info from SNS Topic, convert str to dict
    customer_info = event['Records'][0]['Sns']['Message']
    payload = ast.literal_eval(customer_info)
    
    logger.info("SUCCESS: SNS topic retrived")
    logger.info("PAYLOAD:" + customer_info)
    
    
    # POST to IMIMOBILE to send customer sms
    print("Sending SMS to customer...")
    response = requests.post(url, json=payload)
    logger.info("SUCCESS: Request sent to IMIMOBILE")
    logger.info(response.text)
    
    return {
        'Response':200,
        'Body': response.text
    }
