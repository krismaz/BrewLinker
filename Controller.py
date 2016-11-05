from time import sleep, time
import datetime
from pymsgbox import *
import threading
from pubsub import pub


class Controller:
    def __init__(self, settings, coms):
        self.settings = settings
        self.coms = coms
        self.coms.pump_off()
        self.pump = False
        pub.subscribe(self.pump_toggle, 'PumpToggle')
        thread = threading.Thread(target=self.brew_loop)
        thread.start()

    def name_sensors(self, raw):
        return dict((self.settings['names'].get(k) or k, v) for k, v in raw.items())

    def evaluate(self, command, index):
        if not command:
            return
        print(command, '----')
        if command[0] == '#':
            return
        op, *args = command.split(' ')
        if op == 'TARGET':
            print('TARGET command deprecated, use settings file.')
        if op == 'HEAT':
            self.coms.set_temperature(float(args[0]))
            while True:
                temps = self.coms.get_temperatures()
                print(index, '-', self.name_sensors(temps))
                try:
                    if temps[self.coms.sensor] >= float(args[0]):
                        break
                except KeyError:
                    print('Unknown target sensor {}!'.format(self.coms.sensor))
                    print('Connected sensors are:')
                    print('\n'.join(*temps.keys()))
                    exit(1)
                pub.sendMessage('MainTemp', arg1=temps[self.coms.sensor])
                sleep(5)
        if op == 'COOK':
            start = time()
            coms.set_temperature(float(args[0]))
            while True:
                temps = self.coms.get_temperatures()
                print(index, '-', self.name_sensors(temps))
                remaining = start + float(args[1]) * 60.0 - time()
                if remaining < 0:
                    break
                print('Time remaining:', datetime.timedelta(seconds=remaining))
                pub.sendMessage('MainTemp', arg1=temps[self.coms.sensor])
                sleep(5)
        if op == 'PAUSE':
            self.coms.set_temperature(-100000000.0)
            alert(text=' '.join(args), title='', button='OK')
        if op == 'DONE':
            self.coms.set_temperature(-100000000.0)
            self.coms.set_target('0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0')

    def pump_toggle(self, newState):
        if self.pump == newState:
            return
        if self.pump:
            self.coms.pump_off()
            self.pump = False
        else:
            self.coms.pump_on()
            self.pump = True
        pub.sendMessage('PumpStatus', arg1=self.pump)

    def brew_loop(self):
        i = 1
        while(True):
            self.evaluate(input().strip(), i)
            i += 1
