from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

tstamp = datetime.now()

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def post(devId, data):
    dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')

    table = dynamodb.Table('Sensors')
    timestamp = datetime.now()
    
    #Posts sensor data to database once every hour
    if ((timestamp - tstamp).total_seconds() > 3600):
        response = table.put_item(
            Item={
                'Device': str(devId),
                'Time': str(timestamp),
                'Sound': data['sound'],
                'Temperature': data['temperature'],
                'Ambient Light': data['ambientLight'],
                'Humidity': data['humidity'],
            }
        )
	global tstamp
	tstamp = datetime.now()