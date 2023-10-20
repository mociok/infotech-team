from django.contrib import admin
from django.urls import path
from collab.views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('api/get_device_data/', LoraApi.as_view() , name='get_device_data'), # get device data
    path('api/get_devices/', DevicesApi.as_view() , name='get_devices'), # get devices
]
