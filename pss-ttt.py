from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt, QAbstractTableModel, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QListWidgetItem, QTableView, QApplication
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt6.QtGui import QColor
from datetime import date
from openpyxl import load_workbook
from decimal import Decimal
import sys, csv, math, webbrowser, os
'''
To-do
Talk with the worst and see if I can just directly hook into savy API for frequent updates somehow on players?
Add column in fights db for hp remaining
crew training calculator - help my head
consolidate ui files into this script for ease of external download if possible
'''
def create_connection():
      databases = {
            "targetdb": "targets.db",
            "tournydb": "tournyfights.db",
            "legendsdb": "legendfights.db",
            "pvpdb": "pvpfights.db"
      }
      for name, filename in databases.items():
            db = QSqlDatabase.addDatabase('QSQLITE', name)
            db.setDatabaseName(filename)
            if not db.open():
                  throwErrorMessage("Fatal Error", f"{name.capitalize()} DB did not open properly")
                  return False
      return True
def create_table():
      targetsQuery = QSqlQuery(QSqlDatabase.database("targetdb"))
      tournyQuery = QSqlQuery(QSqlDatabase.database("tournydb"))
      legendQuery = QSqlQuery(QSqlDatabase.database("legendsdb"))
      pvpQuery = QSqlQuery(QSqlDatabase.database("pvpdb"))
      targetsQuery.exec("CREATE TABLE IF NOT EXISTS players (playername TEXT PRIMARY KEY, fleetname TEXT NOT NULL, laststars TEXT NOT NULL, beststars TEXT NOT NULL, trophies TEXT NOT NULL, maxtrophies TEXT NOT NULL, notes TEXT NOT NULL)")
      tournyQuery.exec("CREATE TABLE IF NOT EXISTS fights (name TEXT NOT NULL, rewards TEXT NOT NULL, datetag TEXT NOT NULL, UNIQUE(name, rewards, datetag))")
      legendQuery.exec("CREATE TABLE IF NOT EXISTS fights (name TEXT NOT NULL, rewards TEXT NOT NULL, datetag TEXT NOT NULL, UNIQUE(name, rewards, datetag))")
      pvpQuery.exec("CREATE TABLE IF NOT EXISTS fights (name TEXT NOT NULL, rewards TEXT NOT NULL, datetag TEXT NOT NULL, UNIQUE(name, rewards, datetag))")
def write_to_fights_database(data, fights):
      if fights == "tourny":
            query = QSqlQuery(QSqlDatabase.database("tournydb"))
      if fights == "legends":
            query = QSqlQuery(QSqlDatabase.database("legendsdb"))
      if fights == "pvp":
            query = QSqlQuery(QSqlDatabase.database("pvpdb"))
      query.prepare("INSERT OR REPLACE INTO fights(name, rewards, datetag) VALUES(?, ?, ?)")
      for i in range(3):
            query.bindValue(i, data[i].strip())
      if not query.exec():
            throwErrorMessage("FightsDB:", query.lastError().text())
            return False
      return True
def write_to_targets_database(data):
      query = QSqlQuery(QSqlDatabase.database("targetdb"))
      query.prepare("INSERT OR REPLACE INTO players(playername, fleetname, laststars, beststars, trophies, maxtrophies, notes) VALUES(?, ?, ?, ?, ?, ?, ?)")
      for i in range(7):
            query.bindValue(i, data[i])
      if not query.exec():
            throwErrorMessage("targetdb:", query.lastError().text())
            return False
      return True
def throwErrorMessage(text, dump):
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Icon.Critical)
      errortext = "Error: "+text
      msg.setText(errortext)
      msg.setInformativeText(dump)
      msg.setWindowTitle("Error")
      msg.exec()
class FleetDialogBox(QtWidgets.QDialog):
      copyFleetSearchClicked = QtCore.pyqtSignal(str, bool)

      def __init__(self):
            super().__init__()
            uic.loadUi('pss-ttt-fleetbrowser.ui', self)
            self.fleetSearchClose.clicked.connect(self.accept)
            self.copyFleetSearch.clicked.connect(self.onCopyFleetSearchClicked)
            self.fleetFilterBox.textChanged.connect(self.filterFleetList)
            self.charLimiter.valueChanged.connect(self.filterFleetListLength)
            self.charLimiterCheckBox.stateChanged.connect(self.filterFleetListLength)
      def populateFleetList(self, fleet_name):
            self.fleetNameList.clear()
            if not QSqlDatabase.database("targetdb").isOpen():
                  if not QSqlDatabase.database("targetdb").open():
                        throwErrorMessage("Database Connection Failure", "Targets DB did not open properly")
                        return

            query = QSqlQuery(QSqlDatabase.database("targetdb"))
            query.prepare("SELECT playername FROM players WHERE fleetname = :fleet_name")
            query.bindValue(":fleet_name", fleet_name)
            if not query.exec():
                  throwErrorMessage("Query Exection Failure", query.lastError().text())
                  return
            while query.next():
                  player_name = query.value(0)
                  item = QListWidgetItem(player_name)
                  self.fleetNameList.addItem(item)
      def onCopyFleetSearchClicked(self):
            selected_item = self.fleetNameList.currentItem()
            if selected_item:
                  selected_text = selected_item.text()
                  self.copyFleetSearchClicked.emit(selected_text, True)
      def filterFleetList(self):
            filter_text = self.fleetFilterBox.toPlainText().lower()
            for i in range(self.fleetNameList.count()):
                  item = self.fleetNameList.item(i)
                  item_text = item.text().lower()
                  if filter_text in item_text:
                        item.setHidden(False)
                  else:
                        item.setHidden(True)
      def filterFleetListLength(self):
            if self.charLimiterCheckBox.isChecked():
                  length_threshold = self.charLimiter.value()
                  for i in range(self.fleetNameList.count()):
                        item = self.fleetNameList.item(i)
                        item_text = item.text()
                        if len(item_text) == length_threshold:
                              item.setHidden(False)
                        else:
                              item.setHidden(True)
class MainWindow(QtWidgets.QMainWindow):
      def __init__(self):
            super(MainWindow, self).__init__() 
            uic.loadUi('pss-ttt.ui', self) 
            self.show()
            
            self.lockUnlockButton.clicked.connect(self.changeButtonText)
            self.searchButton.clicked.connect(self.searchPlayer)
            self.saveNewData.clicked.connect(self.submitNewPlayerData)
            self.resetButton.clicked.connect(self.resetDataFields)
            self.pixyshipLayoutButton.clicked.connect(self.pixyshipURL)
            self.tournamentSubmit.clicked.connect(self.submitTournamentData)
            self.legendsSubmit.clicked.connect(self.submitLegendsData)
            self.pvpSubmit.clicked.connect(self.submitPVPData)
            self.importDialogButton.clicked.connect(self.open_importDialog)
            self.fleetSearchButton.clicked.connect(self.open_fleetBrowser)
            self.delLegendsButton.clicked.connect(self.deleteLegendsLine)
            self.delTournyButton.clicked.connect(self.deleteTournamentLine)
            self.delPVPButton.clicked.connect(self.deletePVPLine)
            self.tournyStarsWindow.clicked.connect(self.open_tournamentStarsCalc)
            self.crewTrainerButton.clicked.connect(self.open_crewTrainer)
            
            self.fleetBrowser = FleetDialogBox()
            self.fleetBrowser.copyFleetSearchClicked.connect(self.handleCopyFleetSearchClicked)

            self.starCalculator = TournamentDialogBox()

            self.importDialog = ImportDialogBox()

            self.trainingDialog = CrewTrainerDialogBox()

      def open_fleetBrowser(self):
            self.fleetBrowser.populateFleetList(self.fleetName.toPlainText())
            self.fleetBrowser.exec()
      def open_importDialog(self):
            self.importDialog.importDialogLabel.setText("")
            self.importDialog.importFilenameBox.setPlainText("")
            self.importDialog.exec()
      def open_tournamentStarsCalc(self):
            self.starCalculator.exec()
      def open_crewTrainer(self):
            self.trainingDialog.exec()
      def handleCopyFleetSearchClicked(self, selected_text, close_dialog):
            self.resetDataFields()
            self.playerNameSearchBox.insertPlainText(selected_text)
            self.searchPlayer()
            if close_dialog:
                  self.fleetBrowser.accept()
      def pixyshipURL(self):
            searchName = self.playerNameSearchBox.toPlainText()
            if searchName == "":
                  return
            else:
                  webpage = "https://pixyship.com/players?player="+searchName
                  return webbrowser.open(webpage)         
      def resetDataFields(self):
            self.playerNameSearchBox.clear()
            self.fleetName.clear()
            self.lastStars.clear()
            self.bestStars.clear()
            self.currentTrophies.clear()
            self.maxTrophies.clear()
            self.playerNotes.clear()
            model = QSqlTableModel()
            model.clear()
            self.tournyTable.setModel(model)
            self.tournyTable.show()
            self.legendsTable.setModel(model)
            self.legendsTable.show()
            self.pvpTable.setModel(model)
            self.pvpTable.show()
      def searchPlayer(self):
            text = self.playerNameSearchBox.toPlainText().strip()
            if not text:
                  return
            self.resetDataFields()
            self.playerNameSearchBox.setPlainText(text)
            query = QSqlQuery("SELECT * FROM players", QSqlDatabase.database("targetdb"))
            query.prepare("SELECT * FROM players WHERE playername = :text")
            query.bindValue(":text", text)
            if query.exec():
                  if query.next():
                        self.fleetName.setPlainText(query.value(1))
                        self.lastStars.setPlainText(query.value(2))
                        self.bestStars.setPlainText(query.value(3))
                        self.currentTrophies.setPlainText(query.value(4))
                        self.maxTrophies.setPlainText(query.value(5))
                        self.playerNotes.setPlainText(query.value(6))
                        self.updateFightTables("tourny")
                        self.updateFightTables("legends")
                        self.updateFightTables("pvp")
                  else:
                        return
            else:
                  throwErrorMessage("Query execution failed: ", query.lastError().text())
                  return                 
      def changeButtonText(self):
            is_locked = self.lockUnlockButton.text() == "Locked"
            self.lockUnlockButton.setText("Unlocked" if is_locked else "Locked")
            self.playerDataChange(not is_locked)
      def playerDataChange(self, boolean_value):
            self.lastStars.setReadOnly(boolean_value)
            self.bestStars.setReadOnly(boolean_value)
            self.currentTrophies.setReadOnly(boolean_value)
            self.maxTrophies.setReadOnly(boolean_value)
            self.playerNotes.setReadOnly(boolean_value)     
      def submitNewPlayerData(self):
            try:
                  last_stars = int(self.lastStars.toPlainText())
            except ValueError:
                  last_stars = 0
            try:
                  best_stars = int(self.bestStars.toPlainText())
            except ValueError:
                  best_stars = 0
            try:
                  current_trophies = int(self.currentTrophies.toPlainText())
            except ValueError:
                  current_trophies = 0
            try:
                  max_trophies = int(self.maxTrophies.toPlainText())
            except ValueError:
                  max_trophies = 0
            if last_stars > best_stars:
                  best_stars = last_stars
            if current_trophies > max_trophies:
                  max_trophies = current_trophies
            player_data = [self.playerNameSearchBox.toPlainText(), self.fleetName.toPlainText(), last_stars,
                        best_stars, current_trophies, max_trophies, self.playerNotes.toPlainText()]
            if write_to_targets_database(player_data):
                  player_data.clear()
            else:
                  throwErrorMessage("targetdb: Error writing data to the database - Dumping data", player_data)
      def updateFightTables(self, fights):
            name = self.playerNameSearchBox.toPlainText()
            query_error_message = f"{fights.capitalize()}DB Update: "

            if fights in ("tourny", "legends", "pvp"):
                  db_name = f"{fights}db"
                  table_widget = getattr(self, f"{fights}Table")
                  query = QSqlQuery(QSqlDatabase.database(db_name))
                  query.prepare("SELECT rewards, datetag FROM fights WHERE name LIKE ?")
                  if query.lastError().isValid():
                        throwErrorMessage(query_error_message, query.lastError().text())
                        sys.exit(-1)
                  query.addBindValue(f'%{name}%')
                  query.exec()

                  model = QSqlTableModel()
                  model.setQuery(query)
                  table_widget.setModel(model)
                  table_widget.setColumnWidth(0,50)
                  table_widget.show()
            else:
                  throwErrorMessage("Fights Table Error", "Invalid fights type")
      def submitTournamentData(self):
            todaysdate = str(date.today())
            tournament_data = [self.playerNameSearchBox.toPlainText(), str(self.starCount.value()), todaysdate]
            if not write_to_fights_database(tournament_data, "tourny"):
                  throwErrorMessage("FightsDB: Error writing data to the database - Dumping data", tournament_data)
            self.tournyTable.clearSpans()
            self.updateFightTables("tourny")
            tournament_data.clear()
      def submitLegendsData(self):
            todaysdate = str(date.today())
            legends_data = [self.playerNameSearchBox.toPlainText(), str(self.legendTrophyCount.value()), todaysdate]
            if not write_to_fights_database(legends_data, "legends"):
                  throwErrorMessage("FightsDB: Error writing data to the database - Dumping data", legends_data)
            self.tournyTable.clearSpans()
            self.updateFightTables("legends")
            legends_data.clear()
      def submitPVPData(self):
            todaysdate = str(date.today())
            pvp_data = [self.playerNameSearchBox.toPlainText(), str(self.trophyCount.value()), todaysdate]
            if not write_to_fights_database(pvp_data, "pvp"):
                  throwErrorMessage("FightsDB: Error writing data to the database - Dumping data", pvp_data)
            self.tournyTable.clearSpans()
            self.updateFightTables("pvp")
            pvp_data.clear()
      def deleteTournamentLine(self):
            selected_indexes = self.tournyTable.selectionModel().selectedRows()
            db = QSqlDatabase.database("tournydb")
            if not selected_indexes:
                  return
            name_data = []
            rewards_data = []
            datetag_data = []
            for index in selected_indexes:
                  rewards = self.tournyTable.model().index(index.row(), 0).data()
                  datetag = self.tournyTable.model().index(index.row(), 1).data()
                  rewards_data.append(rewards)
                  datetag_data.append(datetag)
            name_data.append(self.playerNameSearchBox.toPlainText())
            
            query = QSqlQuery(db)
            sql_query = "DELETE FROM fights WHERE name IN ({}) AND rewards IN ({}) AND datetag IN ({})".format(
        ", ".join(["'{}'".format(str(name)) for name in name_data]),  
        ", ".join(["'{}'".format(str(data)) for data in rewards_data]),
        ", ".join(["'{}'".format(str(data)) for data in datetag_data]))

            if not query.exec(sql_query):
                  self.throwErrorMessage("Record Deletion Error", query.lastError().text())
                  return
            # Clear the model associated with the QTableView
            self.tournyTable.model().clear()
            # Update the model to reflect changes in the database
            self.updateFightTables("tourny")
      def deleteLegendsLine(self):
            selected_indexes = self.legendsTable.selectionModel().selectedRows()
            db = QSqlDatabase.database("legendsdb")
            if not selected_indexes:
                  return
            name_data = []
            rewards_data = []
            datetag_data = []
            for index in selected_indexes:
                  rewards = self.legendsTable.model().index(index.row(), 0).data()
                  datetag = self.legendsTable.model().index(index.row(), 1).data()
                  rewards_data.append(rewards)
                  datetag_data.append(datetag)
            name_data.append(self.playerNameSearchBox.toPlainText())
            
            query = QSqlQuery(db)
            sql_query = "DELETE FROM fights WHERE name IN ({}) AND rewards IN ({}) AND datetag IN ({})".format(
        ", ".join(["'{}'".format(str(name)) for name in name_data]),  
        ", ".join(["'{}'".format(str(data)) for data in rewards_data]),
        ", ".join(["'{}'".format(str(data)) for data in datetag_data]))

            if not query.exec(sql_query):
                  self.throwErrorMessage("Record Deletion Error: ", query.lastError().text())
                  return
            # Clear the model associated with the QTableView
            self.legendsTable.model().clear()
            # Update the model to reflect changes in the database
            self.updateFightTables("legends")
      def deletePVPLine(self):
            selected_indexes = self.pvpTable.selectionModel().selectedRows()
            db = QSqlDatabase.database("pvpdb")
            if not selected_indexes:
                  return
            name_data = []
            rewards_data = []
            datetag_data = []
            for index in selected_indexes:
                  rewards = self.pvpTable.model().index(index.row(), 0).data()
                  datetag = self.pvpTable.model().index(index.row(), 1).data()
                  rewards_data.append(rewards)
                  datetag_data.append(datetag)
            name_data.append(self.playerNameSearchBox.toPlainText())
            
            query = QSqlQuery(db)
            sql_query = "DELETE FROM fights WHERE name IN ({}) AND rewards IN ({}) AND datetag IN ({})".format(
        ", ".join(["'{}'".format(str(name)) for name in name_data]),  
        ", ".join(["'{}'".format(str(data)) for data in rewards_data]),
        ", ".join(["'{}'".format(str(data)) for data in datetag_data]))
            
            if not query.exec(sql_query):
                  self.throwErrorMessage("Record Deletion Error: ", query.lastError().text())
                  return
            # Clear the model associated with the QTableView
            self.pvpTable.model().clear()
            # Update the model to reflect changes in the database
            self.updateFightTables("pvp")
class ImportDialogBox(QtWidgets.QDialog):
      progress_signal = pyqtSignal(int)
      counter = 0
      max_counter = 0
      def __init__(self):
            super().__init__()
            uic.loadUi('pss-ttt-importdialog.ui', self)
            self.importTargetsButton.clicked.connect(self.import_data)

            self.progress_signal.connect(self.updateProgressBar, QtCore.Qt.ConnectionType.DirectConnection)
      def import_data(self):
            self.importDialogLabel.setText("Data importing has begun.<br>Please note the application make appear to freeze<br>It is not frozen and just processing in the background<br>This will update once finished")
            QApplication.processEvents()
            file_path = self.importFilenameBox.toPlainText().strip()
            
            if not file_path:
                  throwErrorMessage("Import Error", "No file provided or name is incorrect")
                  return
            if file_path.lower().endswith('.csv'):
                  self.max_counter = total_targets_imported = self.importCSV(file_path)
                  file_type = "CSV"
            elif file_path.lower().endswith(('.xls', '.xlsx')):
                  self.max_counter = total_targets_imported = self.importExcel(file_path)
                  file_type = "Excel"
            else:
                  throwErrorMessage("Unsupported file format", "Only able to accept manicured excel formats or csv from Dolores 2.0 bot")
                  return
            self.importDialogLabel.setText(f"Total Targets Import ({file_type}): {total_targets_imported} targets")
            for i in range(self.max_counter):
                  self.progress_signal.emit(self.counter)
      def updateProgressBar(self, value):
            self.importProgressBar.setValue(int((value / self.max_counter) * 100))
      def importExcel(self, file_path):
            workbook = load_workbook(file_path)
            sheet = workbook.active
            if not QSqlDatabase.database("targetdb").open():
                  throwErrorMessage("Targets Database Error", "Unable to open targets database for import")
                  return self.counter
            query = QSqlQuery(QSqlDatabase.database("targetdb"))
            query.exec(f"CREATE TABLE IF NOT EXISTS players (playername TEXT, fleetname TEXT, laststars INT, beststars INT, trophies INT, maxtrophies INT, notes TEXT)")

            for row in sheet.iter_rows(min_row=2, values_only=True):  # Start from the second row assuming the first row is header
                  playername, fleetname, laststars, beststars, trophies, maxtrophies, notes = row
                  query.prepare(f"INSERT OR REPLACE INTO players (playername, fleetname, laststars, beststars, trophies, maxtrophies, notes) "
                      "VALUES (?, ?, ?, ?, ?, ?, ?)")
                  query.addBindValue(playername)
                  query.addBindValue(fleetname)
                  query.addBindValue(laststars)
                  query.addBindValue(beststars)
                  query.addBindValue(trophies)
                  query.addBindValue(maxtrophies)
                  query.addBindValue(notes)
                  if query.exec():
                        self.counter += 1
                        self.progress_signal.emit(self.counter)
                  else:
                        throwErrorMessage("Targets Database Insertion Error:", query.lastError().text())
            
            QSqlDatabase.database("targetdb").close()
            return self.counter
      def importCSV(self, file_path):
            data_to_insert = []
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                  reader = csv.reader(csvfile, delimiter=';')
                  for row in reader:
                        specific_data = (row[2], row[1], row[7], row[7], row[5], row[6], " ")
                        data_to_insert.append(specific_data)
    
            db = QSqlDatabase.database("targetdb")
            if not db.open():
                  throwErrorMessage("Targets Database Error", "Unable to open targets database for import")
                  return self.counter
    
            query = QSqlQuery(db)
            query.exec("CREATE TABLE IF NOT EXISTS players (playername TEXT PRIMARY KEY, fleetname TEXT NOT NULL, laststars TEXT NOT NULL, beststars TEXT NOT NULL, trophies TEXT NOT NULL, maxtrophies TEXT NOT NULL, notes TEXT NOT NULL)")
    
            self.max_counter = len(data_to_insert)
            for specific_data in data_to_insert:
                  playername, fleetname, laststars, beststars, trophies, maxtrophies, notes = specific_data
                  count_query = QSqlQuery(db)
                  count_query.prepare("SELECT COUNT(*) FROM players WHERE playername = ? AND fleetname = ?")
                  count_query.addBindValue(playername)
                  count_query.addBindValue(fleetname)
                  count_query.exec()
                  count_query.next()
                  count = count_query.value(0)
                  
                  query.prepare("INSERT OR REPLACE INTO players (playername, fleetname, laststars, beststars, trophies, maxtrophies, notes) VALUES (?, ?, ?, ?, ?, ?, ?)")
                  query.addBindValue(playername)
                  query.addBindValue(fleetname)
                  query.addBindValue(laststars)
                  query.addBindValue(beststars)
                  query.addBindValue(trophies)
                  query.addBindValue(maxtrophies)
                  query.addBindValue(notes)
        
                  if query.exec():
                        self.counter += 1
                        self.progress_signal.emit(self.counter)
                  else:
                        throwErrorMessage("Database Error", query.lastError().text())
            db.commit()
            return self.counter
class TournamentDialogBox(QtWidgets.QDialog):
      def __init__(self):
            super().__init__()
            uic.loadUi('pss-ttt-tsc.ui', self)
            
            self.starTableHeaders = ['Star Goal', 'Fight 1', 'Fight 2', 'Fight 3', 'Fight 4', 'Fight 5', 'Fight 6']
            self.starsTable = [
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],]
            self.loadStarsTableFromCSV("starstable.csv")
            self.tournamentTable = self.findChild(QTableView, "starsTableView")
            self.model = self.TournamentTableModel(self.starsTable, self)
            self.tournamentTable.setModel(self.model)
            for i in range(7):
                  self.tournamentTable.setColumnWidth(i,50)
            self.calculateStars.clicked.connect(self.calculateStarsGoal)     
            self.resetStarsTableButton.clicked.connect(self.resetStarsTable)
      def updateActualStarsBox(self):
            total_sum = sum(self.model.getCellValue(7, col) for col in range(self.model.columnCount(None)))
            self.actualStarsBox.setPlainText(str(total_sum))
            self.saveStarsTableToCSV("starstable.csv")
      def saveStarsTableToCSV(self, filename):
            with open(filename, 'w', newline='') as csvfile:
                  writer = csv.writer(csvfile)
                  writer.writerows(self.starsTable)
      def loadStarsTableFromCSV(self, filename):
            if os.path.exists(filename):
                  with open(filename, newline='') as csvfile:
                        reader = csv.reader(csvfile)
                        self.starsTable = [list(map(int, row)) for row in reader]
            else:
                  self.starsTable = [
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],]
                  self.saveStarsTableToCSV(filename)
      def resetStarsTable(self):
            self.starsTable = [
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],]
            self.saveStarsTableToCSV("starstable.csv")
            self.model = self.TournamentTableModel(self.starsTable, self)
            self.tournamentTable.setModel(self.model)
      class starsErrorDialog(QtWidgets.QDialog):
            def __init__(self):
                  super().__init__()
            def checkStarsErrors(self):
                  winsPerDay = self.winsPerDayBox.toPlainText().strip()
                  myTrophies = self.myTrophiesBox.toPlainText().strip()
                  strengthRatio = self.strengthRatioBox.toPlainText().strip()

                  if not winsPerDay or not myTrophies or not strengthRatio:
                        error_message = QMessageBox()
                        error_message.setIcon(QMessageBox.Icon.Warning)
                        error_message.setText("Error: Please fill out all 3 boxes for star calculations.")
                        error_message.setWindowTitle("Missing Information")
                        error_message.exec()
                        return False
                  else:
                        return True
      class TournamentTableModel(QAbstractTableModel):
            def __init__(self, data, parent=None):
                  super().__init__()
                  self._data = data
                  self.parent = parent
                  self.verticalHeaders = ['Star Goal', 'Fight 1', 'Fight 2', 'Fight 3', 'Fight 4', 'Fight 5', 'Fight 6', 'Stars Gained']
                  self.horizontalHeaders = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
            def rowCount(self, index):
                  return len(self._data)
            def columnCount(self, index):
                  return len(self._data[0])
            def data(self, index, role=Qt.ItemDataRole.DisplayRole):
                  if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
                        return str(self._data[index.row()][index.column()])
            def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
                  if role == Qt.ItemDataRole.EditRole and index.isValid():
                        self._data[index.row()][index.column()] = value
                        self.dataChanged.emit(index, index)
                        for col in range(self.columnCount(None)):
                                    self._data[7][col] = sum(int(self._data[i][col]) for i in range(1,7))
                        self.parent.updateActualStarsBox()
                        return True
                  return False
            def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
                  if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
                        return self.horizontalHeaders[section]
                  if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Vertical:
                        return self.verticalHeaders[section]
            def getCellValue(self, row, column):
                  return self._data[row][column]
            def flags(self, index):
                  if index.row() == 0 or index.row() == 7:
                        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
                  else:
                        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
      def calculateStarsGoal(self):
            if not self.starsErrorDialog.checkStarsErrors(self):
                  return
                        
            start_value = Decimal(0)
            winsPerDay = Decimal(self.winsPerDayBox.toPlainText())
            myTrophies = Decimal(self.myTrophiesBox.toPlainText())
            strengthRatio = Decimal(self.strengthRatioBox.toPlainText())
            end_value = Decimal(0)
            todaysStarsTarget = Decimal(0)
            for i in range(7):
                  start_value = end_value
                  trophyStarsTarget = math.floor((myTrophies*strengthRatio)/1000)
                  starsStarsTarget = math.floor(Decimal(start_value*Decimal(".15")*strengthRatio))
                  if trophyStarsTarget > starsStarsTarget:
                        todaysStarsTarget = trophyStarsTarget
                  else:
                        todaysStarsTarget = starsStarsTarget
                  end_value = todaysStarsTarget*winsPerDay+start_value
                  index = self.model.index(0,i)
                  self.model.setData(index, todaysStarsTarget)
                  self.estStarsBox.clear()
                  if i == 6:
                        self.estStarsBox.insertPlainText(str(end_value))
            self.tournamentTable.show()
            self.saveStarsTableToCSV("starstable.csv")
class CrewTrainerDialogBox(QtWidgets.QDialog):
      def __init__(self):
            super().__init__()
            uic.loadUi('pss-ttt-crewtrainer.ui', self)

            self.trainingList = [
                  ("ABL Green", "Steam Yoga", [0,0,4,1,0,0,0,0,0]),
                  ("ABL Blue", "Crew vs Wild", [1,1,8,1,0,0,0,0,0]),
                  ("ABL Gold", "Space Marine", [1,1,12,2,0,0,0,0,0]),
                  ("ABL Common", "Paracetamol", [1,0,2,1,0,1,0,0,0]),
                  ("ABL Elite", "Paracetamol Rapid", [2,0,4,1,0,2,0,0,0]),
                  ("ABL Unique", "Ibuprofen", [3,0,8,3,0,3,0,0,1]),
                  ("ABL Epic", "Ibuprofen Rapid", [5,0,16,3,0,5,0,0,2]),
                  ("ABL Hero", "Ginkgo", [12,0,24,4,0,12,0,0,3]),
                  ("ABL Special", "Brain Enhancer", [8,0,48,3,0,8,0,0,2]),
                  ("ABL Legendary", "Super Brain Enhancer", [3,0,96,1,0,3,0,0,1]),
                  ("ATK Green", "Kickbox", [0,4,0,1,0,0,0,0,0]),
                  ("ATK Blue", "BJJ", [1,8,1,1,0,0,0,0,0]),
                  ("ATK Gold", "Shaolin Tradition", [1,12,1,2,0,0,0,0,0]),
                  ("ATK Common", "Chicken Skewer", [0,2,1,1,0,0,0,0,1]),
                  ("ATK Elite", "Yakitori", [0,4,2,1,0,0,0,0,2]),
                  ("ATK Unique", "Double Yakitori", [1,8,3,3,0,0,0,0,3]),
                  ("ATK Epic", "Shish Kebabs", [2,16,5,3,0,0,0,0,5]),
                  ("ATK Hero", "Drumsticks", [3,24,12,4,0,0,0,0,12]),
                  ("ATK Special", "Steak", [2,48,8,3,0,0,0,0,8]),
                  ("ATK Legendary", "Roast Turkey", [1,96,3,1,0,0,0,0,3]),
                  ("ENG Green", "Study Expert Engineering Manual", [0,0,0,0,1,0,0,4,0]),
                  ("ENG Blue", "Engineering Summit", [0,0,0,0,1,1,1,8,0]),
                  ("ENG Gold", "Engineering PhD", [0,0,0,0,2,0,0,12,1]),
                  ("ENG Common", "Standard Engineering Tool Kit", [0,0,0,1,1,0,1,2,0]),
                  ("ENG Elite", "Obsolete Engineering Tool Kit", [0,0,0,1,2,0,2,4,0]),
                  ("ENG Unique", "Starter Engineering Tool Kit", [0,0,0,3,3,1,3,8,0]),
                  ("ENG Epic", "Advanced Engineering Tool Kit", [0,0,0,3,5,2,5,16,0]),
                  ("ENG Hero", "Rare Engineering Tool Kit", [0,0,0,4,12,3,12,24,0]),
                  ("ENG Special", "Prototype Engineering Tool Kit", [0,0,0,3,8,2,8,48,0]),
                  ("ENG Legendary", "Alien Engineering Tool Kit", [0,0,0,1,3,1,3,96,0]),
                  ("HP Green", "Bench Press", [4,0,0,1,0,0,0,0,0]),
                  ("HP Blue", "Muscle Beach", [8,1,1,1,0,0,0,0,0]),
                  ("HP Gold", "Olympic Weightlifting", [12,1,1,2,0,0,0,0,0]),
                  ("HP Common", "Small Protein Shake", [2,1,0,1,0,0,0,1,0]),
                  ("HP Elite", "Regular Protein Shake", [4,2,0,1,0,0,0,2,0]),
                  ("HP Unique", "Large Protein Shake", [8,3,1,3,0,0,0,3,0]),
                  ("HP Epic", "Super Protein Shake", [16,5,2,3,0,0,0,5,0]),
                  ("HP Hero", "HGH", [24,12,3,4,0,0,0,12,0]),
                  ("HP Special", "Enhanced HGH", [48,8,2,3,0,0,0,8,0]),
                  ("HP Legendary", "Prototype HGH", [96,3,1,1,0,0,0,3,0]),
                  ("PLT Green", "Read Expert Pilot Handbook", [0,0,0,0,0,4,0,0,1]),
                  ("PLT Blue", "Pilot Summit", [0,0,0,0,1,8,0,1,1]),
                  ("PLT Gold", "Pilot Expert", [0,0,0,0,1,12,0,0,2]),
                  ("PLT Common", "Street Map", [0,0,0,1,0,2,0,1,1]),
                  ("PLT Elite", "Travel Map", [0,0,0,1,0,4,0,2,2]),
                  ("PLT Unique", "World Map", [0,1,0,3,0,8,0,3,3]),
                  ("PLT Epic", "Global Map", [0,2,0,3,0,16,0,5,5]),
                  ("PLT Hero", "System Map", [0,3,0,4,0,24,0,12,12]),
                  ("PLT Special", "Star Map", [0,2,0,3,0,48,0,8,8]),
                  ("PLT Legendary", "Galactic Navigation Map", [0,1,0,1,0,96,0,3,3]),
                  ("RPR Common", "Repair Guide", [0,0,0,1,2,0,1,1,0]),
                  ("RPR Elite", "New Repair Guide", [0,0,0,1,4,0,2,2,0]),
                  ("RPR Unique", "Advanced Repair Guide", [0,0,1,3,8,0,3,3,0]),
                  ("RPR Epic", "Epic Repair Guide", [0,0,2,3,16,0,5,5,0]),
                  ("RPR Hero", "Lost Repair Guide", [0,0,3,4,24,0,12,12,0]),
                  ("RPR Special", "Special Repair Guide", [0,0,2,3,48,0,8,8,0]),
                  ("RPR Legendary", "Legendary Repair Guide", [0,0,1,1,96,0,3,3,0]),
                  ("SCI Green", "Big Book of Science", [0,0,0,0,0,0,4,1,0]),
                  ("SCI Blue", "Scientific Summit", [0,0,0,0,1,0,8,1,1]),
                  ("SCI Gold", "Science PhD", [0,0,0,0,0,0,12,2,1]),
                  ("SCI Common", "Drop of Brain Juice", [0,0,1,1,1,0,2,0,0]),
                  ("SCI Elite", "Sliver of Brain Juice", [0,0,2,1,2,0,4,0,0]),
                  ("SCI Unique", "Brew of Brain Juice", [0,0,3,3,3,0,8,0,1]),
                  ("SCI Epic", "Tincture of Brain Juice", [0,0,5,3,5,0,16,0,2]),
                  ("SCI Hero", "Solution of Brain Juice", [0,0,12,4,12,0,24,0,3]),
                  ("SCI Special", "Concentrate of Brain Juice", [0,0,8,3,8,0,48,0,2]),
                  ("SCI Legendary", "Elixir of Brain Juice", [0,0,3,1,3,0,96,0,1]),
                  ("STA Green", "Weighted Run", [0,0,0,5,0,0,0,0,0]),
                  ("STA Blue", "Hardcore Aerobics", [2,2,2,8,0,0,0,0,0]),
                  ("STA Gold", "Everest Climb", [3,3,3,16,0,0,0,0,0]),
                  ("STA Common", "Small Cola", [1,1,1,2,1,1,1,1,1]),
                  ("STA Elite", "Large Cola", [1,1,1,4,1,1,1,1,1]),
                  ("STA Unique", "Mountain Brew", [2,2,2,8,2,2,2,2,2]),
                  ("STA Epic", "Pink Cow", [3,3,3,16,3,3,3,3,3]),
                  ("STA Hero", "Large Pink Cow", [4,4,4,24,4,4,4,4,4]),
                  ("STA Special", "U", [3,3,3,48,3,3,3,3,3]),
                  ("STA Legendary", "Father", [2,2,2,96,2,2,2,2,2]),
                  ("WPN Green", "Read Expert Weapon Theory", [0,0,0,0,0,0,1,0,4]),
                  ("WPN Blue", "Weapons Summit", [0,0,0,0,1,1,1,0,8]),
                  ("WPN Gold", "Weapons PhD", [0,0,0,0,2,0,0,1,12]),
                  ("WPN Common", "Military Recruit Handbook", [0,1,0,1,0,1,0,0,2]),
                  ("WPN Elite", "Standard Combat Manual", [0,2,0,1,0,2,0,0,4]),
                  ("WPN Unique", "Galetrooper Training Manual", [0,3,0,3,0,3,1,0,8]),
                  ("WPN Epic", "Elite Combat Manual", [0,5,0,3,0,5,2,0,16]),
                  ("WPN Hero", "Veteran's Guidebook", [0,12,0,4,0,12,3,0,24]),
                  ("WPN Special", "How To Shoot Your Shot'", [0,8,0,3,0,8,2,0,48]),
                  ("WPN Legendary", "Sharpshooter's Cheatbook", [0,3,0,1,0,3,1,0,96]),
            ]
            self.baseTrainingList = [
                  ("ABL Green", "Steam Yoga", [0,0,4,1,0,0,0,0,0]),
                  ("ABL Blue", "Crew vs Wild", [1,1,8,1,0,0,0,0,0]),
                  ("ABL Gold", "Space Marine", [1,1,12,2,0,0,0,0,0]),
                  ("ABL Common", "Paracetamol", [1,0,2,1,0,1,0,0,0]),
                  ("ABL Elite", "Paracetamol Rapid", [2,0,4,1,0,2,0,0,0]),
                  ("ABL Unique", "Ibuprofen", [3,0,8,3,0,3,0,0,1]),
                  ("ABL Epic", "Ibuprofen Rapid", [5,0,16,3,0,5,0,0,2]),
                  ("ABL Hero", "Ginkgo", [12,0,24,4,0,12,0,0,3]),
                  ("ABL Special", "Brain Enhancer", [8,0,48,3,0,8,0,0,2]),
                  ("ABL Legendary", "Super Brain Enhancer", [3,0,96,1,0,3,0,0,1]),
                  ("ATK Green", "Kickbox", [0,4,0,1,0,0,0,0,0]),
                  ("ATK Blue", "BJJ", [1,8,1,1,0,0,0,0,0]),
                  ("ATK Gold", "Shaolin Tradition", [1,12,1,2,0,0,0,0,0]),
                  ("ATK Common", "Chicken Skewer", [0,2,1,1,0,0,0,0,1]),
                  ("ATK Elite", "Yakitori", [0,4,2,1,0,0,0,0,2]),
                  ("ATK Unique", "Double Yakitori", [1,8,3,3,0,0,0,0,3]),
                  ("ATK Epic", "Shish Kebabs", [2,16,5,3,0,0,0,0,5]),
                  ("ATK Hero", "Drumsticks", [3,24,12,4,0,0,0,0,12]),
                  ("ATK Special", "Steak", [2,48,8,3,0,0,0,0,8]),
                  ("ATK Legendary", "Roast Turkey", [1,96,3,1,0,0,0,0,3]),
                  ("ENG Green", "Study Expert Engineering Manual", [0,0,0,0,1,0,0,4,0]),
                  ("ENG Blue", "Engineering Summit", [0,0,0,0,1,1,1,8,0]),
                  ("ENG Gold", "Engineering PhD", [0,0,0,0,2,0,0,12,1]),
                  ("ENG Common", "Standard Engineering Tool Kit", [0,0,0,1,1,0,1,2,0]),
                  ("ENG Elite", "Obsolete Engineering Tool Kit", [0,0,0,1,2,0,2,4,0]),
                  ("ENG Unique", "Starter Engineering Tool Kit", [0,0,0,3,3,1,3,8,0]),
                  ("ENG Epic", "Advanced Engineering Tool Kit", [0,0,0,3,5,2,5,16,0]),
                  ("ENG Hero", "Rare Engineering Tool Kit", [0,0,0,4,12,3,12,24,0]),
                  ("ENG Special", "Prototype Engineering Tool Kit", [0,0,0,3,8,2,8,48,0]),
                  ("ENG Legendary", "Alien Engineering Tool Kit", [0,0,0,1,3,1,3,96,0]),
                  ("HP Green", "Bench Press", [4,0,0,1,0,0,0,0,0]),
                  ("HP Blue", "Muscle Beach", [8,1,1,1,0,0,0,0,0]),
                  ("HP Gold", "Olympic Weightlifting", [12,1,1,2,0,0,0,0,0]),
                  ("HP Common", "Small Protein Shake", [2,1,0,1,0,0,0,1,0]),
                  ("HP Elite", "Regular Protein Shake", [4,2,0,1,0,0,0,2,0]),
                  ("HP Unique", "Large Protein Shake", [8,3,1,3,0,0,0,3,0]),
                  ("HP Epic", "Super Protein Shake", [16,5,2,3,0,0,0,5,0]),
                  ("HP Hero", "HGH", [24,12,3,4,0,0,0,12,0]),
                  ("HP Special", "Enhanced HGH", [48,8,2,3,0,0,0,8,0]),
                  ("HP Legendary", "Prototype HGH", [96,3,1,1,0,0,0,3,0]),
                  ("PLT Green", "Read Expert Pilot Handbook", [0,0,0,0,0,4,0,0,1]),
                  ("PLT Blue", "Pilot Summit", [0,0,0,0,1,8,0,1,1]),
                  ("PLT Gold", "Pilot Expert", [0,0,0,0,1,12,0,0,2]),
                  ("PLT Common", "Street Map", [0,0,0,1,0,2,0,1,1]),
                  ("PLT Elite", "Travel Map", [0,0,0,1,0,4,0,2,2]),
                  ("PLT Unique", "World Map", [0,1,0,3,0,8,0,3,3]),
                  ("PLT Epic", "Global Map", [0,2,0,3,0,16,0,5,5]),
                  ("PLT Hero", "System Map", [0,3,0,4,0,24,0,12,12]),
                  ("PLT Special", "Star Map", [0,2,0,3,0,48,0,8,8]),
                  ("PLT Legendary", "Galactic Navigation Map", [0,1,0,1,0,96,0,3,3]),
                  ("RPR Common", "Repair Guide", [0,0,0,1,2,0,1,1,0]),
                  ("RPR Elite", "New Repair Guide", [0,0,0,1,4,0,2,2,0]),
                  ("RPR Unique", "Advanced Repair Guide", [0,0,1,3,8,0,3,3,0]),
                  ("RPR Epic", "Epic Repair Guide", [0,0,2,3,16,0,5,5,0]),
                  ("RPR Hero", "Lost Repair Guide", [0,0,3,4,24,0,12,12,0]),
                  ("RPR Special", "Special Repair Guide", [0,0,2,3,48,0,8,8,0]),
                  ("RPR Legendary", "Legendary Repair Guide", [0,0,1,1,96,0,3,3,0]),
                  ("SCI Green", "Big Book of Science", [0,0,0,0,0,0,4,1,0]),
                  ("SCI Blue", "Scientific Summit", [0,0,0,0,1,0,8,1,1]),
                  ("SCI Gold", "Science PhD", [0,0,0,0,0,0,12,2,1]),
                  ("SCI Common", "Drop of Brain Juice", [0,0,1,1,1,0,2,0,0]),
                  ("SCI Elite", "Sliver of Brain Juice", [0,0,2,1,2,0,4,0,0]),
                  ("SCI Unique", "Brew of Brain Juice", [0,0,3,3,3,0,8,0,1]),
                  ("SCI Epic", "Tincture of Brain Juice", [0,0,5,3,5,0,16,0,2]),
                  ("SCI Hero", "Solution of Brain Juice", [0,0,12,4,12,0,24,0,3]),
                  ("SCI Special", "Concentrate of Brain Juice", [0,0,8,3,8,0,48,0,2]),
                  ("SCI Legendary", "Elixir of Brain Juice", [0,0,3,1,3,0,96,0,1]),
                  ("STA Green", "Weighted Run", [0,0,0,5,0,0,0,0,0]),
                  ("STA Blue", "Hardcore Aerobics", [2,2,2,8,0,0,0,0,0]),
                  ("STA Gold", "Everest Climb", [3,3,3,16,0,0,0,0,0]),
                  ("STA Common", "Small Cola", [1,1,1,2,1,1,1,1,1]),
                  ("STA Elite", "Large Cola", [1,1,1,4,1,1,1,1,1]),
                  ("STA Unique", "Mountain Brew", [2,2,2,8,2,2,2,2,2]),
                  ("STA Epic", "Pink Cow", [3,3,3,16,3,3,3,3,3]),
                  ("STA Hero", "Large Pink Cow", [4,4,4,24,4,4,4,4,4]),
                  ("STA Special", "U", [3,3,3,48,3,3,3,3,3]),
                  ("STA Legendary", "Father", [2,2,2,96,2,2,2,2,2]),
                  ("WPN Green", "Read Expert Weapon Theory", [0,0,0,0,0,0,1,0,4]),
                  ("WPN Blue", "Weapons Summit", [0,0,0,0,1,1,1,0,8]),
                  ("WPN Gold", "Weapons PhD", [0,0,0,0,2,0,0,1,12]),
                  ("WPN Common", "Military Recruit Handbook", [0,1,0,1,0,1,0,0,2]),
                  ("WPN Elite", "Standard Combat Manual", [0,2,0,1,0,2,0,0,4]),
                  ("WPN Unique", "Galetrooper Training Manual", [0,3,0,3,0,3,1,0,8]),
                  ("WPN Epic", "Elite Combat Manual", [0,5,0,3,0,5,2,0,16]),
                  ("WPN Hero", "Veteran's Guidebook", [0,12,0,4,0,12,3,0,24]),
                  ("WPN Special", "How To Shoot Your Shot'", [0,8,0,3,0,8,2,0,48]),
                  ("WPN Legendary", "Sharpshooter's Cheatbook", [0,3,0,1,0,3,1,0,96]),
            ]
            self.trainingChart = [
                  (" ", " ", [0,0,0,0,0,0,0,0,0]),
                  (" ", " ", [0,0,0,0,0,0,0,0,0]),
                  (" ", " ", [0,0,0,0,0,0,0,0,0]),
                  (" ", " ", [0,0,0,0,0,0,0,0,0]),
                  (" ", " ", [0,0,0,0,0,0,0,0,0]),
                  (" ", " ", [0,0,0,0,0,0,0,0,0]),
                  (" ", " ", [0,0,0,0,0,0,0,0,0]),
                  (" ", " ", [0,0,0,0,0,0,0,0,0]),
                  (" ", " ", [0,0,0,0,0,0,0,0,0]),
                  (" ", " ", [0,0,0,0,0,0,0,0,0])
            ]
            self.crewStats = [[0, 0] for _ in range(9)]
            self.trainingStats = [[0] for _ in range(9)]
            self.itemTrainingStats = [[0] for _ in range(9)]

            self.statsTable = self.findChild(QTableView, "crewStatTable")
            self.model = self.StatsTableModel(self.crewStats, self)
            self.trainingTable = self.findChild(QTableView, "trainingListValuesTable")
            self.trainingmodel = self.TrainingListTableModel(self.itemTrainingStats, self)
            self.chartTable = self.findChild(QTableView, "trainingChartTable")
            self.chartModel = self.TrainingChartTableModel(self.trainingChart, self.trainingStatBox)
            self.trainignStatBox = self.findChild(QtWidgets.QComboBox, "trainingStatBox")
            self.statsTable.setModel(self.model)
            self.statsTable.setColumnWidth(0,50)
            self.statsTable.setColumnWidth(1,90)
            self.statsTable.setColumnWidth(2,90)
            self.trainingTable.setModel(self.trainingmodel)
            self.trainingTable.setColumnWidth(0,50)
            self.trainingTable.setColumnWidth(1,50)
            self.chartTable.setModel(self.chartModel)
            self.trainingPointsBox.currentIndexChanged.connect(self.onComboBoxValueChanged)
            self.trainingStatBox.currentIndexChanged.connect(self.onComboBoxValueChanged)
            self.trainingLevelBox.currentIndexChanged.connect(self.onComboBoxValueChanged)
            self.fatigueBox.currentIndexChanged.connect(self.onComboBoxValueChanged)

            for i in range(9):
                  if i == 1:
                        self.trainingTable.setRowHeight(i,1)
                  else:
                        self.trainingTable.setRowHeight(i,10)
            for i in range(10):
                  if i == 0:
                        self.chartTable.setColumnWidth(i,125)
                  else:
                        self.chartTable.setColumnWidth(i,1)
            self.testPushButton.clicked.connect(self.wipeCrewStats)
            self.onComboBoxValueChanged()
      def calculateTrainingChart(self): #Builds training chart for the selected
            selected_item = self.trainingStatBox.currentText()
            selected_key = selected_item[:3]
            selected_data_list = []

            for item in self.trainingList:
                  key, name, data = item[0], item[1], item[2]
                  if key.startswith(selected_key):
                        selected_data_list.append((name, data))
            self.model = self.TrainingChartTableModel(selected_data_list, self.trainingStatBox)
            self.chartTable.setModel(self.model)
            return
      def updateFatigueMod(self): #Calculates training modifer based on fatigue
            max_training_points = int(self.trainingPointsBox.currentText())
            total_tp = sum(int(self.crewStats[i][0]) for i in range (9))
            fatigue = self.fatigueBox.currentText()
            fatigue_m = {
                  '0': 1,
                  '1-50': 0.5,
                  '51-99': 0.3,
                  '100': 0
            }
            fatigue_m = fatigue_m.get(fatigue, 1)
            crew_stats_m = {}
            for i, (stat_name, _) in enumerate([('hp', 1), ('atk', 1), ('abl', 1), ('sta', 1), ('rpr', 1), ('plt', 1), ('sci', 1), ('eng', 1), ('wpn', 1)]):
                  crew_stat_value = self.crewStats[i][0]
                  crew_stats_m[stat_name] = float(fatigue_m) * (1 - (total_tp / max_training_points)) * (1 - (float(crew_stat_value) / max_training_points))
            for i, (stat_name, _) in enumerate([('hp', 1), ('atk', 1), ('abl', 1), ('sta', 1), ('rpr', 1), ('plt', 1), ('sci', 1), ('eng', 1), ('wpn', 1)]):
                  self.crewStats[i][1] = round(crew_stats_m[stat_name],3)
            self.statsTable.viewport().update()
            return
      def getConsumableName(self):
            training_stat = self.trainingStatBox.currentText()
            training_level = self.trainingLevelBox.currentText()
            
            parseName = training_stat+" "+training_level
            result = next((item for item in self.trainingList if item[0] == parseName), None)
            self.trainingTypeName.setText(result[1])
            self.trainingTable.setModel(None)

            if result[2]:
                  values = result[2]
                  model = self.TrainingStatTableModel(values)
                  self.trainingTable.setModel(model)
            for i in range(9):
                  if i == 1:
                        self.trainingTable.setRowHeight(i,1)
                  else:
                        self.trainingTable.setRowHeight(i,10)
      def modifyTrainingMethods(self):
            selected_training_stat = self.trainingStatBox.currentText()            
            modified_data_list = []
            for item in self.trainingList:
                  key, name, data = item[0], item[1], item[2]
                  if key.startswith(selected_training_stat[:3]):
                        modified_data_list.append((name, key, data))
            self.resetTrainingData()
            if selected_training_stat == "RPR":
                  for i in range(7):
                        for j in range(9):
                              modified_data_list[i][2][j] *= self.crewStats[j][1]
                              modified_data_list[i][2][j] = math.floor(modified_data_list[i][2][j])
            else:
                  for i in range(10):
                        for j in range(9):
                              modified_data_list[i][2][j] *= self.crewStats[j][1]
                              modified_data_list[i][2][j] = math.floor(modified_data_list[i][2][j])
      def onComboBoxValueChanged(self):
            self.getConsumableName()
            self.updateFatigueMod()
            self.calculateTrainingChart()
            self.modifyTrainingMethods()
      def resetTrainingData(self):
            self.trainingList = [
                  ("ABL Green", "Steam Yoga", [0,0,4,1,0,0,0,0,0]),
                  ("ABL Blue", "Crew vs Wild", [1,1,8,1,0,0,0,0,0]),
                  ("ABL Gold", "Space Marine", [1,1,12,2,0,0,0,0,0]),
                  ("ABL Common", "Paracetamol", [1,0,2,1,0,1,0,0,0]),
                  ("ABL Elite", "Paracetamol Rapid", [2,0,4,1,0,2,0,0,0]),
                  ("ABL Unique", "Ibuprofen", [3,0,8,3,0,3,0,0,1]),
                  ("ABL Epic", "Ibuprofen Rapid", [5,0,16,3,0,5,0,0,2]),
                  ("ABL Hero", "Ginkgo", [12,0,24,4,0,12,0,0,3]),
                  ("ABL Special", "Brain Enhancer", [8,0,48,3,0,8,0,0,2]),
                  ("ABL Legendary", "Super Brain Enhancer", [3,0,96,1,0,3,0,0,1]),
                  ("ATK Green", "Kickbox", [0,4,0,1,0,0,0,0,0]),
                  ("ATK Blue", "BJJ", [1,8,1,1,0,0,0,0,0]),
                  ("ATK Gold", "Shaolin Tradition", [1,12,1,2,0,0,0,0,0]),
                  ("ATK Common", "Chicken Skewer", [0,2,1,1,0,0,0,0,1]),
                  ("ATK Elite", "Yakitori", [0,4,2,1,0,0,0,0,2]),
                  ("ATK Unique", "Double Yakitori", [1,8,3,3,0,0,0,0,3]),
                  ("ATK Epic", "Shish Kebabs", [2,16,5,3,0,0,0,0,5]),
                  ("ATK Hero", "Drumsticks", [3,24,12,4,0,0,0,0,12]),
                  ("ATK Special", "Steak", [2,48,8,3,0,0,0,0,8]),
                  ("ATK Legendary", "Roast Turkey", [1,96,3,1,0,0,0,0,3]),
                  ("ENG Green", "Study Expert Engineering Manual", [0,0,0,0,1,0,0,4,0]),
                  ("ENG Blue", "Engineering Summit", [0,0,0,0,1,1,1,8,0]),
                  ("ENG Gold", "Engineering PhD", [0,0,0,0,2,0,0,12,1]),
                  ("ENG Common", "Standard Engineering Tool Kit", [0,0,0,1,1,0,1,2,0]),
                  ("ENG Elite", "Obsolete Engineering Tool Kit", [0,0,0,1,2,0,2,4,0]),
                  ("ENG Unique", "Starter Engineering Tool Kit", [0,0,0,3,3,1,3,8,0]),
                  ("ENG Epic", "Advanced Engineering Tool Kit", [0,0,0,3,5,2,5,16,0]),
                  ("ENG Hero", "Rare Engineering Tool Kit", [0,0,0,4,12,3,12,24,0]),
                  ("ENG Special", "Prototype Engineering Tool Kit", [0,0,0,3,8,2,8,48,0]),
                  ("ENG Legendary", "Alien Engineering Tool Kit", [0,0,0,1,3,1,3,96,0]),
                  ("HP Green", "Bench Press", [4,0,0,1,0,0,0,0,0]),
                  ("HP Blue", "Muscle Beach", [8,1,1,1,0,0,0,0,0]),
                  ("HP Gold", "Olympic Weightlifting", [12,1,1,2,0,0,0,0,0]),
                  ("HP Common", "Small Protein Shake", [2,1,0,1,0,0,0,1,0]),
                  ("HP Elite", "Regular Protein Shake", [4,2,0,1,0,0,0,2,0]),
                  ("HP Unique", "Large Protein Shake", [8,3,1,3,0,0,0,3,0]),
                  ("HP Epic", "Super Protein Shake", [16,5,2,3,0,0,0,5,0]),
                  ("HP Hero", "HGH", [24,12,3,4,0,0,0,12,0]),
                  ("HP Special", "Enhanced HGH", [48,8,2,3,0,0,0,8,0]),
                  ("HP Legendary", "Prototype HGH", [96,3,1,1,0,0,0,3,0]),
                  ("PLT Green", "Read Expert Pilot Handbook", [0,0,0,0,0,4,0,0,1]),
                  ("PLT Blue", "Pilot Summit", [0,0,0,0,1,8,0,1,1]),
                  ("PLT Gold", "Pilot Expert", [0,0,0,0,1,12,0,0,2]),
                  ("PLT Common", "Street Map", [0,0,0,1,0,2,0,1,1]),
                  ("PLT Elite", "Travel Map", [0,0,0,1,0,4,0,2,2]),
                  ("PLT Unique", "World Map", [0,1,0,3,0,8,0,3,3]),
                  ("PLT Epic", "Global Map", [0,2,0,3,0,16,0,5,5]),
                  ("PLT Hero", "System Map", [0,3,0,4,0,24,0,12,12]),
                  ("PLT Special", "Star Map", [0,2,0,3,0,48,0,8,8]),
                  ("PLT Legendary", "Galactic Navigation Map", [0,1,0,1,0,96,0,3,3]),
                  ("RPR Common", "Repair Guide", [0,0,0,1,2,0,1,1,0]),
                  ("RPR Elite", "New Repair Guide", [0,0,0,1,4,0,2,2,0]),
                  ("RPR Unique", "Advanced Repair Guide", [0,0,1,3,8,0,3,3,0]),
                  ("RPR Epic", "Epic Repair Guide", [0,0,2,3,16,0,5,5,0]),
                  ("RPR Hero", "Lost Repair Guide", [0,0,3,4,24,0,12,12,0]),
                  ("RPR Special", "Special Repair Guide", [0,0,2,3,48,0,8,8,0]),
                  ("RPR Legendary", "Legendary Repair Guide", [0,0,1,1,96,0,3,3,0]),
                  ("SCI Green", "Big Book of Science", [0,0,0,0,0,0,4,1,0]),
                  ("SCI Blue", "Scientific Summit", [0,0,0,0,1,0,8,1,1]),
                  ("SCI Gold", "Science PhD", [0,0,0,0,0,0,12,2,1]),
                  ("SCI Common", "Drop of Brain Juice", [0,0,1,1,1,0,2,0,0]),
                  ("SCI Elite", "Sliver of Brain Juice", [0,0,2,1,2,0,4,0,0]),
                  ("SCI Unique", "Brew of Brain Juice", [0,0,3,3,3,0,8,0,1]),
                  ("SCI Epic", "Tincture of Brain Juice", [0,0,5,3,5,0,16,0,2]),
                  ("SCI Hero", "Solution of Brain Juice", [0,0,12,4,12,0,24,0,3]),
                  ("SCI Special", "Concentrate of Brain Juice", [0,0,8,3,8,0,48,0,2]),
                  ("SCI Legendary", "Elixir of Brain Juice", [0,0,3,1,3,0,96,0,1]),
                  ("STA Green", "Weighted Run", [0,0,0,5,0,0,0,0,0]),
                  ("STA Blue", "Hardcore Aerobics", [2,2,2,8,0,0,0,0,0]),
                  ("STA Gold", "Everest Climb", [3,3,3,16,0,0,0,0,0]),
                  ("STA Common", "Small Cola", [1,1,1,2,1,1,1,1,1]),
                  ("STA Elite", "Large Cola", [1,1,1,4,1,1,1,1,1]),
                  ("STA Unique", "Mountain Brew", [2,2,2,8,2,2,2,2,2]),
                  ("STA Epic", "Pink Cow", [3,3,3,16,3,3,3,3,3]),
                  ("STA Hero", "Large Pink Cow", [4,4,4,24,4,4,4,4,4]),
                  ("STA Special", "U", [3,3,3,48,3,3,3,3,3]),
                  ("STA Legendary", "Father", [2,2,2,96,2,2,2,2,2]),
                  ("WPN Green", "Read Expert Weapon Theory", [0,0,0,0,0,0,1,0,4]),
                  ("WPN Blue", "Weapons Summit", [0,0,0,0,1,1,1,0,8]),
                  ("WPN Gold", "Weapons PhD", [0,0,0,0,2,0,0,1,12]),
                  ("WPN Common", "Military Recruit Handbook", [0,1,0,1,0,1,0,0,2]),
                  ("WPN Elite", "Standard Combat Manual", [0,2,0,1,0,2,0,0,4]),
                  ("WPN Unique", "Galetrooper Training Manual", [0,3,0,3,0,3,1,0,8]),
                  ("WPN Epic", "Elite Combat Manual", [0,5,0,3,0,5,2,0,16]),
                  ("WPN Hero", "Veteran's Guidebook", [0,12,0,4,0,12,3,0,24]),
                  ("WPN Special", "How To Shoot Your Shot'", [0,8,0,3,0,8,2,0,48]),
                  ("WPN Legendary", "Sharpshooter's Cheatbook", [0,3,0,1,0,3,1,0,96]),
            ]
      def wipeCrewStats(self):
            for i in range(9):
                  self.crewStats[i][0] = 0
      class TrainingStatTableModel(QAbstractTableModel):
            def __init__(self, values, parent=None):
                  super().__init__()
                  self.values = values
                  self.verticalHeaders = ['HP','ATK','ABL','STA','RPR','PLT','SCI','ENG','WPN']
                  self.horizontalHeaders = ['']
            def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
                  if role == Qt.ItemDataRole.DisplayRole:
                        if orientation == Qt.Orientation.Horizontal and section < len(self.horizontalHeaders):
                              return self.horizontalHeaders[section]
                        elif role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Vertical:
                              return self.verticalHeaders[section]
                  return None
            def rowCount(self, parent):
                  return len(self.values)
            def columnCount(self, parent):
                  return 1  # Assuming you have only one column
            def data(self, index, role):
                  if role == Qt.ItemDataRole.DisplayRole:
                        row = index.row()
                        if 0 <= row < len(self.values):
                              return str(self.values[row])
                  return None
            def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
                  if index.isValid() and role == Qt.ItemDataRole.EditRole:
                        if isinstance(value, int):
                              self.values[index.row()] = value
                              self.dataChanged.emit(index, index)
                              self.parent.onComboBoxValueChanged()
                              return True
                        else:
                              return False
                  return False
      class TrainingListTableModel(QAbstractTableModel):
            def __init__(self, data, parent=None):
                  super().__init__()
                  self._data = data
                  self.parent = parent
                  self.verticalHeaders = ['HP','ATK','ABL','STA','RPR','PLT','SCI','ENG','WPN']
                  self.horizontalHeaders = ['']
            def rowCount(self, index):
                  return len(self._data)
            def columnCount(self, index):
                  return len(self._data[0])
            def data(self, index, role=Qt.ItemDataRole.DisplayRole):
                  if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
                        return str(self._data[index.row()][index.column()])
            def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
                  if index.isValid():
                        self._data[index.row()][index.column()] = value
                        self.dataChanged.emit(index, index)
                        self.parent.onComboBoxValueChanged()
                        return True
                  return False
            def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
                  if role == Qt.ItemDataRole.DisplayRole:
                        if orientation == Qt.Orientation.Horizontal and section < len(self.horizontalHeaders):
                              return self.horizontalHeaders[section]
                        elif role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Vertical:
                              return self.verticalHeaders[section]
                  return None
            def getCellValue(self, row, column):
                  return self._data[row][column]
            def flags(self, index):
                  return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
      class TrainingChartTableModel(QAbstractTableModel):
            def __init__(self, data, trainingStatBox, parent=None):
                  super().__init__(parent)
                  self._data = data
                  self.trainingStatBox = trainingStatBox
                  self.horizontalHeaders = ['Training', 'HP','ATK','ABL','STA','RPR','PLT','SCI','ENG','WPN']
                  self.verticalHeaders = [''] * len(data)
            def rowCount(self, index):
                  return len(self._data)
            def columnCount(self, index):
                  return len(self.horizontalHeaders)
            def data(self, index, role=Qt.ItemDataRole.DisplayRole):
                  if role == Qt.ItemDataRole.DisplayRole:
                        row = index.row()
                        col = index.column()
                        if col == 0:
                              return self._data[row][0]  # First column data
                        elif 0 < col <= len(self.horizontalHeaders) - 1:
                              item_data = self._data[row][1]
                              if isinstance(item_data, str):
                                    return ""  # Return an empty string for non-existent data
                              else:
                                    return item_data[col - 1]  # Data values (adjusting for the first column)
                  elif role == Qt.ItemDataRole.BackgroundRole:
                        value = self.data(index, Qt.ItemDataRole.DisplayRole)
                        col = index.column()
                        if value == 0:
                              return QColor(198,239,206)
                        elif self.trainingStatBox.currentText() == self.horizontalHeaders[col]:
                              return QColor(189,215,238)
                        else:
                              return QColor(255,255,255)
                  return None
            def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
                  if role == Qt.ItemDataRole.EditRole and index.isValid():
                        row = index.row()
                        col = index.column()
                        self._data[row][2][col - 1] = value
                        self.dataChanged.emit(index, index)
                        return True
                  return False
            def updateData(self, data):
                  self.beginResetModel()
                  self._data = data
                  self.endResetModel()
            def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
                  if role == Qt.ItemDataRole.DisplayRole:
                        if orientation == Qt.Orientation.Horizontal:
                              if section == 0:
                                    return "Name"
                              else:
                                    return f"{self.horizontalHeaders[section]}"
                        else:
                              return str(section + 1)
                  return None
            def getCellValue(self, row, column):
                  return self._data[row][column]
            def flags(self, index):
                  return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
      class StatsTableModel(QAbstractTableModel):
            def __init__(self, data, parent=None):
                  super().__init__()
                  self._data = data
                  self.parent = parent
                  self.verticalHeaders = ['HP','ATK','ABL','STA','RPR','PLT','SCI','ENG','WPN']
                  self.horizontalHeaders = ['Current', 'Multiplier', '% Required']
            def rowCount(self, index):
                  return len(self._data)
            def columnCount(self, index):
                  return len(self._data[0])
            def data(self, index, role=Qt.ItemDataRole.DisplayRole):
                  if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
                        return str(self._data[index.row()][index.column()])
            def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
                  if index.isValid() and role == Qt.ItemDataRole.EditRole:
                        try:
                              int_value = int(value)
                        except ValueError:
                              int_value = 0
                        self._data[index.row()][index.column()] = int_value
                        self.dataChanged.emit(index, index)
                        self.parent.onComboBoxValueChanged()
                        return True
                  return False
            def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
                  if role == Qt.ItemDataRole.DisplayRole:
                        if orientation == Qt.Orientation.Horizontal and section < len(self.horizontalHeaders):
                              return self.horizontalHeaders[section]
                        elif role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Vertical:
                              return self.verticalHeaders[section]
                  return None
            def getCellValue(self, row, column):
                  return self._data[row][column]
            def flags(self, index):
                  if index.column() >= 1:
                        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
                  else:
                        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
## Startup and program operation
if __name__ == "__main__":
      app = QtWidgets.QApplication(sys.argv)
      if create_connection():
            create_table()
      else:
            sys.exit(1)
      window = MainWindow()
      app.exec()