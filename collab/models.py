from django.db import models

# Create your models here.
class Devices(models.Model):
    devEui = models.CharField(max_length=100) # primary key
    devName = models.CharField(max_length=100) # unique Name of device
    decodedPayload = models.JSONField(null=True) # decoded payload
    time = models.DateTimeField(auto_now_add=True) # time of receiving data
    user = models.ManyToManyField('auth.User', related_name='devices', blank=True) # user that have access to data from multiple devices
