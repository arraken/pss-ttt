# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pss-ttt-clb.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(939, 340)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 40, 51, 31))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 80, 51, 31))
        self.bodyEquipBox = QLineEdit(Dialog)
        self.bodyEquipBox.setObjectName(u"bodyEquipBox")
        self.bodyEquipBox.setGeometry(QRect(60, 40, 211, 31))
        self.headEquipBox = QLineEdit(Dialog)
        self.headEquipBox.setObjectName(u"headEquipBox")
        self.headEquipBox.setGeometry(QRect(60, 80, 211, 31))
        self.crewName = QLineEdit(Dialog)
        self.crewName.setObjectName(u"crewName")
        self.crewName.setGeometry(QRect(130, 10, 113, 20))
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(250, 10, 51, 23))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 120, 51, 31))
        self.accessEquipBox = QLineEdit(Dialog)
        self.accessEquipBox.setObjectName(u"accessEquipBox")
        self.accessEquipBox.setGeometry(QRect(60, 160, 211, 31))
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 160, 51, 31))
        self.legEquipBox = QLineEdit(Dialog)
        self.legEquipBox.setObjectName(u"legEquipBox")
        self.legEquipBox.setGeometry(QRect(60, 120, 211, 31))
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 200, 51, 31))
        self.petEquipBox = QLineEdit(Dialog)
        self.petEquipBox.setObjectName(u"petEquipBox")
        self.petEquipBox.setGeometry(QRect(60, 240, 211, 31))
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 240, 51, 31))
        self.wepEquipBox = QLineEdit(Dialog)
        self.wepEquipBox.setObjectName(u"wepEquipBox")
        self.wepEquipBox.setGeometry(QRect(60, 200, 211, 31))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Body", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Head", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Load", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Leg", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Accessory", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Weapon", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Pet", None))
    # retranslateUi

