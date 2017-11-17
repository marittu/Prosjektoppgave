from __future__ import print_function # Python 2/3 compatibility
from django.http import HttpResponse
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from django.shortcuts import render
from django.template import loader

from graphos.renderers import flot, gchart
from graphos.sources.model import ModelDataSource
from graphos.sources.simple import SimpleDataSource
#from graphos.views import FloatAsJson, RenderAsJson

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



def index(request):
 
    response = table.query(
        KeyConditionExpression=Key('Device').eq('44804')
    )
    data = [[]for i in range(int(response['Count'])+1)]
 
    data[0] = ['Time', 'Temperature', 'Humidity']
    msg = ()
    n = 1
    for i in response['Items']:
      	info = [i['payload']['Time'], int(i['payload']['Temperature']),  int(i['payload']['Humidity'])]
        data[n] = info
	n += 1
       
    line_chart = gchart.LineChart(SimpleDataSource(data=data))
    context = {"line_chart": line_chart}
    
    return render(request, 'index.html', context)
