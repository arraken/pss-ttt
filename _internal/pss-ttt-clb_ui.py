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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QDoubleSpinBox,
    QLabel, QLineEdit, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(419, 464)
        self.doubleSpinBox = QDoubleSpinBox(Dialog)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setGeometry(QRect(120, 280, 62, 22))
        self.doubleSpinBox.setDecimals(1)
        self.doubleSpinBox.setMinimum(0.100000000000000)
        self.doubleSpinBox.setMaximum(90.000000000000000)
        self.doubleSpinBox.setSingleStep(0.100000000000000)
        self.comboBox = QComboBox(Dialog)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(50, 280, 69, 22))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 40, 47, 21))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 90, 47, 21))
        self.bodyEquipBox = QLineEdit(Dialog)
        self.bodyEquipBox.setObjectName(u"bodyEquipBox")
        self.bodyEquipBox.setGeometry(QRect(40, 40, 113, 20))
        self.headEquipBox = QLineEdit(Dialog)
        self.headEquipBox.setObjectName(u"headEquipBox")
        self.headEquipBox.setGeometry(QRect(40, 90, 113, 20))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Body", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Head", None))
    # retranslateUi

