# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(620, 10, 151, 431))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Vertical)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setEnabled(True)
        self.checkBox.setGeometry(QtCore.QRect(620, 450, 54, 17))
        self.checkBox.setObjectName("checkBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 291, 261))
        self.label.setObjectName("label")
        self.upButton = QtWidgets.QPushButton(self.centralwidget)
        self.upButton.setGeometry(QtCore.QRect(729, 450, 51, 22))
        self.upButton.setObjectName("upButton")
        self.downButton = QtWidgets.QPushButton(self.centralwidget)
        self.downButton.setGeometry(QtCore.QRect(729, 470, 51, 22))
        self.downButton.setObjectName("downButton")
        self.pauseButton = QtWidgets.QPushButton(self.centralwidget)
        self.pauseButton.setGeometry(QtCore.QRect(619, 501, 161, 51))
        self.pauseButton.setObjectName("pauseButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 340, 201, 121))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.timeUpButton = QtWidgets.QPushButton(self.centralwidget)
        self.timeUpButton.setGeometry(QtCore.QRect(680, 450, 51, 23))
        self.timeUpButton.setObjectName("timeUpButton")
        self.timeDownButton = QtWidgets.QPushButton(self.centralwidget)
        self.timeDownButton.setGeometry(QtCore.QRect(680, 470, 51, 23))
        self.timeDownButton.setObjectName("timeDownButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.progressBar.setFormat(_translate("MainWindow", "%p"))
        self.checkBox.setText(_translate("MainWindow", "Pumps"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.upButton.setText(_translate("MainWindow", "↑🌡"))
        self.downButton.setText(_translate("MainWindow", "↓🌡"))
        self.pauseButton.setText(_translate("MainWindow", "Pause"))
        self.timeUpButton.setText(_translate("MainWindow", "↑🕐"))
        self.timeDownButton.setText(_translate("MainWindow", "↓🕐"))

