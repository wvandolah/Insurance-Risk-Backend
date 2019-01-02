from django.conf.urls import url
from . import views

urlpatterns = [
    url('registration', views.register),
    url('login', views.login),
]
