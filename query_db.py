import sys
import pymysql
import rds_config
import logging
import json
import boto3

# Configuration values
rds_host  = 'customer-database.ceisylvthaeg.us-west-1.rds.amazonaws.com'
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

# Instantiate logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Connect to database
try:
    conn = pymysql.connect(host=rds_host, user=name, password=password, 
        database=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()
    

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def lambda_handler(event, context):
    
    platenum = event['Body']
    
    # Query database for license plate
    query = query_database(platenum)
    
    # Format customer information and return
    customer_info = {
                "CustomerName": query['cust_name'],
                "OrderId": query['order_id'],
                "ProductName": query['product_name'],
                "CustomerPhone": "+1" + str(query['cust_phone'])
    }
    
    client = boto3.client('sns')
    response = client.publish(
                                TargetArn='arn:aws:sns:us-west-1:225067446252:OrderRequested',
                                Message=json.dumps({'default': customer_info}),
                                MessageStructure='json'
                )

    logger.info("SUCCESS: Customer Order sent to SNS Topic for SMS messaging lambda.")
    logger.info(response.text)
    return response
    
def query_database(platenum):
    cursor = conn.cursor()
    sql_query = "SELECT cust_name, cust_phone, product_name, order_id FROM CUST_INFO JOIN CUST_ORDER USING (cust_id) JOIN ORDER_INFO USING(order_id) WHERE cust_platenum = %s LIMIT 1"
    row_count = cursor.execute(sql_query, (platenum, ))
    
    if row_count < 1:
        logger.info("SUCCESS: Database succesfully queried but NO customer order associated.")
    else:
        rows = cursor.fetchall()
        logger.info("SUCCESS: Database succesfully queried and customer order retrieved.")
    
    return rows[0]
        
