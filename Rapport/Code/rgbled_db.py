from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

#Post status of RGB LED to database
def post(device, status):

  dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')

  table = dynamodb.Table('LedStatus')

  response = table.update_item(
     Item={
          'Device': device,
          'Status': status,
        
      }
  )