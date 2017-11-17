from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')

table = dynamodb.Table('SensorData')

print("Queries from 44804")

response = table.query(
    KeyConditionExpression=Key('Device').eq('44804')
)

for i in response['Items']:
    print(i['Device'],": Time: ",i['payload']['Time'] ,"Pressure: ", i['payload']['Pressure'], 
        "Temperature: ", i['payload']['Temperature'] , "Sound Level: ", i['payload']['Sound'],
        "Ambient Light: ", i['payload']['Ambient Light'], "UV Index: ", i['payload']['UV Index'], 
        "Humidity: ", i['payload']['Humidity'])