from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import QMessageBox, QListWidgetItem, QTableView
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from datetime import date
from openpyxl import load_workbook
from decimal import Decimal
import sys, csv, math, webbrowser, os

'''
To-do
Keep up to date with targets easier (import xls somehow? talk with the worst and see if there's a specific formatting)
Talk with the worst and see if I can just directly hook into savy API for frequent updates somehow on players?
Add column in fights db for hp remaining

Calculate up stars gained each time a new value is entered into the table
Find spot to display Est cumulative stars and current cumulative stars
'''
def create_connection():
      targetsdb = QSqlDatabase.addDatabase('QSQLITE', "targetsdb")
      tournyfightsdb = QSqlDatabase.addDatabase('QSQLITE', "tournydb")
      legendfightsdb = QSqlDatabase.addDatabase('QSQLITE', "legendsdb")
      pvpfightsdb = QSqlDatabase.addDatabase('QSQLITE', "pvpdb")
      targetsdb.setDatabaseName('targets.db')
      tournyfightsdb.setDatabaseName('tournyfights.db')
      legendfightsdb.setDatabaseName('legendfights.db')
      pvpfightsdb.setDatabaseName('pvpfights.db')
      if not targetsdb.open():
            throwErrorMessage("Fatal Error", "Targets DB did not open properly")
            return False
      if not tournyfightsdb.open():
            throwErrorMessage("Fatal Error", "Tournament Fights DB did not open properly")
            return False
      if not legendfightsdb.open():
            throwErrorMessage("Fatal Error", "Legend Fights DB did not open properly")
            return False
      if not pvpfightsdb.open():
            throwErrorMessage("Fatal Error", "PVP Fights DB did not open properly")
      return True
def create_table():
      targetsQuery = QSqlQuery(QSqlDatabase.database("targetsdb"))
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
#      print("Database type selected: ", fights)
      query.prepare("INSERT OR REPLACE INTO fights(name, rewards, datetag) VALUES(?, ?, ?)")
      for i in range(3):
            query.bindValue(i, data[i].strip())
      if not query.exec():
            throwErrorMessage("FightsDB:", query.lastError().text())
            return False
      return True
def write_to_targets_database(data):
      query = QSqlQuery(QSqlDatabase.database("targetsdb"))
      query.prepare("INSERT OR REPLACE INTO players(playername, fleetname, laststars, beststars, trophies, maxtrophies, notes) VALUES(?, ?, ?, ?, ?, ?, ?)")
      for i in range(7):
            query.bindValue(i, data[i])
      if not query.exec():
            throwErrorMessage("TargetsDB:", query.lastError().text())
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
            if not QSqlDatabase.database("targetsdb").isOpen():
                  if not QSqlDatabase.database("targetsdb").open():
                        throwErrorMessage("Database Connection Failure", "Targets DB did not open properly")
                        return

            query = QSqlQuery(QSqlDatabase.database("targetsdb"))
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
            self.pvpSubmit.clicked.connect(self.pvpLegendsData)
            #self.importButton.clicked.connect(self.importExcel)
            self.importButton.clicked.connect(self.importCSV)
            self.fleetSearchButton.clicked.connect(self.open_fleetBrowser)
            self.delLegendsButton.clicked.connect(self.deleteLegendsLine)
            self.delTournyButton.clicked.connect(self.deleteTournamentLine)
            self.delPVPButton.clicked.connect(self.deletePVPLine)
            self.tournyStarsWindow.clicked.connect(self.open_tournamentStarsCalc)
            
            self.fleetBrowser = FleetDialogBox()
            self.fleetBrowser.copyFleetSearchClicked.connect(self.handleCopyFleetSearchClicked)

            self.starCalculator = TournamentDialogBox()
        #    self.starCalculator.openCalculator.connect(self.handleOpenCalculator)

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
      def importExcel(self):
            workbook = load_workbook("Import.xlsx")
            sheet = workbook.active
            if not QSqlDatabase.database("targetsdb").open():
                  throwErrorMessage("Targets Database Error", "Unable to open targets database for import")
                  return False
            query = QSqlQuery(QSqlDatabase.database("targetsdb"))
            query.exec(f"CREATE TABLE IF NOT EXISTS players (playername TEXT, fleetname TEXT, laststars INT, beststars INT, trophies INT, maxtrophies INT, notes TEXT)")

            for row in sheet.iter_rows(min_row=2, values_only=True):  # Start from the second row assuming the first row is header
                  playername, fleetname, laststars, beststars, trophies, maxtrophies, notes = row
                  query.prepare(f"INSERT INTO players (playername, fleetname, laststars, beststars, trophies, maxtrophies, notes) "
                      "VALUES (?, ?, ?, ?, ?, ?, ?)")
                  query.addBindValue(playername)
                  query.addBindValue(fleetname)
                  query.addBindValue(laststars)
                  query.addBindValue(beststars)
                  query.addBindValue(trophies)
                  query.addBindValue(maxtrophies)
                  query.addBindValue(notes)
                  if not query.exec():
                        throwErrorMessage("Targets Database Insertion Error:", query.lastError().text())
                        sys.exit(1)
            
            QSqlDatabase.database("targetsdb").close()
            print("Data imported successfully")
            return True
      def importCSV(self):
            data_to_insert = []
            with open('fleetsdata.csv', 'r', encoding='utf-8') as csvfile:
                  reader = csv.reader(csvfile, delimiter=';')
                  for row in reader:
                        specific_data = (row[2], row[1], row[7], row[7], row[5], row[6], " ")
                        data_to_insert.append(specific_data)
    
            if not QSqlDatabase.database("targetsdb").open():
                  throwErrorMessage("Targets Database Error", "Unable to open targets database for import")
                  return False
    
            query = QSqlQuery(QSqlDatabase.database("targetsdb"))
            query.exec("CREATE TABLE IF NOT EXISTS players (playername TEXT PRIMARY KEY, fleetname TEXT NOT NULL, laststars TEXT NOT NULL, beststars TEXT NOT NULL, trophies TEXT NOT NULL, maxtrophies TEXT NOT NULL, notes TEXT NOT NULL)")
    
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
                        query.prepare("UPDATE players SET laststars = ?, beststars = ?, trophies = ?, maxtrophies = ?, notes = ? WHERE playername = ? AND fleetname = ?")
                        query.addBindValue(laststars)
                        query.addBindValue(beststars)
                        query.addBindValue(trophies)
                        query.addBindValue(maxtrophies)
                        query.addBindValue(notes)
                        query.addBindValue(playername)
                        query.addBindValue(fleetname)
                        if not query.exec_():
                              print("Update failed:", query.lastError().text())
                  else:
                        query.prepare("INSERT INTO players (playername, fleetname, laststars, beststars, trophies, maxtrophies, notes) VALUES (?, ?, ?, ?, ?, ?, ?)")
                        query.addBindValue(playername)
                        query.addBindValue(fleetname)
                        query.addBindValue(laststars)
                        query.addBindValue(beststars)
                        query.addBindValue(trophies)
                        query.addBindValue(maxtrophies)
                        query.addBindValue(notes)
                        if not query.exec():
                              print("Insert failed:", query.lastError().text())
            QSqlDatabase.database("targetsdb").commit()
      def pixyshipURL(self):
            searchName = self.playerNameSearchBox.toPlainText()
            print(searchName)
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
            text = self.playerNameSearchBox.toPlainText()
            self.resetDataFields()
            self.playerNameSearchBox.insertPlainText(text)
            query = QSqlQuery("SELECT * FROM players", QSqlDatabase.database("targetsdb"))
            if query.exec():
                  found = False
                  while query.next():
                        entry = query.value(0)
                        if(entry.casefold() == text.casefold()):
                              self.fleetName.insertPlainText(query.value(1))
                              self.lastStars.insertPlainText(query.value(2))
                              self.bestStars.insertPlainText(query.value(3))
                              self.currentTrophies.insertPlainText(query.value(4))
                              self.maxTrophies.insertPlainText(query.value(5))
                              self.playerNotes.insertPlainText(query.value(6))
                              self.updateFightTables("tourny")
                              self.updateFightTables("legends")
                              self.updateFightTables("pvp")
                              found = True
                  if not found:
                        return
            else:
                  throwErrorMessage("Query execution failed: ", query.lastError().text())
                  return                 
      def changeButtonText(self):
            if self.lockUnlockButton.text() == "Locked":
                  self.lockUnlockButton.setText("Unlocked")
                  self.playerDataChange(False)
            else:
                  self.lockUnlockButton.setText("Locked")
                  self.playerDataChange(True)
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
                  throwErrorMessage("TargetsDB: Error writing data to the database - Dumping data", player_data)
      def updateFightTables(self, fights):
            name = self.playerNameSearchBox.toPlainText()
            if fights == "tourny":
                  query = QSqlQuery(QSqlDatabase.database("tournydb"))
                  query.prepare("SELECT rewards, datetag FROM fights WHERE name LIKE ?")
                  if query.lastError().isValid():
                        throwErrorMessage("TournyDB Update: ",query.lastError().text())
                        sys.exit(-1)
                  query.addBindValue('%' + self.playerNameSearchBox.toPlainText() + '%')
                  query.exec()
                  model = QSqlTableModel()
                  model.setQuery(query)
                  self.tournyTable.setModel(model)
                  self.tournyTable.setColumnWidth(0,50)
                  self.tournyTable.show()
            if fights == "legends":
                  query = QSqlQuery(QSqlDatabase.database("legendsdb"))
                  query.prepare("SELECT rewards, datetag FROM fights WHERE name LIKE ?")
                  if query.lastError().isValid():
                        throwErrorMessage("LegendsDB Update: ",query.lastError().text())
                        sys.exit(-1)
                  query.addBindValue('%' + self.playerNameSearchBox.toPlainText() + '%')
                  query.exec()
                  model = QSqlTableModel()
                  model.setQuery(query)
                  self.legendsTable.setModel(model)
                  self.legendsTable.setColumnWidth(0,50)
                  self.legendsTable.show()
            if fights == "pvp":
                  query = QSqlQuery(QSqlDatabase.database("pvpdb"))
                  query.prepare("SELECT rewards, datetag FROM fights WHERE name LIKE ?")
                  if query.lastError().isValid():
                        throwErrorMessage("pvpDB Update: ",query.lastError().text())
                        sys.exit(-1)
                  query.addBindValue('%' + self.playerNameSearchBox.toPlainText() + '%')
                  query.exec()

                  model = QSqlTableModel()
                  model.setQuery(query)
                  self.pvpTable.setModel(model)
                  self.pvpTable.setColumnWidth(0,50)
                  self.pvpTable.show()            
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
      def pvpLegendsData(self):
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
            print("Stars table data has been saved to", filename)
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
            print("Stars table data has been loaded from", filename)
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
            # Sort out day 1 planning first, then 2 should be easier and 3 shoudl be automatic then
                        
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
                  #print("Day[",i,"] star target: ",todaysStarsTarget) debugging
                  #print("Day[",i,"] start value: ",start_value)
                  #print("Day[",i,"] end value", end_value)
                  index = self.model.index(0,i)
                  self.model.setData(index, todaysStarsTarget)
                  self.estStarsBox.clear()
                  if i == 6:
                        self.estStarsBox.insertPlainText(str(end_value))
            self.tournamentTable.show()
            self.saveStarsTableToCSV("starstable.csv")

## Startup
if __name__ == "__main__":
      if create_connection():
            create_table()
      else:
            sys.exit(1)
      app = QtWidgets.QApplication(sys.argv)
      window = MainWindow()
      app.exec()