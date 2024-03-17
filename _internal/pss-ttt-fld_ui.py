# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pss-ttt-fld.ui'
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
        self.itemList = QListWidget(fleetBrowser)
        self.itemList.setObjectName(u"itemList")
        self.itemList.setGeometry(QRect(10, 10, 231, 231))
        self.copyItemSearch = QPushButton(fleetBrowser)
        self.copyItemSearch.setObjectName(u"copyItemSearch")
        self.copyItemSearch.setGeometry(QRect(260, 10, 81, 23))
        self.charLimiterCheckBox = QCheckBox(fleetBrowser)
        self.charLimiterCheckBox.setObjectName(u"charLimiterCheckBox")
        self.charLimiterCheckBox.setGeometry(QRect(60, 310, 111, 21))
        self.charLimiter = QSpinBox(fleetBrowser)
        self.charLimiter.setObjectName(u"charLimiter")
        self.charLimiter.setGeometry(QRect(10, 310, 41, 21))
        self.filterBox = QPlainTextEdit(fleetBrowser)
        self.filterBox.setObjectName(u"filterBox")
        self.filterBox.setGeometry(QRect(10, 260, 231, 31))
        self.filterBox.setTabChangesFocus(True)
        self.filterLabel = QLabel(fleetBrowser)
        self.filterLabel.setObjectName(u"filterLabel")
        self.filterLabel.setGeometry(QRect(10, 290, 231, 21))
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        self.filterLabel.setFont(font)
        self.filterLabel.setLayoutDirection(Qt.LeftToRight)
        self.filterLabel.setAlignment(Qt.AlignCenter)
        self.itemSearchClose = QPushButton(fleetBrowser)
        self.itemSearchClose.setObjectName(u"itemSearchClose")
        self.itemSearchClose.setGeometry(QRect(260, 40, 81, 23))

        self.retranslateUi(fleetBrowser)

        QMetaObject.connectSlotsByName(fleetBrowser)
    # setupUi

    def retranslateUi(self, fleetBrowser):
        fleetBrowser.setWindowTitle(QCoreApplication.translate("fleetBrowser", u"Filtered List Dialog", None))
        self.copyItemSearch.setText(QCoreApplication.translate("fleetBrowser", u"Copy && Close", None))
        self.charLimiterCheckBox.setText(QCoreApplication.translate("fleetBrowser", u"Limit characters", None))
        self.filterLabel.setText(QCoreApplication.translate("fleetBrowser", u"Fleet Name Filter", None))
        self.itemSearchClose.setText(QCoreApplication.translate("fleetBrowser", u"Close", None))
    # retranslateUi

