from django.shortcuts import render
from .models import Devices

def index(req):
    return render(req, 'index.html') # render index.html
