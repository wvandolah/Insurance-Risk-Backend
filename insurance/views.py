# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from .api import PersonalMetricSerializer, HumanMetricSerializer
from .models import PersonalMetric, HumanMetric
from util.checkMed import mCheck
from util.checkPlan import pCheck
import json


@csrf_exempt
@api_view(["GET", "POST"])
def people(request):
  # if request.user.is_anonymous:
  #   return JsonResponse({'error': 'You most be logged in'})
  user = User.objects.filter(username=request.user).values_list('id', flat=True).get()
  if request.method == 'POST':
    data = json.loads(request.body)
    # print(data)
    snippit = PersonalMetric(name=data['name'], age=data['age'], weight=data['weight'], gender=data['gender'], height=data['height'], user_id=user)
    # not needed right now
    # snippit.save()
    serial = PersonalMetricSerializer(snippit)
    # print(serial.data)
    return JsonResponse({'plans': ['CFG', 'Dignified Choice'], 'user': serial.data})
  # return JsonResponse({'test': 'test'}, safe=True)
  elif request.method == 'GET':
    if 'id' in request.GET:
      datap = PersonalMetric.objects.filter(id=request.GET['id'])
      serial = PersonalMetricSerializer(datap, many=True)
    else:
      datap = PersonalMetric.objects.filter(user=user)
      serial = PersonalMetricSerializer(datap, many=True)
    return JsonResponse(serial.data, safe=False)

@csrf_exempt
@api_view(["POST"])
def checkBuild(request):
  data = json.loads(request.body)
  snippit = HumanMetric(age=data['age'], weight=data['weight'], gender=data['gender'], height=data['height'])
  # not needed right now
  # snippit.save()
  serial = HumanMetricSerializer(snippit)
  pCheck(serial.data)
  return JsonResponse({'plans': ['CFG', 'Dignified Choice'], 'user': serial.data})
# Create your views here.

@csrf_exempt
@api_view(["POST"])
def checkMed(request):
  data = json.loads(request.body)
  value = mCheck(data['plan'], 'no')
  return JsonResponse({'value': value})
