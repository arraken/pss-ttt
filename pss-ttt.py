from PyQt6 import QtWidgets, uic
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
            print("Fatal Error: Connection with targets database failed.")
            return False
      if not tournyfightsdb.open():
            print("Fatal Error: Connection with tournament fights database failed.")
            return False
      if not legendfightsdb.open():
            print("Fatal Error: Connection with legends fight database failed.")
            return False
      if not pvpfightsdb.open():
            print("Fatal Error: Connection with pvp fight database failed.")
      return True

# Name - Battle Type - Trophies/Stars - Date
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
            print("FightsDB[41]:", query.lastError().text())
            return False
      print("Fights Data processed successfully ",data)
      return True

def write_to_targets_database(data):
      query = QSqlQuery(QSqlDatabase.database("targetsdb"))
      query.prepare("INSERT OR REPLACE INTO players(playername, fleetname, laststars, beststars, trophies, maxtrophies, notes) VALUES(?, ?, ?, ?, ?, ?, ?)")
      for i in range(7):
            query.bindValue(i, data[i])
      if not query.exec():
            print("TargetsDB[52]:", query.lastError().text())
            return False
      #print("Targets Data processed successfully")
      return True

class Ui(QtWidgets.QMainWindow):
      def __init__(self):
            super(Ui, self).__init__() # Call the inherited classes __init__ method
            uic.loadUi('pss-ttt.ui', self) # Load the .ui file
            self.show()
            self.lockUnlockButton.clicked.connect(self.changeButtonText)
            self.searchButton.clicked.connect(self.searchPlayer)
            self.saveNewData.clicked.connect(self.submitNewPlayerData)
            self.resetButton.clicked.connect(self.resetDataFields)
            self.pixyshipLayoutButton.clicked.connect(self.pixyshipURL)
            self.tournamentSubmit.clicked.connect(self.submitTournamentData)
            self.legendsSubmit.clicked.connect(self.submitLegendsData)
            self.pvpSubmit.clicked.connect(self.pvpLegendsData)
            self.importButton.clicked.connect(self.importExcel)

      def importExcel(self):
            workbook = load_workbook("Import.xlsx")
            sheet = workbook.active
            if not QSqlDatabase.database("targetsdb").open():
                  print("Unable to open targets database for import")
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
                        print("Error inserting data:", query.lastError().text())
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
                  print("Query execution failed: ", query.lastError().text())
                  return
            
            
      def changeButtonText(self):
            if self.lockUnlockButton.text() == "Locked":
                  self.lockUnlockButton.setText("Unlocked")
                  self.playerDataChange(False)
            else:
                  self.lockUnlockButton.setText("Locked")
                  self.playerDataChange(True)

      def playerDataChange(self, boolean_value):
            self.fleetName.setReadOnly(boolean_value)
            self.lastStars.setReadOnly(boolean_value)
            self.bestStars.setReadOnly(boolean_value)
            self.currentTrophies.setReadOnly(boolean_value)
            self.maxTrophies.setReadOnly(boolean_value)
            self.playerNotes.setReadOnly(boolean_value)
      
      def submitNewPlayerData(self):
            player_data = [self.playerNameSearchBox.toPlainText(), self.fleetName.toPlainText(), self.lastStars.toPlainText(),
                        self.bestStars.toPlainText(), self.currentTrophies.toPlainText(), self.maxTrophies.toPlainText(), self.playerNotes.toPlainText()]
            if int(self.lastStars.toPlainText()) > int(self.bestStars.toPlainText()):
                  player_data = [self.playerNameSearchBox.toPlainText(), self.fleetName.toPlainText(), self.lastStars.toPlainText(),
                        self.lastStars.toPlainText(), self.currentTrophies.toPlainText(), self.maxTrophies.toPlainText(), self.playerNotes.toPlainText()]
            if int(self.currentTrophies.toPlainText()) > int(self.maxTrophies.toPlainText()):
                  player_data = [self.playerNameSearchBox.toPlainText(), self.fleetName.toPlainText(), self.lastStars.toPlainText(),
                        self.lastStars.toPlainText(), self.currentTrophies.toPlainText(), self.currentTrophies.toPlainText(), self.playerNotes.toPlainText()]
            if write_to_targets_database(player_data):
                  player_data.clear()
            else:
                  print("TargetsDB: Error writing data to the database - Dumping data")
                  print("[***]:",player_data)

      def updateFightTables(self, fights):
            name = self.playerNameSearchBox.toPlainText()
            if fights == "tourny":
                  query = QSqlQuery(QSqlDatabase.database("tournydb"))
                  query.prepare("SELECT rewards, datetag FROM fights WHERE name LIKE ?")
                  if query.lastError().isValid():
                        print("TournyDB: ",query.lastError().text())
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
                        print("LegendsDB: ",query.lastError().text())
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
                        print("pvpDB: ",query.lastError().text())
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
                  print("FightsDB: Error writing data to the database - Dumping data")
                  print("[***]:",tournament_data)
            self.tournyTable.clearSpans()
            self.updateFightTables("tourny")
            tournament_data.clear()
      def submitLegendsData(self):
            todaysdate = str(date.today())
            legends_data = [self.playerNameSearchBox.toPlainText(), str(self.legendTrophyCount.value()), todaysdate]
            if not write_to_fights_database(legends_data, "legends"):
                  print("FightsDB: Error writing data to the database - Dumping data")
                  print("[***]:",legends_data)
            self.tournyTable.clearSpans()
            self.updateFightTables("legends")
            legends_data.clear()
      def pvpLegendsData(self):
            todaysdate = str(date.today())
            pvp_data = [self.playerNameSearchBox.toPlainText(), str(self.trophyCount.value()), todaysdate]
            if not write_to_fights_database(pvp_data, "pvp"):
                  print("FightsDB: Error writing data to the database - Dumping data")
                  print("[***]:",pvp_data)
            self.tournyTable.clearSpans()
            self.updateFightTables("pvp")
            pvp_data.clear()
            

if __name__ == "__main__":
      if create_connection():
            create_table()
      else:
            sys.exit(1)
      app = QtWidgets.QApplication(sys.argv)
      window = Ui()
      app.exec()