from rest_framework import serializers
from .models import Device, SensorData, Alert

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'location', 'is_active', 'created_at']
        read_only_fields =['id', 'created_at']

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['id', 'device', 'value', 'unit', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'device', 'sensor_data', 'message', 'severity', 'is_resolved', 'created_at']
        read_only_fields = ['id', 'created_at']