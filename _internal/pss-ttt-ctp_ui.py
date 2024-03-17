# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pss-ttt-ctp.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHeaderView, QPlainTextEdit,
    QPushButton, QSizePolicy, QTableView, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(639, 249)
        self.presetTableView = QTableView(Dialog)
        self.presetTableView.setObjectName(u"presetTableView")
        self.presetTableView.setGeometry(QRect(0, 10, 471, 231))
        self.savePresetButton = QPushButton(Dialog)
        self.savePresetButton.setObjectName(u"savePresetButton")
        self.savePresetButton.setGeometry(QRect(520, 50, 81, 31))
        self.deletePresetButton = QPushButton(Dialog)
        self.deletePresetButton.setObjectName(u"deletePresetButton")
        self.deletePresetButton.setGeometry(QRect(520, 170, 81, 31))
        self.presetCrewNameBox = QPlainTextEdit(Dialog)
        self.presetCrewNameBox.setObjectName(u"presetCrewNameBox")
        self.presetCrewNameBox.setGeometry(QRect(490, 10, 141, 31))
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(9)
        font.setBold(True)
        self.presetCrewNameBox.setFont(font)
        self.presetCrewNameBox.setTabChangesFocus(True)
        self.loadPresetButton = QPushButton(Dialog)
        self.loadPresetButton.setObjectName(u"loadPresetButton")
        self.loadPresetButton.setGeometry(QRect(520, 90, 81, 31))
        QWidget.setTabOrder(self.presetCrewNameBox, self.savePresetButton)
        QWidget.setTabOrder(self.savePresetButton, self.loadPresetButton)
        QWidget.setTabOrder(self.loadPresetButton, self.deletePresetButton)
        QWidget.setTabOrder(self.deletePresetButton, self.presetTableView)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Crew Trainer Presets", None))
        self.savePresetButton.setText(QCoreApplication.translate("Dialog", u"Save Preset", None))
        self.deletePresetButton.setText(QCoreApplication.translate("Dialog", u"Delete Preset", None))
        self.presetCrewNameBox.setPlaceholderText(QCoreApplication.translate("Dialog", u"Enter Crew Name Here", None))
        self.loadPresetButton.setText(QCoreApplication.translate("Dialog", u"Load Preset", None))
    # retranslateUi

