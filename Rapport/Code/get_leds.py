from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import tbsense

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def read_db(tb, devId):
    
    dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')

    table = dynamodb.Table('LedStatus')

    response = table.query(
        KeyConditionExpression=Key('Device').eq('%d' % devId)
    )
   
    for i in response['Items']:
        if( i['Status'] == 'On'):
            tb.LedOn()
        elif(i['Status'] == 'Off'):
            tb.LedOff()