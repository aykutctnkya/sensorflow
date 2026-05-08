from django.contrib import admin
from .models import Device, SensorData, Alert

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'location']


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ['device', 'value', 'unit', 'timestamp']
    list_filter = ['device', 'unit']

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['device', 'severity', 'message', 'is_resolved', 'created_at']
    list_filter = ['severity', 'is_resolved']
    search_fields = ['device__name', 'message']