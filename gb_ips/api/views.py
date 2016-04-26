from django.shortcuts import render
from training.models import TrainingRawData
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

# Create your views here.

@csrf_exempt
def rps_pos(req):
    data = req.POST.get('data')
    data = json.loads(data)

    objs = TrainingRawData.load_all(data)
    x_values = []
    y_values = []

    for obj in objs:
        x = obj['x']
        y = obj['y']
        x_values.append(x)
        y_values.append(y)

    return HttpResponse(json.dumps([x_values, y_values]))


