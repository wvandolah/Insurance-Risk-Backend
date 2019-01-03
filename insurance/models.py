from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class HumanMetric(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
  name = models.CharField(max_length=200)
  age = models.IntegerField(default=0)
  weight = models.IntegerField(default=0)
  gender = models.CharField(max_length=200)
  height = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)

class PersonalMetric(HumanMetric):
  user = models.ForeignKey(User, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        PersonalMetric.objects.create(user=instance)
        Token.objects.create(user=instance)
