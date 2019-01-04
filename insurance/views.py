# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from .api import PersonalMetricSerializer, HumanMetricSerializer, InsuranceProductSerializer, MedicationSerializer

from .models import PersonalMetric, HumanMetric, InsuranceProductBuild, MedicationCheck
from django.db.models import Q


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
  products = build_query(age=data['age'], weight=data['weight'], height=data['height'], gender=data['gender'])
  print(products)
  hSerial = InsuranceProductSerializer(products, many=True)
  return JsonResponse({'user': serial.data, "plans": hSerial.data})

# Create your views here.

@csrf_exempt
@api_view(["POST"])
def checkMed(request):
  data = json.loads(request.body)
  medication = medication_query(prescription=data['prescription'], product=data['product'])
  if not medication:
    return JsonResponse([{
        "medication": data['prescription'],
        "time": "N/A",
        "indication": "No Data",
        "outcome": "No Data",
        "product": data['product']
      }], safe=False)
  else:
    mSerial = MedicationSerializer(medication, many=True)
  return JsonResponse(mSerial.data, safe=False)

# queries the insurance product table

def build_query(age, height, weight, gender):
  hwa = InsuranceProductBuild.objects.filter(Q(height=height) | Q(height = 0)).filter(max_weight__gt=weight).filter(min_weight__lt=weight
  ).filter(min_age__lte=age).filter(max_age__gt=age)

  if gender == 'male':
    g = hwa.filter(male=1)
  else:
    g = hwa.filter(female=1)

  return g.values("id", "carrier", "product2", "product3")

# Medication functions


def medication_query(prescription, product):
  rx = MedicationCheck.objects.filter(medication=prescription)
  c = rx.filter(product=product).all()
  return c.values('medication', 'time', 'indication', 'outcome', 'product')
