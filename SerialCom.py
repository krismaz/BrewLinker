import json
import argparse
from ArduinoCommunicator import ArduinoCommunicator
from DebugCommunicator import DebugCommunicator
import gui
from PyQt5 import QtWidgets
from Controller import Controller
import sys


def update_temp(arg1):
    ui.ProgressBar.setProperty('value', arg1)
    ui.MainTempLabel.setText('{:.1f}°'.format(arg1))


def update_pump(arg1):
    ui.PumpCheckBox.setProperty('checked', arg1)


def update_list(arg1):
    text = '\n'.join(('> ' if step == control.current_step else '   ') + str(step) for step in arg1)
    ui.StepLabel.setText(text)


def update_sensors(arg1):
    text = '\n'.join('{}: {:.1f}°'.format(k,v) for k,v in arg1.items())
    ui.SensorLabel.setText(text)


if __name__ == "__main__":
    global ui
    parser = argparse.ArgumentParser(description='Brewing process runner.')
    parser.add_argument('-s', dest="settings", default="settings.json",
                        help="Settings file")
    parser.add_argument('script', type=str, help='script file')
    args = parser.parse_args()

    with open(args.settings, 'r') as settingsfile:
        settings = json.load(settingsfile)

    with open(args.script, 'r') as sriptFile:
        script = sriptFile.readlines()

    coms = ArduinoCommunicator(settings['COM'], settings['sensor'])
    #coms = DebugCommunicator(settings['COM'], settings['sensor'])

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    MainWindow = QtWidgets.QMainWindow()
    ui = gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    control = Controller(settings, coms, script, MainWindow)

    update_list(control.program)

    control.pump_changed.connect(update_pump)
    control.temp_changed.connect(update_temp)
    control.program_changed.connect(update_list)
    control.sensors_changed.connect(update_sensors)

    ui.PumpCheckBox.stateChanged.connect(lambda x: control.pump_toggle(bool(x)))

    ui.TempUpButton.clicked.connect(lambda x: control.shift_temp(0.5))
    ui.TempDownButton.clicked.connect(lambda x: control.shift_temp(-0.5))
    ui.TimeUpButton.clicked.connect(lambda x: control.shift_time(30))
    ui.TimeDownButton.clicked.connect(lambda x: control.shift_time(-30))
    ui.StepUpButton.clicked.connect(lambda x: control.shift_step(1))
    ui.StepDownButton.clicked.connect(lambda x: control.shift_step(-1))
    ui.PauseButton.clicked.connect(lambda x: control.request_pause())

    control.start()

    MainWindow.show()
    sys.exit(app.exec_())
