from time import sleep, time


class DebugCommunicator:
    def __init__(self, port, sensor):
        self.setup_serial(port)
        self.set_sensor(sensor)
        self.start = time()

    def setup_serial(self, port):
        print('Connecting to', port)
        sleep(3)
        print('Connection done!')

    def set_sensor(self, sensor):
        self.sensor = sensor
        print('Sensor set:', sensor)

    def set_temperature(self, temp):
        print('Temperature set:', temp)

    def get_temperatures(self):
        return {self.sensor: time() - self.start}

    def pump_on(self):
        print('Pump on')

    def pump_off(self):
        print('Pump off')
