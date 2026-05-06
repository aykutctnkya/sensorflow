from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Device
from .serializer import DeviceSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

