from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import Point
import json

def index(request):
    return HttpResponse("Hello world!")

@csrf_exempt
def put(request):
    if request.method == 'POST':
        for row in json.loads(request.body):
            print row
            p = Point(payload=row['payload'])
            p.save()
            print p.id
    return HttpResponse('OK')

# Create your views here.
