from django.conf.urls import url
from . import views

urlpatterns = [
    url('people', views.people),
    url('build', views.checkBuild)
]
