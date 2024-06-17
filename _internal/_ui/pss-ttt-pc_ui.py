# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pss-ttt-pc.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(611, 494)
        self.mergeCrewButton = QPushButton(Dialog)
        self.mergeCrewButton.setObjectName(u"mergeCrewButton")
        self.mergeCrewButton.setGeometry(QRect(10, 370, 161, 23))
        self.oneStepRecipeCheckButton = QPushButton(Dialog)
        self.oneStepRecipeCheckButton.setObjectName(u"oneStepRecipeCheckButton")
        self.oneStepRecipeCheckButton.setGeometry(QRect(260, 410, 161, 23))
        self.addCrewButton = QPushButton(Dialog)
        self.addCrewButton.setObjectName(u"addCrewButton")
        self.addCrewButton.setGeometry(QRect(10, 400, 161, 23))
        self.deleteCrewButton = QPushButton(Dialog)
        self.deleteCrewButton.setObjectName(u"deleteCrewButton")
        self.deleteCrewButton.setGeometry(QRect(10, 430, 161, 23))
        self.currentCrewList = QListWidget(Dialog)
        self.currentCrewList.setObjectName(u"currentCrewList")
        self.currentCrewList.setGeometry(QRect(10, 40, 161, 321))
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(12)
        self.currentCrewList.setFont(font)
        self.currentCrewList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 19, 161, 21))
        font1 = QFont()
        font1.setFamilies([u"Calibri"])
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setKerning(True)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)
        self.oneStepPrestigeList = QListWidget(Dialog)
        self.oneStepPrestigeList.setObjectName(u"oneStepPrestigeList")
        self.oneStepPrestigeList.setGeometry(QRect(260, 40, 161, 321))
        self.oneStepPrestigeList.setFont(font)
        self.oneStepPrestigeList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.twoStepPrestigeList = QListWidget(Dialog)
        self.twoStepPrestigeList.setObjectName(u"twoStepPrestigeList")
        self.twoStepPrestigeList.setGeometry(QRect(430, 40, 161, 321))
        self.twoStepPrestigeList.setFont(font)
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(260, 20, 161, 21))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(430, 20, 161, 21))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(260, 370, 161, 31))
        self.clearCrewListButton = QPushButton(Dialog)
        self.clearCrewListButton.setObjectName(u"clearCrewListButton")
        self.clearCrewListButton.setGeometry(QRect(10, 460, 161, 23))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.mergeCrewButton.setText(QCoreApplication.translate("Dialog", u"Merge Selected", None))
        self.oneStepRecipeCheckButton.setText(QCoreApplication.translate("Dialog", u"Recipe Check", None))
        self.addCrewButton.setText(QCoreApplication.translate("Dialog", u"Add Crew", None))
        self.deleteCrewButton.setText(QCoreApplication.translate("Dialog", u"Delete Crew", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Current Crew", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"1 Step Prestige", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"2 Step Prestige", None))
        self.clearCrewListButton.setText(QCoreApplication.translate("Dialog", u"Clear List", None))
    # retranslateUi

