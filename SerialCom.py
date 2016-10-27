import json
import argparse
from ArduinoCommunicator import ArduinoCommunicator
from DebugCommunicator import DebugCommunicator
import gui
from PyQt5 import QtWidgets
from Controller import Controller
import sys
from pubsub import pub


def update_temp(arg1):
    ui.progressBar.setProperty('value', arg1)

if __name__ == "__main__":
    global ui
    parser = argparse.ArgumentParser(description='Brewing process runner.')
    parser.add_argument('-s', dest="settings", default="settings.json",
                        help="Settings file")
    args = parser.parse_args()

    with open(args.settings, 'r') as settingsfile:
        settings = json.load(settingsfile)

    # coms = ArduinoCommunicator(settings['COM'], settings['sensor'])
    coms = DebugCommunicator(settings['COM'], settings['sensor'])

    control = Controller(settings, coms)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = gui.Ui_MainWindow()
    ui.setupUi(MainWindow)

    pub.subscribe(update_temp, 'MainTemp')

    MainWindow.show()
    sys.exit(app.exec_())
