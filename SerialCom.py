import serial
import io
from time import sleep
from struct import pack
import binascii

sio = None

def getTemperatures():
	ser.write(bytes([1]))
	ser.flush()
	res = dict()
	for i in range(int(sio.readline())):
		addr = sio.readline().strip() #Right side evaluates first
		res[addr] = float(sio.readline())
	return res

def setTemperature(temp):
	bts = pack('f', temp)
	ser.write(bytes([2]))
	ser.write(bts)
	ser.flush()
	print(sio.readline())

def setTarget(target):
	ser.write(bytes([3]))
	ser.write(bytes(map(lambda x: int(x,16), target.split(" "))))
	ser.flush()
	print(sio.readline())

def setupSerial(port = 'COM9'):
	global sio, ser
	ser = serial.Serial(
	    port='COM9',
	    baudrate=9600,
	    timeout = 3
	)
	sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser, buffer_size  = 1), encoding = 'ascii', newline = None)
	sio._CHUNK_SIZE = 1 #Why the fuck! Just emit a sting as sson as it is done! I understand the need to buffer, but really, why not emit stuff on newlines???
	sleep(10)


setupSerial()

setTemperature(32.5)
setTarget('0x28 0xFF 0x20 0x23 0x4B 0x4 0x0 0x83')

while True:
	print(getTemperatures())
	sleep(1)	