# Form implementation generated from reading ui file 'c:\Users\Kamguh\Documents\GitHub\pss-ttt\pss-ttt-fleetbrowser.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_fleetBrowser(object):
    def setupUi(self, fleetBrowser):
        fleetBrowser.setObjectName("fleetBrowser")
        fleetBrowser.resize(343, 339)
        self.fleetNameList = QtWidgets.QListWidget(parent=fleetBrowser)
        self.fleetNameList.setGeometry(QtCore.QRect(10, 10, 231, 231))
        self.fleetNameList.setObjectName("fleetNameList")
        self.copyFleetSearch = QtWidgets.QPushButton(parent=fleetBrowser)
        self.copyFleetSearch.setGeometry(QtCore.QRect(250, 10, 91, 23))
        self.copyFleetSearch.setObjectName("copyFleetSearch")
        self.charLimiterCheckBox = QtWidgets.QCheckBox(parent=fleetBrowser)
        self.charLimiterCheckBox.setGeometry(QtCore.QRect(250, 150, 101, 21))
        self.charLimiterCheckBox.setObjectName("charLimiterCheckBox")
        self.charLimiter = QtWidgets.QSpinBox(parent=fleetBrowser)
        self.charLimiter.setGeometry(QtCore.QRect(250, 170, 41, 21))
        self.charLimiter.setObjectName("charLimiter")
        self.fleetNameSearchBox = QtWidgets.QPlainTextEdit(parent=fleetBrowser)
        self.fleetNameSearchBox.setGeometry(QtCore.QRect(10, 260, 231, 31))
        self.fleetNameSearchBox.setObjectName("fleetNameSearchBox")
        self.fleetNameSearch = QtWidgets.QLabel(parent=fleetBrowser)
        self.fleetNameSearch.setGeometry(QtCore.QRect(10, 290, 231, 21))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.fleetNameSearch.setFont(font)
        self.fleetNameSearch.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.fleetNameSearch.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fleetNameSearch.setObjectName("fleetNameSearch")
        self.fleetSearchClose = QtWidgets.QPushButton(parent=fleetBrowser)
        self.fleetSearchClose.setGeometry(QtCore.QRect(250, 40, 91, 23))
        self.fleetSearchClose.setObjectName("fleetSearchClose")

        self.retranslateUi(fleetBrowser)
        QtCore.QMetaObject.connectSlotsByName(fleetBrowser)

    def retranslateUi(self, fleetBrowser):
        _translate = QtCore.QCoreApplication.translate
        fleetBrowser.setWindowTitle(_translate("fleetBrowser", "Fleet Browser"))
        self.copyFleetSearch.setText(_translate("fleetBrowser", "Copy && Close"))
        self.charLimiterCheckBox.setText(_translate("fleetBrowser", "Limit characters"))
        self.fleetNameSearch.setText(_translate("fleetBrowser", "Player Name Filter"))
        self.fleetSearchClose.setText(_translate("fleetBrowser", "Close"))
