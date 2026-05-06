from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Device, SensorData
from .serializer import DeviceSerializer, SensorDataSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer