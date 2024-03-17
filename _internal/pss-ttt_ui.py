# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pss-ttt.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QPlainTextEdit, QPushButton, QSizePolicy, QStatusBar,
    QTableView, QTextBrowser, QTextEdit, QToolButton,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(592, 597)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Calibri"])
        MainWindow.setFont(font)
#if QT_CONFIG(statustip)
        MainWindow.setStatusTip(u"")
#endif // QT_CONFIG(statustip)
        MainWindow.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.fleetNameLabel = QLabel(self.centralwidget)
        self.fleetNameLabel.setObjectName(u"fleetNameLabel")
        self.fleetNameLabel.setGeometry(QRect(40, 80, 91, 16))
        font1 = QFont()
        font1.setFamilies([u"Calibri"])
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setItalic(False)
        self.fleetNameLabel.setFont(font1)
        self.fleetNameLabel.setAlignment(Qt.AlignCenter)
        self.bestStars = QTextBrowser(self.centralwidget)
        self.bestStars.setObjectName(u"bestStars")
        self.bestStars.setGeometry(QRect(150, 200, 81, 31))
        self.bestStars.setTabChangesFocus(True)
        self.maxTrophiesLabel = QLabel(self.centralwidget)
        self.maxTrophiesLabel.setObjectName(u"maxTrophiesLabel")
        self.maxTrophiesLabel.setGeometry(QRect(120, 240, 131, 20))
        self.maxTrophiesLabel.setFont(font1)
        self.maxTrophiesLabel.setAlignment(Qt.AlignCenter)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 10, 91, 16))
        self.label.setFont(font1)
        self.tournamentFightsLabel = QLabel(self.centralwidget)
        self.tournamentFightsLabel.setObjectName(u"tournamentFightsLabel")
        self.tournamentFightsLabel.setGeometry(QRect(6, 290, 191, 16))
        self.tournamentFightsLabel.setFont(font1)
        self.tournamentFightsLabel.setAlignment(Qt.AlignCenter)
        self.lastStars = QTextBrowser(self.centralwidget)
        self.lastStars.setObjectName(u"lastStars")
        self.lastStars.setGeometry(QRect(20, 200, 81, 31))
        self.lastStars.setTabChangesFocus(True)
        self.starsLastTournamentLabel = QLabel(self.centralwidget)
        self.starsLastTournamentLabel.setObjectName(u"starsLastTournamentLabel")
        self.starsLastTournamentLabel.setGeometry(QRect(20, 180, 81, 20))
        self.starsLastTournamentLabel.setFont(font1)
        self.starsLastTournamentLabel.setAlignment(Qt.AlignCenter)
        self.playerNotes = QTextEdit(self.centralwidget)
        self.playerNotes.setObjectName(u"playerNotes")
        self.playerNotes.setGeometry(QRect(240, 180, 201, 111))
        self.playerNotes.setTabChangesFocus(True)
        self.maxTrophies = QTextBrowser(self.centralwidget)
        self.maxTrophies.setObjectName(u"maxTrophies")
        self.maxTrophies.setGeometry(QRect(150, 260, 81, 31))
        self.maxTrophies.setTabChangesFocus(True)
        self.searchButton = QPushButton(self.centralwidget)
        self.searchButton.setObjectName(u"searchButton")
        self.searchButton.setGeometry(QRect(190, 10, 111, 31))
        font2 = QFont()
        font2.setFamilies([u"Calibri"])
        font2.setPointSize(9)
        font2.setBold(True)
        self.searchButton.setFont(font2)
        self.bestStarsLabel = QLabel(self.centralwidget)
        self.bestStarsLabel.setObjectName(u"bestStarsLabel")
        self.bestStarsLabel.setGeometry(QRect(150, 180, 81, 20))
        self.bestStarsLabel.setFont(font1)
        self.bestStarsLabel.setAlignment(Qt.AlignCenter)
        self.currentTrophiesLabel = QLabel(self.centralwidget)
        self.currentTrophiesLabel.setObjectName(u"currentTrophiesLabel")
        self.currentTrophiesLabel.setGeometry(QRect(-10, 240, 151, 16))
        self.currentTrophiesLabel.setFont(font1)
        self.currentTrophiesLabel.setAlignment(Qt.AlignCenter)
        self.playerNotesLabel = QLabel(self.centralwidget)
        self.playerNotesLabel.setObjectName(u"playerNotesLabel")
        self.playerNotesLabel.setGeometry(QRect(240, 160, 201, 20))
        font3 = QFont()
        font3.setFamilies([u"Calibri"])
        font3.setPointSize(12)
        font3.setBold(True)
        font3.setItalic(True)
        self.playerNotesLabel.setFont(font3)
        self.playerNotesLabel.setAlignment(Qt.AlignCenter)
        self.playerNameSearchBox = QPlainTextEdit(self.centralwidget)
        self.playerNameSearchBox.setObjectName(u"playerNameSearchBox")
        self.playerNameSearchBox.setGeometry(QRect(10, 30, 181, 31))
        font4 = QFont()
        font4.setFamilies([u"Calibri"])
        font4.setPointSize(12)
        self.playerNameSearchBox.setFont(font4)
        self.playerNameSearchBox.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))
        self.playerNameSearchBox.setFocusPolicy(Qt.StrongFocus)
        self.playerNameSearchBox.setInputMethodHints(Qt.ImhNone)
        self.playerNameSearchBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.playerNameSearchBox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.playerNameSearchBox.setTabChangesFocus(True)
        self.playerNameSearchBox.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.lockUnlockButton = QToolButton(self.centralwidget)
        self.lockUnlockButton.setObjectName(u"lockUnlockButton")
        self.lockUnlockButton.setGeometry(QRect(70, 140, 101, 41))
        self.lockUnlockButton.setFont(font4)
        self.lockUnlockButton.setCheckable(True)
        self.lockUnlockButton.setChecked(True)
        self.currentTrophies = QTextBrowser(self.centralwidget)
        self.currentTrophies.setObjectName(u"currentTrophies")
        self.currentTrophies.setGeometry(QRect(20, 260, 81, 31))
        self.currentTrophies.setTabChangesFocus(True)
        self.legendsFightsLabel = QLabel(self.centralwidget)
        self.legendsFightsLabel.setObjectName(u"legendsFightsLabel")
        self.legendsFightsLabel.setGeometry(QRect(200, 290, 191, 20))
        self.legendsFightsLabel.setFont(font1)
        self.legendsFightsLabel.setAlignment(Qt.AlignCenter)
        self.pvpFightsLabel = QLabel(self.centralwidget)
        self.pvpFightsLabel.setObjectName(u"pvpFightsLabel")
        self.pvpFightsLabel.setGeometry(QRect(390, 290, 191, 20))
        self.pvpFightsLabel.setFont(font1)
        self.pvpFightsLabel.setAlignment(Qt.AlignCenter)
        self.fleetName = QPlainTextEdit(self.centralwidget)
        self.fleetName.setObjectName(u"fleetName")
        self.fleetName.setGeometry(QRect(10, 100, 161, 31))
        self.fleetName.setInputMethodHints(Qt.ImhNone)
        self.fleetName.setMidLineWidth(-5)
        self.fleetName.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.fleetName.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.fleetName.setTabChangesFocus(True)
        self.fleetName.setReadOnly(False)
        self.saveNewData = QPushButton(self.centralwidget)
        self.saveNewData.setObjectName(u"saveNewData")
        self.saveNewData.setGeometry(QRect(450, 250, 111, 31))
        self.saveNewData.setFont(font2)
        self.tournyTable = QTableView(self.centralwidget)
        self.tournyTable.setObjectName(u"tournyTable")
        self.tournyTable.setGeometry(QRect(6, 310, 191, 201))
        self.legendsTable = QTableView(self.centralwidget)
        self.legendsTable.setObjectName(u"legendsTable")
        self.legendsTable.setGeometry(QRect(200, 310, 191, 201))
        self.pvpTable = QTableView(self.centralwidget)
        self.pvpTable.setObjectName(u"pvpTable")
        self.pvpTable.setGeometry(QRect(390, 310, 191, 201))
        self.pvpTable.setAlternatingRowColors(True)
        self.pvpTable.setWordWrap(False)
        self.resetButton = QPushButton(self.centralwidget)
        self.resetButton.setObjectName(u"resetButton")
        self.resetButton.setGeometry(QRect(450, 220, 111, 31))
        self.resetButton.setFont(font2)
        self.pixyshipLayoutButton = QPushButton(self.centralwidget)
        self.pixyshipLayoutButton.setObjectName(u"pixyshipLayoutButton")
        self.pixyshipLayoutButton.setGeometry(QRect(450, 190, 111, 31))
        self.pixyshipLayoutButton.setFont(font2)
        self.importDialogButton = QPushButton(self.centralwidget)
        self.importDialogButton.setObjectName(u"importDialogButton")
        self.importDialogButton.setGeometry(QRect(480, 0, 101, 31))
        self.importDialogButton.setFont(font2)
        self.importDialogButton.setToolTipDuration(10)
        self.fleetSearchButton = QPushButton(self.centralwidget)
        self.fleetSearchButton.setObjectName(u"fleetSearchButton")
        self.fleetSearchButton.setGeometry(QRect(170, 80, 101, 31))
        self.fleetSearchButton.setFont(font2)
        self.delTournyButton = QPushButton(self.centralwidget)
        self.delTournyButton.setObjectName(u"delTournyButton")
        self.delTournyButton.setGeometry(QRect(20, 550, 151, 23))
        self.delLegendsButton = QPushButton(self.centralwidget)
        self.delLegendsButton.setObjectName(u"delLegendsButton")
        self.delLegendsButton.setGeometry(QRect(220, 550, 151, 23))
        self.delPVPButton = QPushButton(self.centralwidget)
        self.delPVPButton.setObjectName(u"delPVPButton")
        self.delPVPButton.setGeometry(QRect(410, 550, 151, 23))
        self.tournyStarsWindow = QPushButton(self.centralwidget)
        self.tournyStarsWindow.setObjectName(u"tournyStarsWindow")
        self.tournyStarsWindow.setGeometry(QRect(480, 90, 101, 31))
        font5 = QFont()
        font5.setPointSize(9)
        font5.setBold(True)
        self.tournyStarsWindow.setFont(font5)
        self.crewTrainerButton = QPushButton(self.centralwidget)
        self.crewTrainerButton.setObjectName(u"crewTrainerButton")
        self.crewTrainerButton.setGeometry(QRect(480, 60, 101, 31))
        self.crewTrainerButton.setFont(font5)
        self.starTargetTrackButton = QPushButton(self.centralwidget)
        self.starTargetTrackButton.setObjectName(u"starTargetTrackButton")
        self.starTargetTrackButton.setGeometry(QRect(480, 120, 101, 31))
        self.starTargetTrackButton.setFont(font5)
        self.playerBrowserSearchButton = QPushButton(self.centralwidget)
        self.playerBrowserSearchButton.setObjectName(u"playerBrowserSearchButton")
        self.playerBrowserSearchButton.setGeometry(QRect(190, 40, 111, 31))
        self.playerBrowserSearchButton.setFont(font2)
        self.submitNewDataButton = QPushButton(self.centralwidget)
        self.submitNewDataButton.setObjectName(u"submitNewDataButton")
        self.submitNewDataButton.setGeometry(QRect(20, 520, 551, 23))
        self.exportFightsButton = QPushButton(self.centralwidget)
        self.exportFightsButton.setObjectName(u"exportFightsButton")
        self.exportFightsButton.setGeometry(QRect(480, 30, 101, 31))
        self.exportFightsButton.setFont(font5)
        self.fleetBrowserSearchButton = QPushButton(self.centralwidget)
        self.fleetBrowserSearchButton.setObjectName(u"fleetBrowserSearchButton")
        self.fleetBrowserSearchButton.setGeometry(QRect(170, 110, 111, 31))
        self.fleetBrowserSearchButton.setFont(font2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.playerNameSearchBox, self.searchButton)
        QWidget.setTabOrder(self.searchButton, self.fleetName)
        QWidget.setTabOrder(self.fleetName, self.fleetSearchButton)
        QWidget.setTabOrder(self.fleetSearchButton, self.lockUnlockButton)
        QWidget.setTabOrder(self.lockUnlockButton, self.lastStars)
        QWidget.setTabOrder(self.lastStars, self.bestStars)
        QWidget.setTabOrder(self.bestStars, self.currentTrophies)
        QWidget.setTabOrder(self.currentTrophies, self.maxTrophies)
        QWidget.setTabOrder(self.maxTrophies, self.playerNotes)
        QWidget.setTabOrder(self.playerNotes, self.saveNewData)
        QWidget.setTabOrder(self.saveNewData, self.resetButton)
        QWidget.setTabOrder(self.resetButton, self.tournyTable)
        QWidget.setTabOrder(self.tournyTable, self.legendsTable)
        QWidget.setTabOrder(self.legendsTable, self.pvpTable)
        QWidget.setTabOrder(self.pvpTable, self.delTournyButton)
        QWidget.setTabOrder(self.delTournyButton, self.delLegendsButton)
        QWidget.setTabOrder(self.delLegendsButton, self.delPVPButton)
        QWidget.setTabOrder(self.delPVPButton, self.pixyshipLayoutButton)
        QWidget.setTabOrder(self.pixyshipLayoutButton, self.importDialogButton)
        QWidget.setTabOrder(self.importDialogButton, self.tournyStarsWindow)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Pixel Starships Target Tracking Tool", None))
        self.fleetNameLabel.setText(QCoreApplication.translate("MainWindow", u"Fleet", None))
        self.maxTrophiesLabel.setText(QCoreApplication.translate("MainWindow", u"Max Trophies", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Player Name", None))
        self.tournamentFightsLabel.setText(QCoreApplication.translate("MainWindow", u"Tournament Fights", None))
        self.starsLastTournamentLabel.setText(QCoreApplication.translate("MainWindow", u"Last Stars", None))
        self.searchButton.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.bestStarsLabel.setText(QCoreApplication.translate("MainWindow", u"Best Stars", None))
        self.currentTrophiesLabel.setText(QCoreApplication.translate("MainWindow", u"Current Trophies", None))
        self.playerNotesLabel.setText(QCoreApplication.translate("MainWindow", u"Notes", None))
        self.lockUnlockButton.setText(QCoreApplication.translate("MainWindow", u"Locked", None))
        self.legendsFightsLabel.setText(QCoreApplication.translate("MainWindow", u"Legends League Fights", None))
        self.pvpFightsLabel.setText(QCoreApplication.translate("MainWindow", u"PvP Fights", None))
        self.saveNewData.setText(QCoreApplication.translate("MainWindow", u"Save Data", None))
        self.resetButton.setText(QCoreApplication.translate("MainWindow", u"Reset Search", None))
        self.pixyshipLayoutButton.setText(QCoreApplication.translate("MainWindow", u"PixyShip Layout", None))
#if QT_CONFIG(tooltip)
        self.importDialogButton.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.importDialogButton.setText(QCoreApplication.translate("MainWindow", u"Import Data", None))
        self.fleetSearchButton.setText(QCoreApplication.translate("MainWindow", u"Fleet Search", None))
        self.delTournyButton.setText(QCoreApplication.translate("MainWindow", u"Delete Tournament Entry", None))
        self.delLegendsButton.setText(QCoreApplication.translate("MainWindow", u"Delete Legends Entry", None))
        self.delPVPButton.setText(QCoreApplication.translate("MainWindow", u"Delete Pvp Entry", None))
        self.tournyStarsWindow.setText(QCoreApplication.translate("MainWindow", u"Tourny Stars Calc", None))
        self.crewTrainerButton.setText(QCoreApplication.translate("MainWindow", u"Crew Trainer", None))
        self.starTargetTrackButton.setText(QCoreApplication.translate("MainWindow", u"Star Target Track", None))
        self.playerBrowserSearchButton.setText(QCoreApplication.translate("MainWindow", u"Search Browser", None))
        self.submitNewDataButton.setText(QCoreApplication.translate("MainWindow", u"Submit Fight Data", None))
        self.exportFightsButton.setText(QCoreApplication.translate("MainWindow", u"Export Fights", None))
        self.fleetBrowserSearchButton.setText(QCoreApplication.translate("MainWindow", u"Search Browser", None))
    # retranslateUi

