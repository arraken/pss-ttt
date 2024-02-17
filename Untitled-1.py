class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('pss-ttt.ui', self)
        self.show()

        self.setupConnections()

        self.fleetBrowser = FleetDialogBox()
        self.fleetBrowser.copyFleetSearchClicked.connect(self.handleCopyFleetSearchClicked)

        self.starCalculator = TournamentDialogBox()

        self.initDatabaseConnection()

    def initDatabaseConnection(self):
        for db_name in ["targetsdb", "tournydb", "legendsdb", "pvpdb"]:
            if not QSqlDatabase.database(db_name).isOpen():
                if not QSqlDatabase.database(db_name).open():
                    throwErrorMessage("Database Connection Failure", f"Unable to open {db_name} database")
                    return False
        return True

    def setupConnections(self):
        self.lockUnlockButton.clicked.connect(self.changeButtonText)
        self.searchButton.clicked.connect(self.searchPlayer)
        self.saveNewData.clicked.connect(self.submitNewPlayerData)
        self.resetButton.clicked.connect(self.resetDataFields)
        self.pixyshipLayoutButton.clicked.connect(self.pixyshipURL)
        self.tournamentSubmit.clicked.connect(self.submitTournamentData)
        self.legendsSubmit.clicked.connect(self.submitLegendsData)
        self.pvpSubmit.clicked.connect(self.pvpLegendsData)
        self.importButton.clicked.connect(self.importCSV)
        self.fleetSearchButton.clicked.connect(self.open_fleetBrowser)
        self.delLegendsButton.clicked.connect(self.deleteLegendsLine)
        self.delTournyButton.clicked.connect(self.deleteTournamentLine)
        self.delPVPButton.clicked.connect(self.deletePVPLine)
        self.tournyStarsWindow.clicked.connect(self.open_tournamentStarsCalc)

    def open_fleetBrowser(self):
        self.fleetBrowser.populateFleetList(self.fleetName.toPlainText())
        self.fleetBrowser.exec()

    def open_tournamentStarsCalc(self):
        self.starCalculator.exec()

    def handleCopyFleetSearchClicked(self, selected_text, close_dialog):
        self.resetDataFields()
        self.playerNameSearchBox.insertPlainText(selected_text)
        self.searchPlayer()
        if close_dialog:
            self.fleetBrowser.accept()

    def importCSV(self):
        data_to_insert = []
        with open('fleetsdata.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                specific_data = (row[2], row[1], row[7], row[7], row[5], row[6], " ")
                data_to_insert.append(specific_data)

        if not self.initDatabaseConnection():
            return False

        query = QSqlQuery(QSqlDatabase.database("targetsdb"))
        query.exec("CREATE TABLE IF NOT EXISTS players (playername TEXT PRIMARY KEY, fleetname TEXT NOT NULL, "
                   "laststars TEXT NOT NULL, beststars TEXT NOT NULL, trophies TEXT NOT NULL, maxtrophies TEXT NOT NULL, "
                   "notes TEXT NOT NULL)")

        for specific_data in data_to_insert:
            playername, fleetname, laststars, beststars, trophies, maxtrophies, notes = specific_data

            count_query = QSqlQuery(QSqlDatabase.database("targetsdb"))
            count_query.prepare("SELECT COUNT(*) FROM players WHERE playername = ? AND fleetname = ?")
            count_query.addBindValue(playername)
            count_query.addBindValue(fleetname)
            count_query.exec()
            count_query.next()
            count = count_query.value(0)

            query = QSqlQuery(QSqlDatabase.database("targetsdb"))
            if count > 0:
                query.prepare("UPDATE players SET laststars = ?, beststars = ?, trophies = ?, maxtrophies = ?, notes = ? "
                              "WHERE playername = ? AND fleetname = ?")
            else:
                query.prepare("INSERT INTO players (playername, fleetname, laststars, beststars, trophies, maxtrophies, "
                              "notes) VALUES (?, ?, ?, ?, ?, ?, ?)")

            query.addBindValue(laststars)
            query.addBindValue(beststars)
            query.addBindValue(trophies)
            query.addBindValue(maxtrophies)
            query.addBindValue(notes)
            query.addBindValue(playername)
            query.addBindValue(fleetname)

            if not query.exec_():
                print("Query execution failed:", query.lastError().text())

        QSqlDatabase.database("targetsdb").commit()
        return True