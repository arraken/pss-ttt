from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtWidgets import QMessageBox, QListWidgetItem
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from datetime import date
from openpyxl import load_workbook
import sys
import webbrowser


'''
Start building database, pull player info from where?

Make ways for players to search by fleet to find name for foreign characters

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
class DialogBox(QtWidgets.QDialog):
      copyFleetSearchClicked = QtCore.pyqtSignal(str, bool)

      def __init__(self):
            super().__init__()
            uic.loadUi('pss-ttt-fleetbrowser.ui', self)
            self.fleetSearchClose.clicked.connect(self.accept)
            self.copyFleetSearch.clicked.connect(self.onCopyFleetSearchClicked)
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
class MainWindow(QtWidgets.QMainWindow):
      def __init__(self):
            super(MainWindow, self).__init__() # Call the inherited classes __init__ method
            uic.loadUi('pss-ttt.ui', self) # Load the .ui file
            self.show()
            #self.copyFleetSearchSignal = QtCore.pyqtSignal(str)

            self.lockUnlockButton.clicked.connect(self.changeButtonText)
            self.searchButton.clicked.connect(self.searchPlayer)
            self.saveNewData.clicked.connect(self.submitNewPlayerData)
            self.resetButton.clicked.connect(self.resetDataFields)
            self.pixyshipLayoutButton.clicked.connect(self.pixyshipURL)
            self.tournamentSubmit.clicked.connect(self.submitTournamentData)
            self.legendsSubmit.clicked.connect(self.submitLegendsData)
            self.pvpSubmit.clicked.connect(self.pvpLegendsData)
            self.importButton.clicked.connect(self.importExcel)
            self.fleetSearchButton.clicked.connect(self.open_fleetBrowser)
            self.delLegendsButton.clicked.connect(self.deleteLegendsLine)
            self.delTournyButton.clicked.connect(self.deleteTournamentLine)
            self.delPVPButton.clicked.connect(self.deletePVPLine)
            
            self.fleetBrowser = DialogBox()
            self.fleetBrowser.copyFleetSearchClicked.connect(self.handleCopyFleetSearchClicked)
      def open_fleetBrowser(self):
            self.fleetBrowser.populateFleetList(self.fleetName.toPlainText())
            self.fleetBrowser.exec()
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
      
## Startup
if __name__ == "__main__":
      if create_connection():
            create_table()
      else:
            sys.exit(1)
      app = QtWidgets.QApplication(sys.argv)
      window = MainWindow()
      box = DialogBox()
      app.exec()