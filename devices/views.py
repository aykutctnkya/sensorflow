from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Device, SensorData
from .serializers import DeviceSerializer, SensorDataSerializer
from .anomaly import check_anomaly

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'location']

class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['device']

    def perform_create(self, serializer):
        instance = serializer.save()
        check_anomaly(instance)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'sensor_data',
            {
                'type': 'sensor_data_message',
                'data': {
                    'device': str(instance.device.id),
                    'value' : instance.value,
                    'unit': instance.unit,
                    'timestamp' : str(instance.timestamp),
                    

                }
            }
        )