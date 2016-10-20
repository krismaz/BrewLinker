import serial
import io
from time import sleep
from struct import pack


class ArduinoCommunicator:
    def __init__(self, port, sensor):
        self.setup_serial(port)
        self.set_sensor(sensor)

    def setup_serial(self, port):
        print('Connecting to', port)
        try:
            ser = serial.Serial(
                port=port,
                baudrate=9600,
                timeout=3
            )
        except serial.serialutil.SerialException:
            print('Error communicating with device "{}"! \n'.format(port) +
                  'Have you provided the correct COM port?')
            exit(1)
        print('a')
        sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1),
                               encoding='ascii',
                               newline=None)
        sio._CHUNK_SIZE = 1
        print('Connection Established, waiting for ready...')
        sleep(10)
        print('Connection done!')
        self.ser, self.sio = ser, sio

    def set_sensor(self, sensor):
        self.sensor = sensor
        self.ser.write(bytes([3]))
        self.ser.write(bytes(map(lambda x: int(x, 16), sensor.split(" "))))
        self.ser.flush()
        print('Sensor set:', self.sio.readline())

    def set_temperature(self, temp):
        bts = pack('f', temp)
        self.ser.write(bytes([2]))
        self.ser.write(bts)
        self.ser.flush()
        print('Temperature set:', self.sio.readline())

    def get_temperatures(self):
        self.ser.write(bytes([1]))
        self.ser.flush()
        res = dict()
        for i in range(int(self.sio.readline())):
            addr = self.sio.readline().strip()  # Right side evaluates first
            res[addr] = float(self.sio.readline())
        return res
