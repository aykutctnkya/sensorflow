from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Device, SensorData

class DeviceAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.device = Device.objects.create(
            name='Test Sensor',
            location='Test Location',
            is_active=True
        )

    def test_get_device_list(self):
        response = self.client.get('/api/devices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_device(self):
        data = {'name': 'New Sensor', 'location': 'New Location'}
        response = self.client.post('/api/devices/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthorized_access(self):
        self.client.credentials()
        response = self.client.get('/api/devices/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_devices_by_active(self):
        response = self.client.get('/api/devices/?is_active=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SensorDataAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.device = Device.objects.create(
            name='Test Sensor',
            location='Test Location'
        )

    def test_create_sensor_data(self):
        data = {
            'device': str(self.device.id),
            'value': 23.5,
            'unit': 'C'
        }
        response = self.client.post('/api/sensor-data/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_sensor_data_by_device(self):
        SensorData.objects.create(device=self.device, value=23.5, unit='C')
        response = self.client.get(f'/api/sensor-data/?device={self.device.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)