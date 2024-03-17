# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pss-ttt-fnb.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QLabel,
    QListWidget, QListWidgetItem, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpinBox, QWidget)

class Ui_fleetBrowser(object):
    def setupUi(self, fleetBrowser):
        if not fleetBrowser.objectName():
            fleetBrowser.setObjectName(u"fleetBrowser")
        fleetBrowser.resize(343, 329)
        self.fleetNameList = QListWidget(fleetBrowser)
        self.fleetNameList.setObjectName(u"fleetNameList")
        self.fleetNameList.setGeometry(QRect(10, 10, 231, 231))
        self.copyFleetNameSearch = QPushButton(fleetBrowser)
        self.copyFleetNameSearch.setObjectName(u"copyFleetNameSearch")
        self.copyFleetNameSearch.setGeometry(QRect(260, 10, 81, 23))
        self.fleetNameCharLimitCheckBox = QCheckBox(fleetBrowser)
        self.fleetNameCharLimitCheckBox.setObjectName(u"fleetNameCharLimitCheckBox")
        self.fleetNameCharLimitCheckBox.setGeometry(QRect(60, 310, 111, 21))
        self.fleetNameCharLimiter = QSpinBox(fleetBrowser)
        self.fleetNameCharLimiter.setObjectName(u"fleetNameCharLimiter")
        self.fleetNameCharLimiter.setGeometry(QRect(10, 310, 41, 21))
        self.fleetNameFilterBox = QPlainTextEdit(fleetBrowser)
        self.fleetNameFilterBox.setObjectName(u"fleetNameFilterBox")
        self.fleetNameFilterBox.setGeometry(QRect(10, 260, 231, 31))
        self.fleetNameSearch = QLabel(fleetBrowser)
        self.fleetNameSearch.setObjectName(u"fleetNameSearch")
        self.fleetNameSearch.setGeometry(QRect(10, 290, 231, 21))
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        self.fleetNameSearch.setFont(font)
        self.fleetNameSearch.setLayoutDirection(Qt.LeftToRight)
        self.fleetNameSearch.setAlignment(Qt.AlignCenter)
        self.fleetNameSearchClose = QPushButton(fleetBrowser)
        self.fleetNameSearchClose.setObjectName(u"fleetNameSearchClose")
        self.fleetNameSearchClose.setGeometry(QRect(260, 40, 81, 23))

        self.retranslateUi(fleetBrowser)

        QMetaObject.connectSlotsByName(fleetBrowser)
    # setupUi

    def retranslateUi(self, fleetBrowser):
        fleetBrowser.setWindowTitle(QCoreApplication.translate("fleetBrowser", u"Fleet Name Browser", None))
        self.copyFleetNameSearch.setText(QCoreApplication.translate("fleetBrowser", u"Copy && Close", None))
        self.fleetNameCharLimitCheckBox.setText(QCoreApplication.translate("fleetBrowser", u"Limit characters", None))
        self.fleetNameSearch.setText(QCoreApplication.translate("fleetBrowser", u"Fleet Name Filter", None))
        self.fleetNameSearchClose.setText(QCoreApplication.translate("fleetBrowser", u"Close", None))
    # retranslateUi

