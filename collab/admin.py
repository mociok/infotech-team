from django.contrib import admin
from .models import Devices, DeviceData, DeviceDataVars
# Register your models here.
admin.site.register(Devices) # register Devices model
admin.site.register(DeviceData)
admin.site.register(DeviceDataVars)