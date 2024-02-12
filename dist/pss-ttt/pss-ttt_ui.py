# Form implementation generated from reading ui file 'c:\Users\Kamguh\Documents\GitHub\pss-ttt\dist\pss-ttt\pss-ttt.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(581, 645)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        MainWindow.setFont(font)
        MainWindow.setStatusTip("")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.fleetNameLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.fleetNameLabel.setGeometry(QtCore.QRect(40, 80, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.fleetNameLabel.setFont(font)
        self.fleetNameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fleetNameLabel.setObjectName("fleetNameLabel")
        self.bestStars = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.bestStars.setGeometry(QtCore.QRect(130, 240, 81, 31))
        self.bestStars.setTabChangesFocus(True)
        self.bestStars.setObjectName("bestStars")
        self.maxTrophiesLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.maxTrophiesLabel.setGeometry(QtCore.QRect(100, 300, 131, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.maxTrophiesLabel.setFont(font)
        self.maxTrophiesLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.maxTrophiesLabel.setObjectName("maxTrophiesLabel")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tournamentFightsLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.tournamentFightsLabel.setGeometry(QtCore.QRect(20, 370, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.tournamentFightsLabel.setFont(font)
        self.tournamentFightsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tournamentFightsLabel.setObjectName("tournamentFightsLabel")
        self.lastStars = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.lastStars.setGeometry(QtCore.QRect(20, 240, 81, 31))
        self.lastStars.setTabChangesFocus(True)
        self.lastStars.setObjectName("lastStars")
        self.pvpSubmit = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pvpSubmit.setGeometry(QtCore.QRect(390, 560, 131, 23))
        self.pvpSubmit.setObjectName("pvpSubmit")
        self.starCount = QtWidgets.QSpinBox(parent=self.centralwidget)
        self.starCount.setGeometry(QtCore.QRect(150, 560, 31, 22))
        self.starCount.setMinimum(-40)
        self.starCount.setMaximum(40)
        self.starCount.setObjectName("starCount")
        self.starsLastTournamentLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.starsLastTournamentLabel.setGeometry(QtCore.QRect(-10, 220, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.starsLastTournamentLabel.setFont(font)
        self.starsLastTournamentLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.starsLastTournamentLabel.setObjectName("starsLastTournamentLabel")
        self.playerNotes = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.playerNotes.setGeometry(QtCore.QRect(240, 200, 311, 161))
        self.playerNotes.setTabChangesFocus(True)
        self.playerNotes.setObjectName("playerNotes")
        self.trophyCount = QtWidgets.QSpinBox(parent=self.centralwidget)
        self.trophyCount.setGeometry(QtCore.QRect(520, 560, 31, 22))
        self.trophyCount.setMinimum(-40)
        self.trophyCount.setMaximum(40)
        self.trophyCount.setObjectName("trophyCount")
        self.maxTrophies = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.maxTrophies.setGeometry(QtCore.QRect(130, 320, 81, 31))
        self.maxTrophies.setTabChangesFocus(True)
        self.maxTrophies.setObjectName("maxTrophies")
        self.searchButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(190, 30, 81, 31))
        self.searchButton.setObjectName("searchButton")
        self.bestStarsLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.bestStarsLabel.setGeometry(QtCore.QRect(100, 220, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.bestStarsLabel.setFont(font)
        self.bestStarsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.bestStarsLabel.setObjectName("bestStarsLabel")
        self.legendsSubmit = QtWidgets.QPushButton(parent=self.centralwidget)
        self.legendsSubmit.setGeometry(QtCore.QRect(210, 560, 131, 23))
        self.legendsSubmit.setObjectName("legendsSubmit")
        self.legendTrophyCount = QtWidgets.QSpinBox(parent=self.centralwidget)
        self.legendTrophyCount.setGeometry(QtCore.QRect(340, 560, 31, 22))
        self.legendTrophyCount.setMinimum(-40)
        self.legendTrophyCount.setMaximum(40)
        self.legendTrophyCount.setObjectName("legendTrophyCount")
        self.currentTrophiesLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.currentTrophiesLabel.setGeometry(QtCore.QRect(-10, 300, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.currentTrophiesLabel.setFont(font)
        self.currentTrophiesLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.currentTrophiesLabel.setObjectName("currentTrophiesLabel")
        self.playerNotesLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.playerNotesLabel.setGeometry(QtCore.QRect(240, 180, 311, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.playerNotesLabel.setFont(font)
        self.playerNotesLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.playerNotesLabel.setObjectName("playerNotesLabel")
        self.playerNameSearchBox = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.playerNameSearchBox.setGeometry(QtCore.QRect(10, 30, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.playerNameSearchBox.setFont(font)
        self.playerNameSearchBox.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.IBeamCursor))
        self.playerNameSearchBox.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.playerNameSearchBox.setTabChangesFocus(True)
        self.playerNameSearchBox.setObjectName("playerNameSearchBox")
        self.lockUnlockButton = QtWidgets.QToolButton(parent=self.centralwidget)
        self.lockUnlockButton.setGeometry(QtCore.QRect(70, 180, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.lockUnlockButton.setFont(font)
        self.lockUnlockButton.setCheckable(True)
        self.lockUnlockButton.setChecked(True)
        self.lockUnlockButton.setObjectName("lockUnlockButton")
        self.tournamentSubmit = QtWidgets.QPushButton(parent=self.centralwidget)
        self.tournamentSubmit.setGeometry(QtCore.QRect(20, 560, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tournamentSubmit.setFont(font)
        self.tournamentSubmit.setObjectName("tournamentSubmit")
        self.currentTrophies = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.currentTrophies.setGeometry(QtCore.QRect(20, 320, 81, 31))
        self.currentTrophies.setTabChangesFocus(True)
        self.currentTrophies.setObjectName("currentTrophies")
        self.legendsFightsLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.legendsFightsLabel.setGeometry(QtCore.QRect(210, 370, 161, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.legendsFightsLabel.setFont(font)
        self.legendsFightsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.legendsFightsLabel.setObjectName("legendsFightsLabel")
        self.pvpFightsLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.pvpFightsLabel.setGeometry(QtCore.QRect(386, 370, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pvpFightsLabel.setFont(font)
        self.pvpFightsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.pvpFightsLabel.setObjectName("pvpFightsLabel")
        self.fleetName = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.fleetName.setGeometry(QtCore.QRect(10, 100, 161, 31))
        self.fleetName.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.fleetName.setTabChangesFocus(True)
        self.fleetName.setReadOnly(False)
        self.fleetName.setObjectName("fleetName")
        self.saveNewData = QtWidgets.QPushButton(parent=self.centralwidget)
        self.saveNewData.setGeometry(QtCore.QRect(440, 60, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.saveNewData.setFont(font)
        self.saveNewData.setObjectName("saveNewData")
        self.tournyTable = QtWidgets.QTableView(parent=self.centralwidget)
        self.tournyTable.setGeometry(QtCore.QRect(20, 390, 161, 161))
        self.tournyTable.setObjectName("tournyTable")
        self.legendsTable = QtWidgets.QTableView(parent=self.centralwidget)
        self.legendsTable.setGeometry(QtCore.QRect(210, 390, 161, 161))
        self.legendsTable.setObjectName("legendsTable")
        self.pvpTable = QtWidgets.QTableView(parent=self.centralwidget)
        self.pvpTable.setGeometry(QtCore.QRect(390, 390, 161, 161))
        self.pvpTable.setAlternatingRowColors(True)
        self.pvpTable.setWordWrap(False)
        self.pvpTable.setObjectName("pvpTable")
        self.resetButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.resetButton.setGeometry(QtCore.QRect(440, 20, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.resetButton.setFont(font)
        self.resetButton.setObjectName("resetButton")
        self.pixyshipLayoutButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pixyshipLayoutButton.setGeometry(QtCore.QRect(270, 30, 101, 31))
        self.pixyshipLayoutButton.setObjectName("pixyshipLayoutButton")
        self.importButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.importButton.setGeometry(QtCore.QRect(450, 140, 75, 23))
        self.importButton.setObjectName("importButton")
        self.fleetSearchButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.fleetSearchButton.setGeometry(QtCore.QRect(170, 100, 81, 31))
        self.fleetSearchButton.setObjectName("fleetSearchButton")
        self.delTournyButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.delTournyButton.setGeometry(QtCore.QRect(24, 590, 151, 23))
        self.delTournyButton.setObjectName("delTournyButton")
        self.delLegendsButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.delLegendsButton.setGeometry(QtCore.QRect(214, 590, 151, 23))
        self.delLegendsButton.setObjectName("delLegendsButton")
        self.delPVPButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.delPVPButton.setGeometry(QtCore.QRect(394, 590, 151, 23))
        self.delPVPButton.setObjectName("delPVPButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.playerNameSearchBox, self.searchButton)
        MainWindow.setTabOrder(self.searchButton, self.lockUnlockButton)
        MainWindow.setTabOrder(self.lockUnlockButton, self.fleetName)
        MainWindow.setTabOrder(self.fleetName, self.lastStars)
        MainWindow.setTabOrder(self.lastStars, self.bestStars)
        MainWindow.setTabOrder(self.bestStars, self.currentTrophies)
        MainWindow.setTabOrder(self.currentTrophies, self.maxTrophies)
        MainWindow.setTabOrder(self.maxTrophies, self.playerNotes)
        MainWindow.setTabOrder(self.playerNotes, self.starCount)
        MainWindow.setTabOrder(self.starCount, self.legendTrophyCount)
        MainWindow.setTabOrder(self.legendTrophyCount, self.trophyCount)
        MainWindow.setTabOrder(self.trophyCount, self.tournamentSubmit)
        MainWindow.setTabOrder(self.tournamentSubmit, self.legendsSubmit)
        MainWindow.setTabOrder(self.legendsSubmit, self.pvpSubmit)
        MainWindow.setTabOrder(self.pvpSubmit, self.tournyTable)
        MainWindow.setTabOrder(self.tournyTable, self.legendsTable)
        MainWindow.setTabOrder(self.legendsTable, self.pvpTable)
        MainWindow.setTabOrder(self.pvpTable, self.saveNewData)
        MainWindow.setTabOrder(self.saveNewData, self.resetButton)
        MainWindow.setTabOrder(self.resetButton, self.pixyshipLayoutButton)
        MainWindow.setTabOrder(self.pixyshipLayoutButton, self.importButton)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pixel Starships Target Tracking Tool"))
        self.fleetNameLabel.setText(_translate("MainWindow", "Fleet"))
        self.maxTrophiesLabel.setText(_translate("MainWindow", "Max Trophies"))
        self.label.setText(_translate("MainWindow", "Player Name"))
        self.tournamentFightsLabel.setText(_translate("MainWindow", "Tournament Fights"))
        self.pvpSubmit.setText(_translate("MainWindow", "Submit PvP Data"))
        self.starsLastTournamentLabel.setText(_translate("MainWindow", "Last Stars"))
        self.searchButton.setText(_translate("MainWindow", "Search"))
        self.bestStarsLabel.setText(_translate("MainWindow", "Best Stars"))
        self.legendsSubmit.setText(_translate("MainWindow", "Submit LLPvP Data"))
        self.currentTrophiesLabel.setText(_translate("MainWindow", "Current Trophies"))
        self.playerNotesLabel.setText(_translate("MainWindow", "Notes"))
        self.lockUnlockButton.setText(_translate("MainWindow", "Locked"))
        self.tournamentSubmit.setText(_translate("MainWindow", "Submit Tournament Data"))
        self.legendsFightsLabel.setText(_translate("MainWindow", "Legends League Fights"))
        self.pvpFightsLabel.setText(_translate("MainWindow", "PvP Fights"))
        self.saveNewData.setText(_translate("MainWindow", "Save New Data"))
        self.resetButton.setText(_translate("MainWindow", "Reset Search"))
        self.pixyshipLayoutButton.setText(_translate("MainWindow", "PixyShip Layout"))
        self.importButton.setText(_translate("MainWindow", "XLS Import"))
        self.fleetSearchButton.setText(_translate("MainWindow", "Fleet Search"))
        self.delTournyButton.setText(_translate("MainWindow", "Delete Tournament Entry"))
        self.delLegendsButton.setText(_translate("MainWindow", "Delete Legends Entry"))
        self.delPVPButton.setText(_translate("MainWindow", "Delete Pvp Entry"))