from rest_framework import serializers
from .models import PersonalMetric, HumanMetric

class PersonalMetricSerializer(serializers.ModelSerializer):
  class Meta:
    model = PersonalMetric
    fields = ('id', 'name', 'age', 'weight', 'gender')

    def create(self, validate_data):
      print('2 test')
      user = self.context['request'].user
      human = PersonalMetric.objects.create(user=user, **validate_data)
      return human


class HumanMetricSerializer(serializers.ModelSerializer):
  class Meta:
    model = HumanMetric
    fields = ('id', 'name', 'age', 'weight', 'gender')
