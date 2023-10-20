from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DeviceData


def index(req):
    return render(req, 'index.html')


# JHVcEiAH.qjWZxBoAtyURBl3NNoqOnleLbmtjrh9A -- API KEY!!!1!
def find_key(input_dict, target_key):
    """Rekursywnie przeszukuje słownik w poszukiwaniu określonego klucza."""
    if target_key in input_dict:
        return input_dict[target_key]
    for key, value in input_dict.items():
        if isinstance(value, dict):
            result = find_key(value, target_key)
            if result:
                return result
    return None
@permission_classes([HasAPIKey])
class LoraApi(APIView):
    def post(self, req):
        try:
            json_data = find_key(req.data, "decoded_payload")
            devEui = find_key(req.data, "dev_eui")
            DeviceData.objects.create(
                device_id=devEui,
                decodedPayload=json_data
            )

            return Response({"status": "ok"})
        except Exception as e:
            return Response({"status": "error"})
