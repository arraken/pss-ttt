# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pss-ttt-fdb.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QLabel,
    QPlainTextEdit, QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(200, 206)
        self.submitFightDataButton = QPushButton(Dialog)
        self.submitFightDataButton.setObjectName(u"submitFightDataButton")
        self.submitFightDataButton.setGeometry(QRect(10, 160, 181, 41))
        self.fightRewardBox = QPlainTextEdit(Dialog)
        self.fightRewardBox.setObjectName(u"fightRewardBox")
        self.fightRewardBox.setGeometry(QRect(10, 20, 111, 31))
        self.fightHPBox = QPlainTextEdit(Dialog)
        self.fightHPBox.setObjectName(u"fightHPBox")
        self.fightHPBox.setGeometry(QRect(10, 60, 111, 31))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(120, 20, 101, 21))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(120, 60, 101, 21))
        self.fightResultBox = QComboBox(Dialog)
        self.fightResultBox.addItem("")
        self.fightResultBox.addItem("")
        self.fightResultBox.addItem("")
        self.fightResultBox.setObjectName(u"fightResultBox")
        self.fightResultBox.setGeometry(QRect(10, 100, 111, 22))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(120, 100, 101, 16))
        self.fightTypeBox = QComboBox(Dialog)
        self.fightTypeBox.addItem("")
        self.fightTypeBox.addItem("")
        self.fightTypeBox.addItem("")
        self.fightTypeBox.setObjectName(u"fightTypeBox")
        self.fightTypeBox.setGeometry(QRect(10, 130, 111, 22))
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(120, 130, 101, 16))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.submitFightDataButton.setText(QCoreApplication.translate("Dialog", u"Submit", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Trophies/Stars", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Remaining HP", None))
        self.fightResultBox.setItemText(0, QCoreApplication.translate("Dialog", u"Win", None))
        self.fightResultBox.setItemText(1, QCoreApplication.translate("Dialog", u"Loss", None))
        self.fightResultBox.setItemText(2, QCoreApplication.translate("Dialog", u"Draw/Flee", None))

        self.label_3.setText(QCoreApplication.translate("Dialog", u"Result", None))
        self.fightTypeBox.setItemText(0, QCoreApplication.translate("Dialog", u"legends", None))
        self.fightTypeBox.setItemText(1, QCoreApplication.translate("Dialog", u"tourny", None))
        self.fightTypeBox.setItemText(2, QCoreApplication.translate("Dialog", u"pvp", None))

        self.label_4.setText(QCoreApplication.translate("Dialog", u"Fight Type", None))
    # retranslateUi

