from __future__ import print_function # Python 2/3 compatibility
from django.http import HttpResponse
import boto3
import json
import decimal
from datetime import datetime
from rgbled_db import post
from boto3.dynamodb.conditions import Key, Attr
from django.shortcuts import render
from django.template import loader

from graphos.renderers import gchart
from graphos.sources.simple import SimpleDataSource
from django.views.decorators.csrf import csrf_exempt

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

table = dynamodb.Table('Sensors')
table2 = dynamodb.Table('LedStatus')

@csrf_exempt
def index(request):
   
    #Post RGB LED status if button pressed
    if (request.is_ajax()):
       post(request.POST['device'], request.POST['status'])

    
    name = ['44804', '45452', '45311']
     
    context = {}
    
    #Read sensor data from database and create graphic view of data
    for dev in name:  
        response = table.query(
            KeyConditionExpression=Key('Device').eq(dev)
        )
        data = [[]for i in range(int(response['Count'])+1)]
 
        data[0] = ['Time', 'Temperature [C]', 'Humidity [RH%]', 'Ambien Light [Lux]', 'Sound [dB]']
        n = 1
        
        for i in response['Items']:
            info = [datetime.strptime(i['Time'],'%Y-%m-%d %H:%M:%S.%f'), int(i['Temperature']),  int(i['Humidity']), int(i['Ambient Light']), int(i['Sound'])]
            data[n] = info
            n += 1
       
        context[dev] =  gchart.LineChart(SimpleDataSource(data=data), options={'title':'Device ID '+dev})
        response2 = table2.query(
            KeyConditionExpression=Key('Device').eq(dev)
        )
        for j in response2['Items']:
            context['btn'+dev] = j['Status']

         
    return render(request, 'index.html', context)

