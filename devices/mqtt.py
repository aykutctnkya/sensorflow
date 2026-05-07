import json
import django
import os
import paho.mqtt.client as mqtt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensorflow.settings')
django.setup()

from devices.models import Device, SensorData

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with code: {rc}")
    client.subscribe('sensors/#')

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"Received: {payload}")
        device_id = payload.get('device_id')
        value = payload.get('value')
        unit = payload.get('unit')

        device = Device.objects.get(id=device_id)
        instance = SensorData.objects.create(
            device=device,
            value=value,
            unit=unit
        )

        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'sensor_data',
            {
                'type': 'sensor_data_message',
                'data': {
                    'device': str(instance.device.id),
                    'value': instance.value,
                    'unit': instance.unit,
                    'timestamp': str(instance.timestamp),
                }
            }
        )
        print(f"Saved and broadcast: {device.name} - {value} {unit}")

    except Device.DoesNotExist:
        print(f"Device not found: {device_id}")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('127.0.0.1', 1883,60)
client.loop_forever()