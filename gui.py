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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ProgressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.ProgressBar.setGeometry(QtCore.QRect(620, 10, 151, 431))
        self.ProgressBar.setProperty("value", 0)
        self.ProgressBar.setTextVisible(False)
        self.ProgressBar.setOrientation(QtCore.Qt.Vertical)
        self.ProgressBar.setInvertedAppearance(False)
        self.ProgressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.ProgressBar.setObjectName("ProgressBar")
        self.PumpCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.PumpCheckBox.setEnabled(True)
        self.PumpCheckBox.setGeometry(QtCore.QRect(620, 450, 54, 17))
        self.PumpCheckBox.setObjectName("PumpCheckBox")
        self.StepLabel = QtWidgets.QLabel(self.centralwidget)
        self.StepLabel.setGeometry(QtCore.QRect(0, 0, 291, 261))
        self.StepLabel.setObjectName("StepLabel")
        self.TempUpButton = QtWidgets.QPushButton(self.centralwidget)
        self.TempUpButton.setGeometry(QtCore.QRect(729, 450, 51, 22))
        self.TempUpButton.setObjectName("TempUpButton")
        self.TempDownButton = QtWidgets.QPushButton(self.centralwidget)
        self.TempDownButton.setGeometry(QtCore.QRect(729, 470, 51, 22))
        self.TempDownButton.setObjectName("TempDownButton")
        self.PauseButton = QtWidgets.QPushButton(self.centralwidget)
        self.PauseButton.setGeometry(QtCore.QRect(619, 501, 161, 51))
        self.PauseButton.setObjectName("PauseButton")
        self.SensorLabel = QtWidgets.QLabel(self.centralwidget)
        self.SensorLabel.setGeometry(QtCore.QRect(10, 340, 201, 121))
        self.SensorLabel.setText("")
        self.SensorLabel.setObjectName("SensorLabel")
        self.TimeUpButton = QtWidgets.QPushButton(self.centralwidget)
        self.TimeUpButton.setGeometry(QtCore.QRect(680, 450, 51, 23))
        self.TimeUpButton.setObjectName("TimeUpButton")
        self.TimeDownButton = QtWidgets.QPushButton(self.centralwidget)
        self.TimeDownButton.setGeometry(QtCore.QRect(680, 470, 51, 23))
        self.TimeDownButton.setObjectName("TimeDownButton")
        self.MainTempLabel = QtWidgets.QLabel(self.centralwidget)
        self.MainTempLabel.setGeometry(QtCore.QRect(620, 190, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.MainTempLabel.setFont(font)
        self.MainTempLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MainTempLabel.setObjectName("MainTempLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BrewLinker"))
        self.ProgressBar.setFormat(_translate("MainWindow", "%p"))
        self.PumpCheckBox.setText(_translate("MainWindow", "Pumps"))
        self.StepLabel.setText(_translate("MainWindow", "TextLabel"))
        self.TempUpButton.setText(_translate("MainWindow", "↑🌡"))
        self.TempDownButton.setText(_translate("MainWindow", "↓🌡"))
        self.PauseButton.setText(_translate("MainWindow", "Pause"))
        self.TimeUpButton.setText(_translate("MainWindow", "↑🕐"))
        self.TimeDownButton.setText(_translate("MainWindow", "↓🕐"))
        self.MainTempLabel.setText(_translate("MainWindow", "TextLabel"))

