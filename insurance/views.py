# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from .api import PersonalMetricSerializer
from .models import PersonalMetric
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
    snippit = PersonalMetric(name=data['name'], age=data['age'], weight=data['weight'], gender=data['gender'], user_id=user)
    snippit.save()
    serial = PersonalMetricSerializer(snippit)
    # print(serial.data)
    return JsonResponse(serial.data)
  # return JsonResponse({'test': 'test'}, safe=True)
  elif request.method == 'GET':
    if 'id' in request.GET:
      datap = PersonalMetric.objects.filter(id=request.GET['id'])
      serial = PersonalMetricSerializer(datap, many=True)
    else:
      datap = PersonalMetric.objects.filter(user=user)
      serial = PersonalMetricSerializer(datap, many=True)
    return JsonResponse(serial.data, safe=False)


# Create your views here.
