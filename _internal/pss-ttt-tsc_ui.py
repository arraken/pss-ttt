# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pss-ttt-tsc.ui'
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

class Ui_TournamentStarCalculator(object):
    def setupUi(self, TournamentStarCalculator):
        if not TournamentStarCalculator.objectName():
            TournamentStarCalculator.setObjectName(u"TournamentStarCalculator")
        TournamentStarCalculator.resize(569, 290)
        self.winsPerDayBox = QPlainTextEdit(TournamentStarCalculator)
        self.winsPerDayBox.setObjectName(u"winsPerDayBox")
        self.winsPerDayBox.setGeometry(QRect(0, 20, 111, 21))
        font = QFont()
        font.setFamilies([u"Arial Black"])
        font.setPointSize(8)
        font.setBold(True)
        self.winsPerDayBox.setFont(font)
        self.winsPerDayBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.winsPerDayBox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.winsPerDayBox.setTabChangesFocus(True)
        self.label = QLabel(TournamentStarCalculator)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 0, 91, 21))
        self.label.setAlignment(Qt.AlignCenter)
        self.myTrophiesBox = QPlainTextEdit(TournamentStarCalculator)
        self.myTrophiesBox.setObjectName(u"myTrophiesBox")
        self.myTrophiesBox.setGeometry(QRect(0, 60, 111, 21))
        font1 = QFont()
        font1.setFamilies([u"Arial Black"])
        font1.setPointSize(7)
        font1.setBold(True)
        self.myTrophiesBox.setFont(font1)
        self.myTrophiesBox.setFocusPolicy(Qt.StrongFocus)
        self.myTrophiesBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.myTrophiesBox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.myTrophiesBox.setTabChangesFocus(True)
        self.label_2 = QLabel(TournamentStarCalculator)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 40, 91, 21))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(TournamentStarCalculator)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 80, 91, 21))
        self.label_3.setAlignment(Qt.AlignCenter)
        self.strengthRatioBox = QPlainTextEdit(TournamentStarCalculator)
        self.strengthRatioBox.setObjectName(u"strengthRatioBox")
        self.strengthRatioBox.setGeometry(QRect(0, 100, 111, 21))
        self.strengthRatioBox.setFont(font1)
        self.strengthRatioBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.strengthRatioBox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.strengthRatioBox.setTabChangesFocus(True)
        self.calculateStars = QPushButton(TournamentStarCalculator)
        self.calculateStars.setObjectName(u"calculateStars")
        self.calculateStars.setGeometry(QRect(0, 130, 111, 23))
        self.starsTableView = QTableView(TournamentStarCalculator)
        self.starsTableView.setObjectName(u"starsTableView")
        self.starsTableView.setGeometry(QRect(110, 10, 441, 271))
        self.starsTableView.setAlternatingRowColors(True)
        self.estCumulStarsLabel = QLabel(TournamentStarCalculator)
        self.estCumulStarsLabel.setObjectName(u"estCumulStarsLabel")
        self.estCumulStarsLabel.setGeometry(QRect(0, 150, 111, 20))
        self.estCumulStarsLabel.setAlignment(Qt.AlignCenter)
        self.estStarsBox = QPlainTextEdit(TournamentStarCalculator)
        self.estStarsBox.setObjectName(u"estStarsBox")
        self.estStarsBox.setGeometry(QRect(20, 170, 71, 31))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.estStarsBox.setFont(font2)
        self.estStarsBox.setTextInteractionFlags(Qt.NoTextInteraction)
        self.actualStarsLabel = QLabel(TournamentStarCalculator)
        self.actualStarsLabel.setObjectName(u"actualStarsLabel")
        self.actualStarsLabel.setGeometry(QRect(0, 200, 111, 20))
        self.actualStarsLabel.setAlignment(Qt.AlignCenter)
        self.actualStarsBox = QPlainTextEdit(TournamentStarCalculator)
        self.actualStarsBox.setObjectName(u"actualStarsBox")
        self.actualStarsBox.setGeometry(QRect(20, 220, 71, 31))
        self.actualStarsBox.setFont(font2)
        self.actualStarsBox.setTextInteractionFlags(Qt.NoTextInteraction)
        self.resetStarsTableButton = QPushButton(TournamentStarCalculator)
        self.resetStarsTableButton.setObjectName(u"resetStarsTableButton")
        self.resetStarsTableButton.setGeometry(QRect(20, 260, 75, 23))
        QWidget.setTabOrder(self.winsPerDayBox, self.myTrophiesBox)
        QWidget.setTabOrder(self.myTrophiesBox, self.strengthRatioBox)
        QWidget.setTabOrder(self.strengthRatioBox, self.calculateStars)
        QWidget.setTabOrder(self.calculateStars, self.starsTableView)
        QWidget.setTabOrder(self.starsTableView, self.estStarsBox)
        QWidget.setTabOrder(self.estStarsBox, self.actualStarsBox)

        self.retranslateUi(TournamentStarCalculator)

        QMetaObject.connectSlotsByName(TournamentStarCalculator)
    # setupUi

    def retranslateUi(self, TournamentStarCalculator):
        TournamentStarCalculator.setWindowTitle(QCoreApplication.translate("TournamentStarCalculator", u"Tournament Star Calculator", None))
        self.winsPerDayBox.setPlaceholderText(QCoreApplication.translate("TournamentStarCalculator", u"Suggested 5", None))
        self.label.setText(QCoreApplication.translate("TournamentStarCalculator", u"Est Wins/Day", None))
        self.myTrophiesBox.setPlaceholderText(QCoreApplication.translate("TournamentStarCalculator", u"Current Trophies", None))
        self.label_2.setText(QCoreApplication.translate("TournamentStarCalculator", u"Trophy Count", None))
        self.label_3.setText(QCoreApplication.translate("TournamentStarCalculator", u"Strength Ratio", None))
        self.strengthRatioBox.setPlaceholderText(QCoreApplication.translate("TournamentStarCalculator", u"Suggested 0.7-0.8", None))
        self.calculateStars.setText(QCoreApplication.translate("TournamentStarCalculator", u"Calculate", None))
        self.estCumulStarsLabel.setText(QCoreApplication.translate("TournamentStarCalculator", u"Est Cumulative Stars", None))
        self.actualStarsLabel.setText(QCoreApplication.translate("TournamentStarCalculator", u"Actual Stars", None))
        self.resetStarsTableButton.setText(QCoreApplication.translate("TournamentStarCalculator", u"Reset Data", None))
    # retranslateUi

