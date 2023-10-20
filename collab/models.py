from django.db import models

# Create your models here.
class Devices(models.Model):
    devEui = models.CharField(max_length=100,unique=True) # primary key
    devName = models.CharField(max_length=100) # unique Name of device
    user = models.ManyToManyField('auth.User', related_name='devices', blank=True) # user that have access to data from multiple devices
    is_public = models.BooleanField(default=False, help_text="Ignores users and shows the device for everyone") # is device public

    def __str__(self):
        if self.is_public:
            return f"{self.devName} - {self.devEui} - Public"
        else:
            return f"{self.devName} - {self.devEui} - Users: {self.user.all().count()}"


class DeviceData(models.Model):
    device = models.ForeignKey(Devices, on_delete=models.CASCADE, related_name='data') # device that send data
    decodedPayload = models.ManyToManyField('DeviceDataVars', related_name='data_vars') # decoded payload
    time = models.DateTimeField(auto_now_add=True) # time of receiving data

    def __str__(self):
        return f"{self.device.devName} - {self.device.devEui} // added at: {self.time.strftime('%m/%d/%Y, %H:%M')}"


class DeviceDataVars(models.Model):
    variable_name = models.CharField(max_length=100) # name of variable
    variable = models.CharField(max_length=250) # value of variable

    def __str__(self):
        return f"({self.id}) {self.variable_name} - {self.variable}"

