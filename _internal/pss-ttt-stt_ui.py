# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pss-ttt-stt.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHeaderView, QLabel,
    QPlainTextEdit, QPushButton, QSizePolicy, QTableView,
    QWidget)

class Ui_starTargetTracking(object):
    def setupUi(self, starTargetTracking):
        if not starTargetTracking.objectName():
            starTargetTracking.setObjectName(u"starTargetTracking")
        starTargetTracking.resize(652, 755)
        self.dayFourTable = QTableView(starTargetTracking)
        self.dayFourTable.setObjectName(u"dayFourTable")
        self.dayFourTable.setGeometry(QRect(0, 80, 321, 261))
        self.dayFiveTable = QTableView(starTargetTracking)
        self.dayFiveTable.setObjectName(u"dayFiveTable")
        self.dayFiveTable.setGeometry(QRect(320, 80, 321, 261))
        self.daySixTable = QTableView(starTargetTracking)
        self.daySixTable.setObjectName(u"daySixTable")
        self.daySixTable.setGeometry(QRect(0, 400, 321, 261))
        self.daySevenTable = QTableView(starTargetTracking)
        self.daySevenTable.setObjectName(u"daySevenTable")
        self.daySevenTable.setGeometry(QRect(320, 400, 321, 261))
        self.dayFourCopy = QPushButton(starTargetTracking)
        self.dayFourCopy.setObjectName(u"dayFourCopy")
        self.dayFourCopy.setGeometry(QRect(190, 340, 81, 31))
        self.dayFourRemove = QPushButton(starTargetTracking)
        self.dayFourRemove.setObjectName(u"dayFourRemove")
        self.dayFourRemove.setGeometry(QRect(130, 340, 61, 31))
        self.dayFourAdd = QPushButton(starTargetTracking)
        self.dayFourAdd.setObjectName(u"dayFourAdd")
        self.dayFourAdd.setGeometry(QRect(80, 340, 51, 31))
        self.daySixCopy = QPushButton(starTargetTracking)
        self.daySixCopy.setObjectName(u"daySixCopy")
        self.daySixCopy.setGeometry(QRect(180, 660, 81, 31))
        self.daySixRemove = QPushButton(starTargetTracking)
        self.daySixRemove.setObjectName(u"daySixRemove")
        self.daySixRemove.setGeometry(QRect(120, 660, 61, 31))
        self.daySixAdd = QPushButton(starTargetTracking)
        self.daySixAdd.setObjectName(u"daySixAdd")
        self.daySixAdd.setGeometry(QRect(70, 660, 51, 31))
        self.daySevenCopy = QPushButton(starTargetTracking)
        self.daySevenCopy.setObjectName(u"daySevenCopy")
        self.daySevenCopy.setGeometry(QRect(500, 660, 81, 31))
        self.daySevenRemove = QPushButton(starTargetTracking)
        self.daySevenRemove.setObjectName(u"daySevenRemove")
        self.daySevenRemove.setGeometry(QRect(440, 660, 61, 31))
        self.daySevenAdd = QPushButton(starTargetTracking)
        self.daySevenAdd.setObjectName(u"daySevenAdd")
        self.daySevenAdd.setGeometry(QRect(390, 660, 51, 31))
        self.dayFiveCopy = QPushButton(starTargetTracking)
        self.dayFiveCopy.setObjectName(u"dayFiveCopy")
        self.dayFiveCopy.setGeometry(QRect(510, 340, 81, 31))
        self.dayFiveRemove = QPushButton(starTargetTracking)
        self.dayFiveRemove.setObjectName(u"dayFiveRemove")
        self.dayFiveRemove.setGeometry(QRect(450, 340, 61, 31))
        self.dayFiveAdd = QPushButton(starTargetTracking)
        self.dayFiveAdd.setObjectName(u"dayFiveAdd")
        self.dayFiveAdd.setGeometry(QRect(400, 340, 51, 31))
        self.label = QLabel(starTargetTracking)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 49, 321, 31))
        font = QFont()
        font.setFamilies([u"Arial Black"])
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(starTargetTracking)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(320, 50, 321, 31))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(starTargetTracking)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 370, 321, 31))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_4 = QLabel(starTargetTracking)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(320, 370, 321, 31))
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.playerNameSTTBox = QPlainTextEdit(starTargetTracking)
        self.playerNameSTTBox.setObjectName(u"playerNameSTTBox")
        self.playerNameSTTBox.setGeometry(QRect(0, 0, 161, 31))
        self.fleetNameSTTBox = QPlainTextEdit(starTargetTracking)
        self.fleetNameSTTBox.setObjectName(u"fleetNameSTTBox")
        self.fleetNameSTTBox.setGeometry(QRect(190, 0, 131, 31))
        self.lastStarsSTTBox = QPlainTextEdit(starTargetTracking)
        self.lastStarsSTTBox.setObjectName(u"lastStarsSTTBox")
        self.lastStarsSTTBox.setGeometry(QRect(350, 0, 131, 31))
        self.maxTrophiesSTTBox = QPlainTextEdit(starTargetTracking)
        self.maxTrophiesSTTBox.setObjectName(u"maxTrophiesSTTBox")
        self.maxTrophiesSTTBox.setGeometry(QRect(510, 0, 131, 31))
        self.trackerResetButton = QPushButton(starTargetTracking)
        self.trackerResetButton.setObjectName(u"trackerResetButton")
        self.trackerResetButton.setGeometry(QRect(260, 710, 131, 41))

        self.retranslateUi(starTargetTracking)

        QMetaObject.connectSlotsByName(starTargetTracking)
    # setupUi

    def retranslateUi(self, starTargetTracking):
        starTargetTracking.setWindowTitle(QCoreApplication.translate("starTargetTracking", u"Dialog", None))
        self.dayFourCopy.setText(QCoreApplication.translate("starTargetTracking", u"Copy&&Search", None))
        self.dayFourRemove.setText(QCoreApplication.translate("starTargetTracking", u"Remove", None))
        self.dayFourAdd.setText(QCoreApplication.translate("starTargetTracking", u"Add", None))
        self.daySixCopy.setText(QCoreApplication.translate("starTargetTracking", u"Copy&&Search", None))
        self.daySixRemove.setText(QCoreApplication.translate("starTargetTracking", u"Remove", None))
        self.daySixAdd.setText(QCoreApplication.translate("starTargetTracking", u"Add", None))
        self.daySevenCopy.setText(QCoreApplication.translate("starTargetTracking", u"Copy&&Search", None))
        self.daySevenRemove.setText(QCoreApplication.translate("starTargetTracking", u"Remove", None))
        self.daySevenAdd.setText(QCoreApplication.translate("starTargetTracking", u"Add", None))
        self.dayFiveCopy.setText(QCoreApplication.translate("starTargetTracking", u"Copy&&Search", None))
        self.dayFiveRemove.setText(QCoreApplication.translate("starTargetTracking", u"Remove", None))
        self.dayFiveAdd.setText(QCoreApplication.translate("starTargetTracking", u"Add", None))
        self.label.setText(QCoreApplication.translate("starTargetTracking", u"Day 4", None))
        self.label_2.setText(QCoreApplication.translate("starTargetTracking", u"Day 5", None))
        self.label_3.setText(QCoreApplication.translate("starTargetTracking", u"Day 6", None))
        self.label_4.setText(QCoreApplication.translate("starTargetTracking", u"Day 7", None))
        self.trackerResetButton.setText(QCoreApplication.translate("starTargetTracking", u"Reset", None))
    # retranslateUi

