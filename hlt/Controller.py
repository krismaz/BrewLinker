from time import sleep, time
import datetime
from pymsgbox import *
import Steps
from PyQt5.QtCore import QThread, pyqtSignal


class Controller(QThread):
    program_changed = pyqtSignal([object])
    temp_changed = pyqtSignal(float)
    pump_changed = pyqtSignal(bool)
    

    def __init__(self, settings, coms, script, parent=None):
        QThread.__init__(self, parent)
        self.settings = settings
        self.coms = coms
        self.coms.pump_off()
        self.pump = False
        self.program = [step for step in map(Steps.parse, script) if step]
        self.current_step = None

    def name_sensors(self, raw):
        return dict((self.settings['names'].get(k) or k, v) for k, v in raw.items())

    def evaluate(self, op, index):
        self.program_changed.emit(self.program)
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
                self.temp_changed.emit(temps[self.coms.sensor])
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
                self.temp_changed.emit(temps[self.coms.sensor])
                sleep(5)
        if op.tag == 'PAUSE':
            self.coms.set_temperature(-100000000.0)
            alert(text=op.msg, title='', button='OK')
        if op.tag == 'DONE':
            self.coms.set_temperature(-100000000.0)
            self.coms.set_sensor('0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0')

    def pump_toggle(self, newState):
        if self.pump == newState:
            return
        if self.pump:
            self.coms.pump_off()
            self.pump = False
        else:
            self.coms.pump_on()
            self.pump = True
        self.pump_changed.emit(self.pump)

    def shift_temp(self, diff):
        try:
            self.current_step.temp += diff
            self.coms.set_temperature(self.current_step.temp)
            self.program_changed.emit(self.program)
        except Exception as e:
            print(e)


    def brew_loop(self):
        for i, step in enumerate(self.program):
            self.current_step = step
            self.evaluate(step, i)

    def run(self):
        self.brew_loop()
