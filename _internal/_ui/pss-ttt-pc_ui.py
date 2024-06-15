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
from PySide6.QtWidgets import (QApplication, QDialog, QHeaderView, QPushButton,
    QScrollArea, QSizePolicy, QTreeView, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(711, 289)
        self.treeView = QTreeView(Dialog)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setGeometry(QRect(50, 40, 256, 192))
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(320, 30, 75, 23))
        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(320, 60, 75, 23))
        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(420, 30, 181, 191))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 179, 189))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.pushButton_3 = QPushButton(Dialog)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(320, 90, 75, 23))
        self.pushButton_4 = QPushButton(Dialog)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(320, 120, 75, 23))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"PushButton", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"PushButton", None))
        self.pushButton_4.setText(QCoreApplication.translate("Dialog", u"PushButton", None))
    # retranslateUi

