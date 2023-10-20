from django.db import models

# Create your models here.
class Devices(models.Model):
    devEui = models.CharField(max_length=100) # primary key
    devName = models.CharField(max_length=100) # unique Name of device
    decodedPayload = models.JSONField(null=True) # decoded payload
    time = models.DateTimeField(auto_now_add=True) # time of receiving data
    user = models.ManyToManyField('auth.User', related_name='devices', blank=True) # user that have access to data from multiple devices

    def __str__(self):
        return f"{self.devName} - {self.devEui} - Users: {self.user.all().count()} // added at: {self.time.strftime('%m/%d/%Y, %H:%M')}"