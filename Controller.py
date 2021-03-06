from time import sleep, time
import datetime
from pymsgbox import *
import Steps
from PyQt5.QtCore import QThread, pyqtSignal


class Controller(QThread):
    program_changed = pyqtSignal([object])
    sensors_changed = pyqtSignal(object)
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
        self.to_pause = False
        self.to_break = False
        self.next_step = 0

    def name_sensors(self, raw):
        return dict((self.settings['names'].get(k) or k, v) for k, v in raw.items())

    def evaluate(self, op, index):
        self.program_changed.emit(self.program)
        self.to_pause = False
        if op.tag == 'TARGET':
            print('TARGET command deprecated, use settings file.')
        if op.tag == 'HEAT':
            self.coms.set_temperature(op.temp)
            while not self.to_break:
                temps = self.coms.get_temperatures()
                self.sensors_changed.emit(self.name_sensors(temps))
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
                if self.to_pause:
                    self.coms.set_temperature(-100000000.0)
                    alert(text='PAUSE', title='', button='OK')
                    self.to_pause = False
                    self.coms.set_temperature(op.temp)
                sleep(5)
        if op.tag == 'COOK':
            start = time()
            self.coms.set_temperature(op.temp)
            while not self.to_break:
                temps = self.coms.get_temperatures()
                self.sensors_changed.emit(self.name_sensors(temps))
                print(index, '-', self.name_sensors(temps))
                remaining = start + op.time - time()
                if remaining < 0:
                    break
                print('Time remaining:', datetime.timedelta(seconds=remaining))
                self.temp_changed.emit(temps[self.coms.sensor])
                if self.to_pause:
                    pauseStart = time()
                    self.coms.set_temperature(-100000000.0)
                    alert(text='PAUSE', title='', button='OK')
                    self.to_pause = False
                    self.coms.set_temperature(op.temp)
                    start += time() - pauseStart
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
            if not self.to_pause:
                self.coms.set_temperature(self.current_step.temp)
            self.program_changed.emit(self.program)
        except Exception as e:
            print(e)

    def shift_time(self, diff):
        try:
            self.current_step.time += diff
            self.program_changed.emit(self.program)
        except Exception as e:
            print(e)

    def shift_step(self, diff):
        if not self.to_break:
            diff -= 1
        self.next_step = max(0, self.next_step + diff)
        self.to_break = True



    def request_pause(self):
        self.to_pause = True

    def brew_loop(self):
        while self.next_step < len(self.program):
            self.current_step = self.program[self.next_step]
            self.next_step += 1
            self.to_break = False
            self.evaluate(self.current_step, self.next_step-1)

    def run(self):
        self.brew_loop()
