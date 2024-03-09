# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pss-ttt-psb.ui'
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

class Ui_playerbrowser(object):
    def setupUi(self, playerbrowser):
        if not playerbrowser.objectName():
            playerbrowser.setObjectName(u"playerbrowser")
        playerbrowser.resize(343, 329)
        self.playerNameList = QListWidget(playerbrowser)
        self.playerNameList.setObjectName(u"playerNameList")
        self.playerNameList.setGeometry(QRect(10, 10, 231, 231))
        self.copyPlayerSearch = QPushButton(playerbrowser)
        self.copyPlayerSearch.setObjectName(u"copyPlayerSearch")
        self.copyPlayerSearch.setGeometry(QRect(260, 10, 81, 23))
        self.playerNameCharLimit = QCheckBox(playerbrowser)
        self.playerNameCharLimit.setObjectName(u"playerNameCharLimit")
        self.playerNameCharLimit.setGeometry(QRect(60, 310, 111, 21))
        self.playerCharLimiter = QSpinBox(playerbrowser)
        self.playerCharLimiter.setObjectName(u"playerCharLimiter")
        self.playerCharLimiter.setGeometry(QRect(10, 310, 41, 21))
        self.playerFilterBox = QPlainTextEdit(playerbrowser)
        self.playerFilterBox.setObjectName(u"playerFilterBox")
        self.playerFilterBox.setGeometry(QRect(10, 260, 231, 31))
        self.playerNameSearchLabel = QLabel(playerbrowser)
        self.playerNameSearchLabel.setObjectName(u"playerNameSearchLabel")
        self.playerNameSearchLabel.setGeometry(QRect(10, 290, 231, 21))
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        self.playerNameSearchLabel.setFont(font)
        self.playerNameSearchLabel.setLayoutDirection(Qt.LeftToRight)
        self.playerNameSearchLabel.setAlignment(Qt.AlignCenter)
        self.playerSearchClose = QPushButton(playerbrowser)
        self.playerSearchClose.setObjectName(u"playerSearchClose")
        self.playerSearchClose.setGeometry(QRect(260, 40, 81, 23))

        self.retranslateUi(playerbrowser)

        QMetaObject.connectSlotsByName(playerbrowser)
    # setupUi

    def retranslateUi(self, playerbrowser):
        playerbrowser.setWindowTitle(QCoreApplication.translate("playerbrowser", u"Player Browser", None))
        self.copyPlayerSearch.setText(QCoreApplication.translate("playerbrowser", u"Copy && Close", None))
        self.playerNameCharLimit.setText(QCoreApplication.translate("playerbrowser", u"Limit characters", None))
        self.playerNameSearchLabel.setText(QCoreApplication.translate("playerbrowser", u"Player Name Filter", None))
        self.playerSearchClose.setText(QCoreApplication.translate("playerbrowser", u"Close", None))
    # retranslateUi

