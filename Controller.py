from time import sleep, time
import datetime
from pymsgbox import *
import threading
from pubsub import pub
import Steps


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

        op = Steps.parse(command)
        if op.tag == 'TARGET':
            print('TARGET command deprecated, use settings file.')
        if op.tag == 'HEAT':
            self.coms.set_temperature(op.temp)
            while True:
                temps = self.coms.get_temperatures()
                print(index, '-', self.name_sensors(temps))
                try:
                    if temps[self.coms.sensor] >= op.temp:
                        break
                except KeyError:
                    print('Unknown target sensor {}!'.format(self.coms.sensor))
                    print('Connected sensors are:')
                    print('\n'.join(*temps.keys()))
                    exit(1)
                pub.sendMessage('MainTemp', arg1=temps[self.coms.sensor])
                sleep(5)
        if op.tag == 'COOK':
            start = time()
            self.coms.set_temperature(op.temp)
            while True:
                temps = self.coms.get_temperatures()
                print(index, '-', self.name_sensors(temps))
                remaining = start + op.time - time()
                if remaining < 0:
                    break
                print('Time remaining:', datetime.timedelta(seconds=remaining))
                pub.sendMessage('MainTemp', arg1=temps[self.coms.sensor])
                sleep(5)
        if op.tag == 'PAUSE':
            self.coms.set_temperature(-100000000.0)
            alert(text=op.msg, title='', button='OK')
        if op.tag == 'DONE':
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
