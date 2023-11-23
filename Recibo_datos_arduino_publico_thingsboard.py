import serial
import time
import paho.mqtt.client as mqtt
import json



# Configuración de Thingsboard
THINGSBOARD_HOST = 'thingsboard.cloud'  # Cambia esto por tu host de Thingsboard
ACCESS_TOKEN = 'KstFC9vkof2YJ56MiUbi'  # Cambia esto por tu token de acceso

# Configuración del puerto COM
SERIAL_PORT = "COM3"  # Cambia esto por el puerto COM que estés usando
BAUD_RATE = 9600


# Inicializa el cliente MQTT
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)

# Conecta al cliente MQTT
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()

try:
    # Abre el puerto COM
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

    while True:
        # Lee una línea del puerto COM
        line = ser.readline().decode('utf-8').strip()

        # Convierte la línea en un objeto JSON
        data = json.loads(line)
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            print(f"Error al decodificar JSON: {line}")
        # Publica los datos en Thingsboard
        client.publish('v1/devices/me/telemetry', json.dumps(data), 1) 
        print(data)



except KeyboardInterrupt:
    pass
finally:
    ser.close()
    client.loop_stop()
    client.disconnect()