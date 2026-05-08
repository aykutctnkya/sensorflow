from django.db import models
import uuid

class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SensorData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='sensor_data')
    value = models.FloatField()
    unit = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.name} - {self.value} {self.unit}"
    
    class Meta:
        ordering = ['-timestamp']

class Alert(models.Model):
    SEVERITY_CHOICES = [
        ('low','Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='alerts')
    sensor_data = models.ForeignKey(SensorData, on_delete=models.CASCADE, related_name='alerts')
    message = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.device.name} - {self.severity} - {self.created_at}"
    
    class Meta:
        ordering = ['-created_at']