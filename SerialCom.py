from time import sleep, time
from pymsgbox import *
import json
import datetime
import argparse
from ArduinoCommunicator import ArduinoCommunicator
from DebugCommunicator import DebugCommunicator

parser = argparse.ArgumentParser(description='Brewing process runner.')
parser.add_argument('-s', dest="settings", default="settings.json",
                    help="Settings file")
args = parser.parse_args()

with open(args.settings, 'r') as settingsfile:
    settings = json.load(settingsfile)


def name_sensors(raw):
    return dict((settings['names'].get(k) or k, v) for k, v in raw.items())


def evaluate(command, index, coms):
    if not command:
        return
    print(command, '----')
    if command[0] == '#':
        return
    op, *args = command.split(' ')
    if op == 'TARGET':
        print('TARGET command deprecated, use settings file.')
    if op == 'HEAT':
        coms.set_temperature(float(args[0]))
        while True:
            temps = coms.get_temperatures()
            print(index, '-', name_sensors(temps))
            try:
                if temps[coms.sensor] >= float(args[0]):
                    break
            except KeyError:
                print('Unknown target sensor {}!'.format(coms.sensor))
                print('Connected sensors are:')
                print('\n'.join(*temps.keys()))
                exit(1)
            sleep(5)
    if op == 'COOK':
        start = time()
        coms.set_temperature(float(args[0]))
        while True:
            temps = coms.get_temperatures()
            print(index, '-', name_sensors(temps))
            remaining = start + float(args[1]) * 60.0 - time()
            if remaining < 0:
                break
            print('Time remaining:', datetime.timedelta(seconds=remaining))
            sleep(5)
    if op == 'PAUSE':
        alert(text=' '.join(args), title='', button='OK')
    if op == 'DONE':
        coms.set_temperature(-100000000.0)
        coms.set_target('0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0')


if __name__ == "__main__":
    i = 1
    coms = ArduinoCommunicator(settings['COM'], settings['sensor'])
    # coms = DebugCommunicator(settings['COM'], settings['sensor'])
    while(True):
        evaluate(input().strip(), i, coms)
        i += 1
