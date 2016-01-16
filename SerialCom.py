import serial
import io
from time import sleep, time
from struct import pack
import binascii
from pymsgbox import *

sio = None

lasttarget = ''

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
	print('Target set:', sio.readline())

def setTarget(target):
	global lasttarget
	lasttarget = target
	ser.write(bytes([3]))
	ser.write(bytes(map(lambda x: int(x,16), target.split(" "))))
	ser.flush()
	print('Temp set:', sio.readline())

def setupSerial(port = 'COM9'):
	print('a')
	global sio, ser
	ser = serial.Serial(
	    port='/dev/ttyACM1',
	    baudrate=9600,
	    timeout = 3
	)
	print('a')
	
	sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser, buffer_size  = 1), encoding = 'ascii', newline = None)
	sio._CHUNK_SIZE = 1 #Why the fuck! Just emit a sting as sson as it is done! I understand the need to buffer, but really, why not emit stuff on newlines???
	
	print('a')
	sleep(10)
	print('a')


def evaluate(command, index):
	if not command:
		return
	print(command, '----')
	if command[0] == '#':
		return
	op, *args = command.split(' ')
	if op == 'TARGET':
		setTarget(' '.join(args))
	if op == 'HEAT':
		setTemperature(float(args[0]))
		while True:
			temps = getTemperatures()
			print(index, '-', temps)
			if temps[lasttarget] >= float(args[0]):
				break
			sleep(5)
	if op == 'COOK':
		start = time()
		setTemperature(float(args[0]))
		while True:
			temps = getTemperatures()
			print(index, '-', temps)
			if time() > start + float(args[1])*60.0:
				break
			sleep(5)
	if op == 'PAUSE':
		alert(text=' '.join(args), title='', button='OK')
	if op == 'DONE':
		setTemperature(-100000000.0)
		setTarget('0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0')

i = 1

if __name__ == "__main__":
	setupSerial()
	
	while(True):
		evaluate(input().strip(), i)
		i += 1
