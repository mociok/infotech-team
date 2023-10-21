from datetime import timedelta

from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DeviceData, DeviceDataVars,Devices
from django.db.models import Q,Avg, FloatField, F,Max
from django.utils import timezone
from django.db.models.functions import Cast,Round
from django.db.models.expressions import ExpressionWrapper
from django.shortcuts import redirect, render
from django.contrib.auth import logout

import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
from vertexai.preview.language_models import TextGenerationModel


def index(req):
    return render(req, 'index.html') # render index.html


def login(req):
    return render(req, 'login.html')  # render login.html

def main(req):
    return render(req, 'main.html')

def signout(req):
    logout(req)  # logout user
    return redirect('login')


# 4hXGwzn4.LbYxWp0Ikiv9u5cneU0h2WRm3jFBMzom -- API KEY!!!1!
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
        devices = Devices.objects.filter(Q(user=req.user, is_public=False) | Q(is_public=True))
        devices_data_list = []
        average_overall_co2_per_device = DeviceData.objects.filter(
            decodedPayload__variable_name='CO2'
        ).values(
            'device__devName'
        ).annotate(
            avg_value=Round(Avg(
                ExpressionWrapper(
                    Cast(F('decodedPayload__variable'), FloatField()),
                    output_field=FloatField()
                )
            ),1)
        )

        peak_overall_co2_per_device = DeviceData.objects.filter(
            decodedPayload__variable_name='CO2'
        ).values(
            'device__devName'
        ).annotate(
            max_value=Round(Max(
                ExpressionWrapper(
                    Cast(F('decodedPayload__variable'), FloatField()),
                    output_field=FloatField()
                )
            ),1)
        )

        # Definicja okresów czasu
        last_hour= timezone.now().replace(minute=0, second=0, microsecond=0)
        last_24_hours = last_hour - timedelta(hours=1)
        #print(last_hour,last_24_hours)

        # Obliczenie średniej z ostatniej godziny dla zmiennej 'CO2' dla każdego urządzenia
        average_last_hour_co2_per_device = DeviceData.objects.filter(
            time__gte=last_hour,
            decodedPayload__variable_name='CO2'
        ).values(
            'device__devEui', 'device__devName'
        ).annotate(
            avg_value=Avg(
                ExpressionWrapper(
                    Cast(F('decodedPayload__variable'), FloatField()),
                    output_field=FloatField()
                )
            )
        )

        # Obliczenie średniej z ostatnich 24 godzin dla zmiennej 'CO2' dla każdego urządzenia
        average_last_24_hours_co2_per_device = DeviceData.objects.filter(
            time__gte=last_24_hours,
            decodedPayload__variable_name='CO2'
        ).values(
            'device__devEui', 'device__devName'
        ).annotate(
            avg_value=Avg(
                ExpressionWrapper(
                    Cast(F('decodedPayload__variable'), FloatField()),
                    output_field=FloatField()
                )
            )
        )

        percentage_comparison_per_device = []
        for last_hour_data, last_24_hours_data in zip(average_last_hour_co2_per_device,
                                                      average_last_24_hours_co2_per_device):
            devEui = last_hour_data['device__devEui']
            devName = last_hour_data['device__devName']
            if last_24_hours_data['avg_value'] != 0:
                percentage_comparison = ((last_hour_data['avg_value'] - last_24_hours_data['avg_value']) /
                                         last_24_hours_data['avg_value']) * 100
            else:
                percentage_comparison = 0  # lub inna wartość w przypadku dzielenia przez zero
            percentage_comparison_per_device.append({
                'devName': devName,
                'prcnt': round(percentage_comparison,2)
            })

        return Response({"devices": devices.values(),"avg":average_overall_co2_per_device,"peak":peak_overall_co2_per_device,"percentage":percentage_comparison_per_device})

#@permission_classes([permissions.IsAuthenticated])
class VertexAiChat(APIView):
    def get(self, req,data):
        parameters = {
            "temperature": 0.2,
            "max_output_tokens": 256,
            "top_p": .8,
            "top_k": 40,
        }

        model = TextGenerationModel.from_pretrained("text-bison@001")
        response = model.predict(
            'Based on this data, write me a trend that will determine whether these data are normal, if not, write a few steps at points that can lead to a reduction in the city'+data,
            **parameters,
        )
        print(f"Response from Model: {response.text}")
        return Response({"status": response.text})