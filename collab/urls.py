from django.contrib import admin
from django.urls import path, include
from collab.views import *
from allauth.socialaccount.providers.google.urls import urlpatterns as google_urlpatterns

urlpatterns = [
    path('old/', index, name='index.old'),
    path('login/',login, name='login'),
    path('', main, name='index'),
    path('api/get_device_data/', LoraApi.as_view() , name='get_device_data'), # get device data
    path('api/get_devices/', DevicesApi.as_view() , name='get_devices'), # get devices
    path('accounts/', include('allauth.urls')), # allauth
]
