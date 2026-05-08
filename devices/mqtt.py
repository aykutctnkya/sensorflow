import json
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensorflow.settings')
django.setup()
import paho.mqtt.client as mqtt
from devices.anomaly import check_anomaly



from devices.models import Device, SensorData

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT broker with code: {reason_code}")
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
        check_anomaly(instance)

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

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect('mosquitto', 1883,60)
client.loop_forever()