from PyQt6 import QtWidgets, uic
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from datetime import date
import sys
import webbrowser


'''
Get bottom buttons to save correctly
Create 3 datasets for the results tables
date (just copy todays easier?), value entered

Start building database, pull player info from where?
'''
def create_connection():
      targetsdb = QSqlDatabase.addDatabase('QSQLITE', "connection1")
      fightsdb = QSqlDatabase.addDatabase('QSQLITE', "connection2")
      targetsdb.setDatabaseName('targets.db')
      fightsdb.setDatabaseName('fights.db')
      if not targetsdb.open():
            print("Fatal Error: Connection with targets database failed.")
            return False
      if not fightsdb.open():
            print("Fatal Error: Connection with fights database failed.")
            return False      
      return True

# Name - Battle Type - Trophies/Stars - Date
def create_table():
      targetsQuery = QSqlQuery(QSqlDatabase.database("connection1"))
      fightsQuery = QSqlQuery(QSqlDatabase.database("connection2"))
      targetsQuery.exec("CREATE TABLE IF NOT EXISTS players (playername TEXT PRIMARY KEY, fleetname TEXT NOT NULL, laststars TEXT NOT NULL, beststars TEXT NOT NULL, trophies TEXT NOT NULL, maxtrophies TEXT NOT NULL, notes TEXT NOT NULL)")
      fightsQuery.exec("CREATE TABLE IF NOT EXISTS fights (name TEXT NOT NULL, fighttype TEXT NOT NULL, rewards TEXT NOT NULL, datetag TEXT NOT NULL, UNIQUE(name, fighttype, rewards, datetag))")

def write_to_fights_database(data):
      query = QSqlQuery(QSqlDatabase.database("connection2"))
      query.prepare("INSERT INTO fights(name, fighttype, rewards, datetag) VALUES(?, ?, ?, ?)")
      print("[***] Prepared SQL Query: ", query.lastQuery())
      for i in range(4):
            query.bindValue(i, data[i].strip())
      if not query.exec():
            print("FightsDB[41]:", query.lastError().text())
            return False
      print("Fights Data processed successfully")
      return True

def write_to_targets_database(data):
      query = QSqlQuery(QSqlDatabase.database("connection1"))
      query.prepare("INSERT OR REPLACE INTO players(playername, fleetname, laststars, beststars, trophies, maxtrophies, notes) VALUES(?, ?, ?, ?, ?, ?, ?)")
      for i in range(7):
            query.bindValue(i, data[i])
      if not query.exec():
            print("TargetsDB[52]:", query.lastError().text())
            return False
      print("Targets Data processed successfully")
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
            self.tournyTable.clearSpans()
            self.legendsTable.clearSpans()
            self.pvpTable.clearSpans()

      def searchPlayer(self):
            text = self.playerNameSearchBox.toPlainText()
            query = QSqlQuery("SELECT * FROM players", QSqlDatabase.database("connection1"))
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
            if write_to_targets_database(player_data):
                  player_data.clear()
            else:
                  print("TargetsDB: Error writing data to the database - Dumping data")
                  print("[***]:",player_data)

      def updateFightTables(self, data):
            # Current data just updated in button is in tournament_data
            # QTableView needs to include the new data
            print("***", data, "***")
            query = QSqlQuery(QSqlDatabase.database("connection2"))
            query.exec("SELECT fighttype, rewards, datetag FROM fights")
            if query.lastError().isValid():
                  print("[***]: ", query.lastError().text())
            print(query)
            
            model = QSqlTableModel()
            model.setQuery(query)
            if data[1] == "tournament":
                  view = self.tournyTable
            if data[1] == "legends":
                  view = self.legendsTable
            if data[1] == "pvp":
                  view = self.pvpTable
            view.setModel(model)
            view.show()


      def submitTournamentData(self):
            todaysdate = str(date.today())
            tournament_data = [self.playerNameSearchBox.toPlainText(), str("tournament"), str(self.starCount.value()), todaysdate]
            print("Debug[137]:",tournament_data)
            if write_to_fights_database(tournament_data):
                  tournament_data.clear()
            else:
                  print("FightsDB: Error writing data to the database - Dumping data")
                  print("[***]:",tournament_data)
            self.updateFightTables(tournament_data)

if __name__ == "__main__":
      if create_connection():
            create_table()
      else:
            sys.exit(1)
      app = QtWidgets.QApplication(sys.argv)
      window = Ui()
      app.exec()