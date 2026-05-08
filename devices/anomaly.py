from .models import Alert

THRESHOLDS = {
    'C': {'high': 80, 'medium': 60, 'low': 40},
    '%': {'high': 90, 'medium': 70, 'low': 50},
    'hPa': {'high': 1050, 'medium': 1030, 'low': 900},
}

def check_anomaly(sensor_data):
    unit = sensor_data.unit
    value = sensor_data.value

    if unit not in THRESHOLDS:
        return
    
    thresholds = THRESHOLDS[unit]

    if value >= thresholds['high']:
        severity = 'high'
        message = f"{sensor_data.device.name}: {value}{unit} exceeded high threshold ({thresholds['high']}{unit})"
    elif value >= thresholds['medium']:
        severity = 'medium'
        message = f"{sensor_data.device.name}: {value}{unit} exceeded medium threshold ({thresholds['medium']}{unit})"
    elif value >= thresholds['low']:
        severity = 'low'
        message = f"{sensor_data.device.name}: {value}{unit} exceeded low threshold ({thresholds['low']}{unit})"
    else:
        return
    
    Alert.objects.create(
        device=sensor_data.device,
        sensor_data=sensor_data,
        message=message,
        severity=severity
    )