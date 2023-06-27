from DIPPID import SensorUDP

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

def handle_sensordata(data):
    print(data)


sensor.register_callback('events', handle_sensordata)

while True:
    print('capabilities: ', sensor.get_capabilities())
    print(sensor.get_value('events'))
