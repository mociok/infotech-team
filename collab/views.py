from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DeviceData, DeviceDataVars,Devices


def index(req):
    return render(req, 'index.html') # render index.html


# JHVcEiAH.qjWZxBoAtyURBl3NNoqOnleLbmtjrh9A -- API KEY!!!1!
def find_key(input_dict, target_key):
    """Rekursywnie przeszukuje słownik w poszukiwaniu określonego klucza."""
    if target_key in input_dict:
        return input_dict[target_key] # if key is found, return it
    for key, value in input_dict.items(): # else perform the same operation on all values
        if isinstance(value, dict):
            result = find_key(value, target_key)
            if result:
                return result
    return None
@permission_classes([HasAPIKey])
class LoraApi(APIView): # API View
    def post(self, req):
        try:
            json_data = find_key(req.data, "decoded_payload") # find decoded_payload key
            data_vars = []
            for data in json_data:
                datavar = DeviceDataVars.objects.create(
                    variable_name=data,
                    variable=json_data[data]
                ) # create new DeviceDataVars object
                data_vars.append(datavar)
            devEui = find_key(req.data, "dev_eui")
            device = DeviceData.objects.create(
                device=Devices.objects.get(devEui=devEui)
            ) # create new DeviceData object
            device.decodedPayload.set(data_vars)
            device.save()
            return Response({"status": "ok"})
        except Exception as e:
            print(e)
            return Response({"status": "error"}) # return error if something went wrong

@permission_classes([permissions.IsAuthenticated])
class DevicesApi(APIView):
    def get(self, req):
        devices = Devices.objects.filter(user=req.user, is_public=False)
        pub_devices = Devices.objects.filter(is_public=True)
        print(DeviceData.objects.filter(device__in=pub_devices))
        return Response({"devices": devices.values(), "public": pub_devices.values()})