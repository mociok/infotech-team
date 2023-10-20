from django.contrib import admin
from django.urls import path
from collab.views import *

urlpatterns = [
    path('', index, name='index'),
    path('api/get_device_data/', LoraApi.as_view() , name='get_device_data'),
]
