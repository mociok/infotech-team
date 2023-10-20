from django.db import models

# Create your models here.
class Devices(models.Model):
    devEui = models.CharField(max_length=100)
    devName = models.CharField(max_length=100)
    decodedPayload = models.JSONField(null=True)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ManyToManyField('auth.User', related_name='devices', blank=True)

    def __str__(self):
        return f"{self.devName} - {self.devEui} - Users: {self.user.all().count()} // added at: {self.time.strftime('%m/%d/%Y, %H:%M')}"