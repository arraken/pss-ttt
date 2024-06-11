from PyQt6 import QtWidgets, QtCore, uic, QtGui
from PyQt6.QtCore import Qt, QAbstractTableModel, pyqtSignal, QTimer
from PyQt6.QtWidgets import QMessageBox, QListWidgetItem, QTableView, QApplication, QFileDialog, QDialog, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QCompleter
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt6.QtGui import QColor, QStandardItemModel
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from collections import OrderedDict
import sys, csv, math, webbrowser, os, traceback, shutil, asyncio, uuid, pssapi, json, requests
import time, logging
from pssapi import PssApiClient

ACCESS_TOKEN = None
CURRENT_VERSION = "v1.4.2"
CREATOR = "Kamguh11"
SUPPORT_LINK = "Trek Discord - https://discord.gg/psstrek or https://discord.gg/pss"
GITHUB_LINK = "https://github.com/arraken/pss-ttt"
GITHUB_RELEASE_LINK = "https://api.github.com/repos/arraken/pss-ttt/releases/latest"
GITHUB_RELEASE_VERSION = "v1.4.1"
ITEM_AND_CREW_DATABASE_VERSION = None
API_CALL_COUNT = 0
NEW_RELEASE = False

DARK_MODE_STYLESHEET = """
            * {
                  background-color: #333;
                  alternate-background-color: #222; 
                  color: white;
                  }
            QDialogTitleBar {
                  background-color: #000080;
                  color: white;
                  }
            QTableView::section {
                  background-color: #333;
                  color: black;
            }
            QHeaderView::section 
            {
                  background-color: #333;
                  color: #FFFFFF;
            }"""
CURRENT_STYLESHEET = "default"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class ProfileDialog(QDialog):
      def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle("Create Starter Profile")
            layout = QVBoxLayout()
            self.label = QLabel("Enter Profile Name:")
            layout.addWidget(self.label)

            self.profile_name_edit = QLineEdit()
            self.profile_name_edit.setPlaceholderText("Default Profile Name")
            layout.addWidget(self.profile_name_edit)

            self.create_button = QPushButton("Create Profile")
            self.create_button.clicked.connect(self.save_profile)
            layout.addWidget(self.create_button)

            self.setLayout(layout)
            self.profile_name = None
      def save_profile(self):
            self.profile_name = self.profile_name_edit.text()

            if not self.profile_name:
                  QMessageBox.warning(self, "Input Error", "Profile name cannot be empty!")
                  return

            profiles_csv = os.path.join('profiles.csv')
            with open(profiles_csv, mode='a', newline='') as file:
                  writer = csv.writer(file)
                  writer.writerow([self.profile_name])

            QMessageBox.information(self, "Profile Created", f"Profile '{self.profile_name}' has been created and saved.")
        
            self.accept()
      def setStyle(self):
            if CURRENT_STYLESHEET == "default":
                  self.setStyleSheet("")
            elif CURRENT_STYLESHEET == "dark":
                  self.setStyleSheet(DARK_MODE_STYLESHEET)
def get_or_create_uuid():
      config_data = load_config()
      config_list = config_data.get('config')

      if not config_list:
            config_list.append({})
      config_entry = config_list[0]
      if 'uuid' not in config_entry:
            config_entry['uuid'] = str(uuid.uuid4())
      if 'item_database' not in config_entry:
            config_entry['item_database'] = None
      if 'last_api_call' not in config_entry:
            config_entry['last_api_call'] = None
      if 'profile_names' not in config_entry:
            config_entry['profile_names'] = []
      config_data['config'] = [OrderedDict([
           ('uuid', config_entry['uuid']),
           ('item_database', config_entry['item_database']),
           ('last_api_call', config_entry['last_api_call']),
           ('profile_names', config_entry['profile_names'])
            ])]
      save_config(config_data)
      return config_entry['uuid']
def load_config():
      try:
            config_file_path = os.path.join('config.json')
            with open(config_file_path, 'r') as file:
                  return json.load(file)
      except (FileNotFoundError, json.JSONDecodeError):
            return {"config": []}
def save_config(config_data):
      config_file_path = os.path.join('config.json')
      with open(config_file_path, 'w') as file:
            json.dump(config_data, file, indent=4)
def getProfiles(create_if_missing=False):
      config_data = load_config()
      profile_names = []
      if config_data.get('config'):
            for entry in config_data['config']:
                  if entry.get('profile_names'):
                        profile_names.extend(entry['profile_names'])
      if not profile_names and create_if_missing:
            profile_names = createProfile()
            if profile_names:
                  new_entry = {
                        "uuid": str(uuid.uuid4()),
                        "item_database" : None,
                        "last_api_call": None,
                        "profile_names": profile_names
                        }
                  config_data['config'].append(new_entry)
                  save_config(config_data)
                  move_db_files(profile_names[0])
      return profile_names
def getDefaultProfile():
      profiles = getProfiles(create_if_missing=True)
      return profiles[0] if profiles else None
def createProfile():
      dialog = ProfileDialog()
      if dialog.exec() == QDialog.DialogCode.Accepted:
            profile_name = dialog.profile_name
            os.makedirs(f'_profiles/{profile_name}', exist_ok=True)
            config_data = load_config()
            for entry in config_data['config']:
                  if entry.get('profile_names'):
                        entry['profile_names'].append(profile_name)
                        break
            save_config(config_data)
            return [profile_name]
      else:
            return []
def create_connection(profile_name):
      for db_name in QSqlDatabase.connectionNames():
            QSqlDatabase.removeDatabase(db_name)
      profile_path = os.path.join('_profiles', profile_name)
      if not os.path.exists(profile_path):
            throwErrorMessage("Profile Error [create_connection]", f"Profile directory '{profile_path}' does not exist")
            return False
      databases = {
            "targetdb": "targets.db",
            "tournydb": "tournyfights.db",
            "legendsdb": "legendfights.db",
            "pvpdb": "pvpfights.db"
      }
      os.makedirs('_oldprofiles', exist_ok=True)
      for name, filename in databases.items():
            db_path = os.path.join(profile_path, filename)
            if not os.path.exists(db_path):
                  open(db_path, 'a').close()
            db = QSqlDatabase.addDatabase('QSQLITE', name)
            db.setDatabaseName(db_path)
            if not db.open():
                  throwErrorMessage("Fatal Error [create_connection]", f"{name.capitalize()} DB did not open properly")
                  return False
      return True
def create_table():
      tables = {
        "targetdb": "players",
        "tournydb": "fights",
        "legendsdb": "fights",
        "pvpdb": "fights"
      }
      for db_name, table_name in tables.items():
            query = QSqlQuery(QSqlDatabase.database(db_name))
            if db_name == "targetdb":
                  query.exec("CREATE TABLE IF NOT EXISTS players (playername TEXT PRIMARY KEY, fleetname TEXT NOT NULL, laststars TEXT NOT NULL, beststars TEXT NOT NULL, notes TEXT NOT NULL)")
            else:
                  query.exec("CREATE TABLE IF NOT EXISTS fights (name TEXT NOT NULL, rewards TEXT NOT NULL, datetag TEXT NOT NULL, hpremain INTEGER NOT NULL, winloss TEXT NOT NULL, UNIQUE(name, rewards, datetag, hpremain, winloss))")
def write_to_fights_database(data, fights):
      query = QSqlQuery(QSqlDatabase.database(fights + "db"))
      query.prepare("INSERT OR REPLACE INTO fights(name, rewards, datetag, hpremain, winloss) VALUES(?, ?, ?, ?, ?)")
      for i in range(5):
            query.bindValue(i, data[i].strip())
      if not query.exec():
            throwErrorMessage("FightsDB [write_to_fights_database]:", query.lastError().text())
            return False
      return True
def write_to_targets_database(data):
      query = QSqlQuery(QSqlDatabase.database("targetdb"))
      query.prepare("INSERT OR REPLACE INTO players(playername, fleetname, laststars, beststars, notes) VALUES(?, ?, ?, ?, ?)")
      for i in range(5):
            query.bindValue(i, data[i])
      if not query.exec():
            throwErrorMessage("targetdb [write_to_targets_database]:", query.lastError().text())
            return False
      return True
def write_to_tournaments_database(data):
      return data
def write_to_targets_database_batch(player_data_list):
      for player_data in player_data_list:
            if not write_to_targets_database(player_data):
                  throwErrorMessage("targetdb: Error writing data to the database - Dumping data [write_to_targets_database_batch]", player_data)
                  return False
      return True
def modify_SQL():
      query = QSqlQuery(QSqlDatabase.database("targetdb"))
      columns_to_drop = ['trophies', 'maxtrophies']
      for column in columns_to_drop:
            if not query.exec(f"ALTER TABLE players DROP COLUMN {column}"):
                  print(f"Failed to drop column {column}: {query.lastError().text()}")
def throwErrorMessage(text, dump):
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Icon.Critical)
      errortext = "Error: "+text
      msg.setText(errortext)
      msg.setInformativeText(dump)
      msg.setWindowTitle("Error")
      msg.exec()
def move_db_files(profile_name):
      internal_path = os.path.dirname(os.path.abspath(__file__))
      app_path = os.path.dirname(internal_path)
      target_path = os.path.join(app_path, '_profiles', profile_name)
      os.makedirs(target_path, exist_ok=True)

      db_files = ["targets.db", "tournyfights.db", "legendfights.db", "pvpfights.db"]

      for db_file in db_files:
            src = os.path.join(app_path, db_file)
            if os.path.exists(src):
                  dst = os.path.join(target_path, db_file)
                  shutil.move(src, dst)
def should_make_api_call():
      config_data = load_config()
      if not config_data.get('config'):
            return True
      for entry in config_data['config']:
            if entry.get('uuid') == get_or_create_uuid():
                  last_api_call = entry.get('last_api_call')
                  if not last_api_call:
                        return True
                  last_api_call_date = datetime.strptime(last_api_call, '%Y-%m-%dT%H:%M:%S.%f')
                  now = datetime.now()
                  if (now - last_api_call_date).total_seconds() > 24*60*60:
                        return True
                  else:
                        return False
def update_last_api_call():
      config_data = load_config()
      for entry in config_data['config']:
            if entry.get('uuid') == get_or_create_uuid():
                  entry['last_api_call'] = datetime.now().isoformat()
                  save_config(config_data)
def api_database_needs_update(version):
      config_data = load_config()
      if not config_data.get('config'):
            return True
      for entry in config_data['config']:
            ITEM_AND_CREW_DATABASE_VERSION = entry.get('item_database')
            if ITEM_AND_CREW_DATABASE_VERSION is None or ITEM_AND_CREW_DATABASE_VERSION < version:
                  return True
            else:
                  return False
def log_time(message):
      logging.info(message)
class MainWindow(QtWidgets.QMainWindow):
      global CURRENT_VERSION
      global CREATOR
      global SUPPORT_LINK
      global GITHUB_LINK
      global GITHUB_RELEASE_LINK
      global API_CALL_COUNT
      global NEW_RELEASE
      global DARK_MODE_STYLESHEET
      global CURRENT_STYLESHEET
      def __init__(self, parent=None):
            super().__init__(parent)
            start_time = time.time()
            log_time("Starting application")
            uic.loadUi(os.path.join('_internal', '_ui', 'pss-ttt.ui'), self)
            self.show()

            self.client = PssApiClient()
            asyncio.run(self.generateAccessToken())

            self.popProfiles()
            self.connect_signals()
            self.initialize_dialogs()
        
            self.populate_tables()

            if NEW_RELEASE:
                  self.start_blinking_about_menu()
            total_time = time.time() - start_time
            log_time(f"Total startup time: {total_time:.4f} seconds")
      def connect_signals(self):
            self.lockUnlockButton.clicked.connect(self.changeButtonText)
            self.searchButton.clicked.connect(self.searchPlayer)
            self.saveNewData.clicked.connect(self.submitNewPlayerData)
            self.resetButton.clicked.connect(self.resetDataFields)
            self.pixyshipLayoutButton.clicked.connect(self.pixyshipURL)
            self.submitNewDataButton.clicked.connect(self.open_fightDialog)
            self.actionImport_Data.triggered.connect(self.open_importDialog)
            self.playerBrowserSearchButton.clicked.connect(self.open_playerBrowser)
            self.fleetSearchButton.clicked.connect(self.open_fleetBrowser)
            self.fleetBrowserSearchButton.clicked.connect(self.open_fleetNameBrowser)
            self.delLegendsButton.clicked.connect(lambda: self.deleteSelectedLine("legends", self.legendsTable))
            self.delTournyButton.clicked.connect(lambda: self.deleteSelectedLine("tourny", self.tournyTable))
            self.delPVPButton.clicked.connect(lambda: self.deleteSelectedLine("pvp", self.pvpTable))
            self.actionStars_Calculator.triggered.connect(self.open_tournamentStarsCalc)
            self.actionTrainer.triggered.connect(self.open_crewTrainer)
            self.actionTarget_Tracking.triggered.connect(self.open_stt)
            self.actionExport_Fights.triggered.connect(self.exportFightsToCSV)
            self.actionAbout.triggered.connect(self.openAboutBox)
            self.actionLoadout_Builder.triggered.connect(self.openLoadoutBuilder)
            self.actionDark_Mode.triggered.connect(self.swapStyle)

            self.createNewProfile.clicked.connect(createProfile)
            self.createNewProfile.clicked.connect(self.popProfiles)
            self.deleteSelectedProfile.clicked.connect(self.deleteProfile)
            self.profileComboBox.currentIndexChanged.connect(self.profileChanged)
      def initialize_dialogs(self):
            self.fightDialog = FightDataConfirmation(parent=self)
            self.fightDialog.fightDataSaved.connect(self.receiveFightData)

            self.player_dialog = FilteredListDialog("Player Dialog", "Player Name", "Search Player")
            self.player_dialog.copyItemSearchClicked.connect(self.handleCopyPlayerSearchClicked)
            self.fleet_dialog = FilteredListDialog("Fleet Dialog", "Fleet Name", "Search Fleet")
            self.fleet_dialog.copyItemSearchClicked.connect(self.handleCopyFleetSearchClicked)
            self.fleet_name_dialog = FilteredListDialog("Fleet Name Dialog", "Fleet Name", "Search Fleet Name")
            self.fleet_name_dialog.copyItemSearchClicked.connect(self.handleCopyFleetNameSearchClicked)

            self.importDialog = ImportDialogBox()
            self.trainingDialog = CrewTrainerDialogBox()
            self.profileCreate = ProfileDialog()
            self.starCalculator = StarsCalculatorDialogBox(self.profileComboBox.currentText())
            self.starTargetTrack = StarTargetTrackDialogBox(self.profileComboBox.currentText(), parent=self)
            self.aboutBox = self.AboutInfoDialog(CURRENT_VERSION, CREATOR, SUPPORT_LINK, GITHUB_LINK, API_CALL_COUNT)
            self.crewLoadoutBuilder = CrewLoadoutBuilderDialogBox(parent=self)
      def populate_tables(self):
            self.update_SQL(QSqlQuery(QSqlDatabase.database("tournydb")), "Tourny")
            self.update_SQL(QSqlQuery(QSqlDatabase.database("legendsdb")), "Legend")
            self.update_SQL(QSqlQuery(QSqlDatabase.database("pvpdb")), "PVP")
      def start_blinking_about_menu(self):
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.blinkAboutMenu)
            self.timer.start(500)
            self.color_flag = True
      async def generateAccessToken(self):
            start_time = time.time()
            global ACCESS_TOKEN
            global API_CALL_COUNT
            device_key = get_or_create_uuid()
            client_date_time = pssapi.utils.get_utc_now()
            checksum = self.client.user_service.utils.create_device_login_checksum(device_key, self.client.device_type, client_date_time, "5343")
            API_CALL_COUNT += 1
            user_login = await self.client.user_service.device_login(checksum, client_date_time, device_key, self.client.device_type)
            API_CALL_COUNT += 1
            assert isinstance(user_login, pssapi.entities.UserLogin)
            assert user_login.access_token
            ACCESS_TOKEN = user_login.access_token
            total_time = time.time() - start_time
            log_time(f"Total access token generation time: {total_time:.4f} seconds")
      async def fetch_user_data(self, searchname):
            global API_CALL_COUNT
            start_time = time.time()
            try:
                  responses = await self.client.user_service.search_users(searchname)
                  API_CALL_COUNT += 1
            except Exception:
                  throwErrorMessage(f"API Call Limit {API_CALL_COUNT} has been reached", f"Player: {searchname} was not searched due to API limitation\nPlease wait a few minutes and try again")
                  return
            if not responses:
                  throwErrorMessage("Player Not Found", f"Player: {searchname} was not found")
                  return
            response = responses[0]
            self.fleetName.setPlainText(response.alliance_name)
            try:
                  if(response.alliance > int(self.bestStars.toPlainText())):
                        self.bestStars.setPlainText(str(response.alliance_score))
            except Exception:
                  self.bestStars.setPlainText(str(response.alliance_score))
                  self.lastStars.setPlainText("0")
            self.currentTrophies.setPlainText(str(response.trophy))
            self.maxTrophies.setPlainText(str(response.highest_trophy))
            self.updateFightTables("tourny")
            self.updateFightTables("legends")
            self.updateFightTables("pvp")
            self.submitNewPlayerData()
            total_time = time.time() - start_time
            log_time(f"Fetch user data generation time: {total_time:.4f} seconds")
            await self.fetch_fleetmembers_from_api(response.alliance_name,response.alliance_id)
            API_CALL_COUNT += 1
            timer = time.time() - start_time
            log_time(f"Fetch searched fleet data: {timer:.4f} seconds")
      async def fetch_fleetmembers_from_api(self, fleetname, fleetid):
            global API_CALL_COUNT
            start_time = time.time()
            try:
                  fleet = await self.client.alliance_service.search_alliances(ACCESS_TOKEN,fleetname,0,5)
                  API_CALL_COUNT += 1
                  players = await self.client.alliance_service.list_users(ACCESS_TOKEN,fleetid,0,fleet[0].number_of_members)
                  API_CALL_COUNT += 1
            except:
                  throwErrorMessage(f"API Call Limit {API_CALL_COUNT} has been reached", f"Fleet: {fleetname} was not fully updated")
                  return False
            query = QSqlQuery(QSqlDatabase.database("targetdb"))
            player_data_list = []

            for player in players:
                  pname = player.name
                  fname = player.alliance_name
                  if fname != fleetname:
                        continue
                  laststars = player.alliance_score
                  beststars = 0
                  notes = ""
                  query.prepare("SELECT * FROM players WHERE playername = :pname")
                  query.bindValue(":pname", pname)
                  if query.exec() and query.next():
                        beststars = query.value(3)
                        notes = query.value(4)
                  else:
                        print(f"Query execution failed on {pname} in fleet {fname} [fetch_fleetmembers_from_api]")
                  player_data_list.append([pname, fname, laststars, beststars, notes])
                  print(f"{pname} | {fname} | {laststars} | {beststars} | {notes}")
            if player_data_list:
                  write_to_targets_database_batch(player_data_list)
            total_time = time.time() - start_time
            log_time(f"Fetch fleet members data generation time: {total_time:.4f} seconds")
            return True
      async def main(self):
            await self.fetch_mass_api_call()
      async def fetch_mass_api_call(self):
            return
            '''if not should_make_api_call():
                  print("Call done too recently")
                  return
            #Pull dataset of top 100 fleets
            #Pull players of each fleet
            #write individual player data into targets database
            #fleet_list = await self.client.alliance_service.list_alliances_by_ranking(0,100)
            #for fleet in fleet_list:
                  #current_fleet_members = await self.client.alliance_service.list_users(ACCESS_TOKEN,fleet.alliance_id,0,fleet.number_of_members)                  
                  #for member in current_fleet_members:
                        #print(member.name)
            topplayers = await self.client.ladder_service.list_users_by_ranking(ACCESS_TOKEN,0,100)
            update_last_api_call()
            for player in topplayers:
                  print(f"Adding {player.name} to targets database")
                  self.update_player_via_api(player.name)
      Update top 100 players and names in fleets once per day maximum'''
      def swapStyle(self):
            global CURRENT_STYLESHEET
            if self.actionDark_Mode.isChecked():
                  self.setStyleSheet(DARK_MODE_STYLESHEET)
                  CURRENT_STYLESHEET="dark"
            else:
                  CURRENT_STYLESHEET="default"
                  self.setStyleSheet("")
            tourny = getattr(self, "tournyTable")
            legends = getattr(self, "legendsTable")
            pvp = getattr(self, "pvpTable")
            list = tourny, legends, pvp
            for table_widget in list:
                  table_widget.setColumnWidth(0,35)
                  table_widget.setColumnWidth(1,70)
                  table_widget.setColumnWidth(2,25)
                  table_widget.setColumnWidth(3,40)
            self.importDialog.setStyle()
            self.fightDialog.setStyle()
            self.player_dialog.setStyle()
            self.fleet_dialog.setStyle()
            self.fleet_name_dialog.setStyle()
            self.trainingDialog.setStyle()
            self.profileCreate.setStyle()
            self.starCalculator.setStyle()
            self.starTargetTrack.setStyle()
            self.aboutBox.setStyle()
            self.crewLoadoutBuilder.setStyle()
      def blinkAboutMenu(self):
            if self.color_flag:
                  self.menuAbout.setTitle("Update Available")
            else:
                  self.menuAbout.setTitle("About")
            self.color_flag = not self.color_flag
      def openLoadoutBuilder(self):
            self.crewLoadoutBuilder.setStyle()
            self.crewLoadoutBuilder.exec()
      def update_player_via_api(self, searchname):
            data = self.fetch_user_data(searchname)
      def get_first_of_following_month(self, utc_now):
            year = utc_now.year
            month = utc_now.month + 1
            if (month == 13):
                  year += 1
                  month = 1
            result = datetime(year, month, 1, 0, 0, 0, 0, timezone.utc)
            return result
      def openAboutBox(self):
            self.aboutBox.update_api_calls(API_CALL_COUNT)
            self.aboutBox.exec()
      def profileChanged(self, index):
            profile_name = self.profileComboBox.itemText(index)
            if bool(profile_name.strip()):
                  create_connection(profile_name)
                  create_table()
                  self.resetDataFields()
                  print(f"changing to profile name of [{profile_name}]")
                  self.starCalculator.setProfilePath(profile_name)
                  self.starTargetTrack.setProfilePath(profile_name)
                  modify_SQL()
      def deleteProfile(self):
            current_index = self.profileComboBox.currentIndex()
            old_profile = self.profileComboBox.currentText()
            self.profileComboBox.removeItem(current_index)
            self.profileComboBox.setCurrentIndex(0)
            os.rename(f'_profiles/{old_profile}',f'_oldprofiles/{old_profile}')
            with open('profiles.csv', 'r', newline = '') as infile, \
                  open('profiles.csv.temp', 'w', newline = '') as outfile:
                  reader = csv.reader(infile)
                  writer = csv.writer(outfile)
                  for row in reader:
                        if old_profile not in row:
                              writer.writerow(row)
            os.replace('profiles.csv.temp', 'profiles.csv')
      def popProfiles(self):
            profile_list = getProfiles()
            self.profileComboBox.clear()
            for item in profile_list:
                  self.profileComboBox.addItem(item)
      def update_SQL(self, query, db_name):
            alter_queries = [
                  "ALTER TABLE fights ADD COLUMN hpremain INTEGER DEFAULT 0",
                  "ALTER TABLE fights ADD COLUMN winloss TEXT DEFAULT 'Draw'"
                  ]
            update_query = (
                  "UPDATE fights "
                  "SET hpremain = 0, winloss = 'Draw' "
                  "WHERE hpremain IS NULL OR winloss IS NULL"
                  )
            for alter_query in alter_queries:
                  if not query.exec(alter_query):
                        if not query.lastError().text().startswith("duplicate"):
                              print(f"Error: {db_name} Alter")
                              print("Error:", query.lastError().text())
            if not query.exec(update_query):
                  if not query.lastError().text().startswith("duplicate"):
                        print(f"Error: {db_name} Update")
                        print("Error:", query.lastError().text())
      def open_fightDialog(self):
            self.fightDialog.exec()
      def open_playerBrowser(self):
            self.player_dialog.populateList("SELECT playername FROM players", None)
            self.player_dialog.exec()
      def open_fleetBrowser(self):
            self.fleet_dialog.populateList("SELECT playername FROM players WHERE fleetname = :fleet_name", self.fleetName.toPlainText())
            self.fleet_dialog.exec()
      def open_fleetNameBrowser(self):
            self.fleet_name_dialog.populateList("SELECT fleetname FROM players", None)
            self.fleet_name_dialog.exec()
      def open_importDialog(self):
            self.importDialog.importDialogLabel.setText("")
            self.importDialog.importFilenameBox.setPlainText("")
            self.importDialog.exec()
      def open_tournamentStarsCalc(self):
            self.starCalculator.exec()
      def open_crewTrainer(self):
            self.trainingDialog.exec()
      def open_stt(self):
            self.starTargetTrack.populateSTT(self.playerNameSearchBox.toPlainText())
            self.starTargetTrack.exec()
      def exportFightsToCSV(self):
            filepath = os.path.join('exportedfights.csv')
            fights_data = []
            for db_name in ("tournydb", "legendsdb", "pvpdb"):
                  db = QSqlDatabase.database(db_name)
                  query = QSqlQuery(db)
                  query.prepare("SELECT name, rewards, datetag, hpremain, winloss FROM fights ORDER BY name")
                  if not query.exec():
                        throwErrorMessage("Query execution failed [exportFightsToCSV]: ", query.lastError().text())
                        return
                  while query.next():
                        name = query.value(0)
                        rewards = query.value(1)
                        datetag = query.value(2)
                        hpremain = query.value(3)
                        winloss = query.value(4)
                        fights_data.append((db_name, name, rewards, datetag, hpremain, winloss))

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                  writer = csv.writer(csvfile)
                  writer.writerow(["Database", "Name", "Rewards", "Datetag", "HP Remaining", "Win/Loss"])
                  for row in fights_data:
                        writer.writerow(row)
            self.exportPlayerDataToCSV()
      def exportPlayerDataToCSV(self):
            filepath = os.path.join('exportedplayers.csv')
            player_data = []
            db = QSqlDatabase.database("targetdb")
            query = QSqlQuery(db)
            query.prepare("SELECT playername, fleetname, laststars, beststars, notes FROM players ORDER BY playername")
            if not query.exec():
                  throwErrorMessage("Query Execution failed [exportPlayerDataToCSV]: ", query.lastError().text())
                  return
            while query.next():
                  playername = query.value(0)
                  fleetname = query.value(1)
                  laststars = query.value(2)
                  beststars = query.value(3)
                  notes = query.value(4)
                  player_data.append((playername, fleetname, laststars, beststars, notes))
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                  writer = csv.writer(csvfile)
                  writer.writerow(["Player Name", "Fleet Name", "Last Stars", "Best Stars", "Notes"])
                  for row in player_data:
                        writer.writerow(row)
            throwErrorMessage("Data Export", "Export complete to exportedfights.csv and exportedplayers.csv")
      def handleCopyFleetSearchClicked(self, selected_text, close_dialog):
            self.resetDataFields()
            self.playerNameSearchBox.setPlainText(selected_text)
            self.searchPlayer()
            if close_dialog:
                  self.fleet_dialog.accept()
      def handleCopyFleetNameSearchClicked(self, selected_text, close_dialog):
            self.resetDataFields()
            self.fleetName.setPlainText(selected_text)
            if close_dialog:
                  self.fleet_name_dialog.accept()
      def handleCopyPlayerSearchClicked(self, selected_text, close_dialog):
            self.resetDataFields()
            self.playerNameSearchBox.setPlainText(selected_text)
            self.searchPlayer()
            if close_dialog:
                  self.player_dialog.accept()
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
                        self.playerNotes.setPlainText(query.value(4))
                        self.updateFightTables("tourny")
                        self.updateFightTables("legends")
                        self.updateFightTables("pvp")
                  else:
                        asyncio.run(self.fetch_user_data(text))
                        self.updateFightTables("tourny")
                        self.updateFightTables("legends")
                        self.updateFightTables("pvp")
                        return
            else:
                  throwErrorMessage("Query execution failed [searchPlayer]: ", query.lastError().text())
                  return
            asyncio.run(self.fetch_user_data(text))
            self.updateFightTables("tourny")
            self.updateFightTables("legends")
            self.updateFightTables("pvp")
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
            player_data = [self.playerNameSearchBox.toPlainText(), self.fleetName.toPlainText(), last_stars, best_stars, self.playerNotes.toPlainText()]
            if write_to_targets_database(player_data):
                  player_data.clear()
            else:
                  throwErrorMessage("targetdb: Error writing data to the database - Dumping data [submitNewPlayerData]", player_data)
      def updateFightTables(self, fights):
            name = self.playerNameSearchBox.toPlainText()
            query_error_message = f"{fights.capitalize()}DB Update: "

            if fights in ("tourny", "legends", "pvp"):
                  db_name = f"{fights}db"
                  table_widget = getattr(self, f"{fights}Table")
                  query = QSqlQuery(QSqlDatabase.database(db_name))
                  query.prepare("SELECT rewards, datetag, hpremain, winloss FROM fights WHERE name LIKE ?")
                  if query.lastError().isValid():
                        throwErrorMessage(f"{query_error_message} [updateFightTables]", query.lastError().text())
                        sys.exit(-1)
                  query.addBindValue(f'%{name}%')
                  query.exec()

                  model = self.CustomSqlTableModel()
                  model.setQuery(query)
                  table_widget.setModel(model)
                  if CURRENT_STYLESHEET == "default":
                        table_widget.setStyleSheet("")
                  elif CURRENT_STYLESHEET == "dark":
                        table_widget.setStyleSheet(DARK_MODE_STYLESHEET)
                  table_widget.setColumnWidth(0,35)
                  table_widget.setColumnWidth(1,70)
                  table_widget.setColumnWidth(2,25)
                  table_widget.setColumnWidth(3,40)
                  table_widget.show()
            else:
                  throwErrorMessage("Fights Table Error [updateFightTables]", "Invalid fights type")
      def receiveFightData(self, rewards, remainhp, result, fight):
            self.submitFightData(rewards, remainhp, result, fight)
      def submitFightData(self, rewards, remainhp, result, fight):
            todaysdate = str(date.today())
            fight_data = [self.playerNameSearchBox.toPlainText(), str(rewards), todaysdate, str(remainhp), result]
            if not write_to_fights_database(fight_data, fight):
                  print(fight_data, " | ", fight)
                  throwErrorMessage("FightsDB: Error writing data to the database - Dumping data [submitFightData]", fight_data)
            getattr(self, f"{fight}Table").clearSpans()
            self.updateFightTables(fight) 
            fight_data.clear()
      def deleteSelectedLine(self, table_name, tableView):
            selected_indexes = tableView.selectionModel().selectedRows()
            db = QSqlDatabase.database(f"{table_name}db")
            if not selected_indexes:
                  return

            name_data = []
            rewards_data = []
            datetag_data = []
            hpremain_data = []
            winloss_data = []

            for index in selected_indexes:
                  rewards = tableView.model().index(index.row(), 0).data()
                  datetag = tableView.model().index(index.row(), 1).data()
                  hpremain = tableView.model().index(index.row(), 2).data()
                  winloss = tableView.model().index(index.row(), 3).data()
                  rewards_data.append(rewards)
                  datetag_data.append(datetag)
                  hpremain_data.append(hpremain)
                  winloss_data.append(winloss)

            name_data.append(self.playerNameSearchBox.toPlainText())

            query = QSqlQuery(db)
            sql_query = "DELETE FROM fights WHERE name IN ({}) AND rewards IN ({}) AND datetag IN ({}) AND hpremain IN ({}) AND winloss IN ({})".format(
                  ", ".join(["'{}'".format(str(name)) for name in name_data]),  
                  ", ".join(["'{}'".format(str(data)) for data in rewards_data]),
                  ", ".join(["'{}'".format(str(data)) for data in datetag_data]),
                  ", ".join(["'{}'".format(float(data)) for data in hpremain_data]),
                  ", ".join(["'{}'".format(str(data)) for data in winloss_data]))

            if not query.exec(sql_query):
                  throwErrorMessage("Record Deletion Error : [deleteSelectedLine]["+table_name+"]", query.lastError().text())
                  return

            tableView.model().clear()
            self.updateFightTables(table_name)
      class CustomSqlTableModel(QSqlTableModel):
            def __init__(self, parent=None):
                  super().__init__(parent)
            def setStyle(self):
                  if CURRENT_STYLESHEET == "default":
                        self.setStyleSheet("")
                  elif CURRENT_STYLESHEET == "dark":
                        self.setStyleSheet(DARK_MODE_STYLESHEET)
                  self.setColumnWidth(0,35)
                  self.setColumnWidth(1,70)
                  self.setColumnWidth(2,25)
                  self.setColumnWidth(3,40)
            def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
                  if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
                        headers = {
                              0: "★/🏆",
                              1: "Date",
                              2: "HP",
                              3: "W/L/D"
                              }
                        return headers.get(section, super().headerData(section, orientation, role))
                  return super().headerData(section, orientation, role)
            def data(self, index, role):
                  if not index.isValid():
                        return None
                  if role == Qt.ItemDataRole.BackgroundRole:
                        column_name = "datetag"
                        datetag_value = self.record(index.row()).value(column_name)
                        datetag_date = datetime.strptime(datetag_value, "%Y-%m-%d")
                        last_day_of_month = datetime(datetag_date.year, datetag_date.month, 1) + timedelta(days=32)
                        last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
                        if (last_day_of_month - datetag_date).days <= 7:
                              return QColor(181,214,232)
                  return super().data(index, role)
      class AboutInfoDialog(QDialog):
            def __init__(self, version, creator, support_link, github_link, api_calls, parent=None):
                  global GITHUB_RELEASE_VERSION
                  global NEW_RELEASE
                  super().__init__(parent)
                  self.setWindowTitle("Information")
                  layout = QVBoxLayout()

                  response = requests.get(GITHUB_RELEASE_LINK)
                  commit_response = requests.get("https://api.github.com/repos/arraken/pss-ttt/commits")
                  commit_version = commit_response.json()[0]['commit']['message']
                  if response.status_code == 200:
                        release_info = response.json()
                        commit_release = commit_response.json()
                        latest_version = release_info['tag_name']
                        GITHUB_RELEASE_VERSION = latest_version
                        commit_version = commit_release[0]['commit']['message']
                  print(f"Current version {version} - Dev version {commit_version} - Release version {latest_version}")
                  version_label = QLabel(f"Current Version: {version} - Release version: {latest_version} - Dev version: {commit_version}")
                  if latest_version > version:
                        print("Converting to new release")
                        NEW_RELEASE = True
                  creator_label = QLabel(f"Creator: {creator}")
                  support_label = QLabel(f"Support Link: {support_link}")
                  github_label = QLabel(f"Github Link: {github_link}")
                  self.api_calls_label = QLabel(f"API Calls: {api_calls}")

                  layout.addWidget(version_label)
                  layout.addWidget(creator_label)
                  layout.addWidget(support_label)
                  layout.addWidget(github_label)
                  layout.addWidget(self.api_calls_label)

                  ok_button = QPushButton("OK")
                  ok_button.clicked.connect(self.accept)
                  layout.addWidget(ok_button)

                  self.setLayout(layout)
            def update_api_calls(self, api_calls):
                  self.api_calls_label.setText(f"API Calls: {api_calls}")
            def setStyle(self):
                  if CURRENT_STYLESHEET == "default":
                        self.setStyleSheet("")
                  elif CURRENT_STYLESHEET == "dark":
                        self.setStyleSheet(DARK_MODE_STYLESHEET)
class FilteredListDialog(QtWidgets.QDialog):
      global CURRENT_STYLESHEET
      copyItemSearchClicked = QtCore.pyqtSignal(str, bool)
      def __init__(self, title, filter_label, filter_placeholder, parent=None):
            super().__init__(parent)
            uic.loadUi(os.path.join('_internal', '_ui', 'pss-ttt-fld.ui'), self)
            self.setWindowTitle(title)

            self.itemSearchClose.clicked.connect(self.accept)
            self.copyItemSearch.clicked.connect(self.onCopyItemSearchClicked)
            self.filterBox.textChanged.connect(self.filterList)
            self.charLimiter.valueChanged.connect(self.filterListLength)
            self.charLimiterCheckBox.stateChanged.connect(self.filterListLength)

            self.filterLabel.setText(filter_label)
            self.filterBox.setPlaceholderText(filter_placeholder)
      def populateList(self, query_string, query_args):
            self.itemList.clear()
            if not QSqlDatabase.database("targetdb").isOpen():
                  if not QSqlDatabase.database("targetdb").open():
                        throwErrorMessage("Database Connection Failure [populateList]", "Targets DB did not open properly")
                        return
            
            query = QSqlQuery(QSqlDatabase.database("targetdb"))
            query.prepare(query_string)
            if query_args:
                  query.bindValue(":fleet_name", query_args)

            if not query.exec():
                  throwErrorMessage("Query Execution Failure [populateList]", query.lastError().text())
                  return
            fleet_names = set()
            while query.next():
                  item_text = query.value(0)
                  if item_text not in fleet_names:
                        fleet_names.add(item_text)
                        item = QListWidgetItem(item_text)
                        self.itemList.addItem(item)
      def onCopyItemSearchClicked(self):
            selected_item = self.itemList.currentItem()
            if selected_item:
                  selected_text = selected_item.text()
                  self.copyItemSearchClicked.emit(selected_text, True)
      def setStyle(self):
            if CURRENT_STYLESHEET == "default":
                  self.setStyleSheet("")
            elif CURRENT_STYLESHEET == "dark":
                  self.setStyleSheet(DARK_MODE_STYLESHEET)
      def filterList(self):
            filter_text = self.filterBox.toPlainText().lower()
            for i in range(self.itemList.count()):
                  item = self.itemList.item(i)
                  item_text = item.text().lower()
                  if filter_text in item_text:
                        item.setHidden(False)
                  else:
                        item.setHidden(True)
      def filterListLength(self):
            if self.charLimiterCheckBox.isChecked():
                  length_threshold = self.charLimiter.value()
                  for i in range(self.itemList.count()):
                        item = self.itemList.item(i)
                        item_text = item.text()
                        if len(item_text) == length_threshold:
                              item.setHidden(False)
                        else:
                              item.setHidden(True)
class FightDataConfirmation(QtWidgets.QDialog):
      global CURRENT_STYLESHEET
      fightDataSaved = pyqtSignal(int, float, str, str)
      def __init__(self, parent=None):
            super().__init__(parent)
            uic.loadUi(os.path.join('_internal','_ui','pss-ttt-fdb.ui'), self)

            self.submitFightDataButton.clicked.connect(self.saveFightData)
      def setStyle(self):
            if CURRENT_STYLESHEET == "default":
                  self.setStyleSheet("")
            elif CURRENT_STYLESHEET == "dark":
                  self.setStyleSheet(DARK_MODE_STYLESHEET)
      def saveFightData(self):
            rewards = int(self.fightRewardBox.toPlainText())
            remainhp = float(self.fightHPBox.toPlainText())
            result = str(self.fightResultBox.currentText())
            fight = str(self.fightTypeBox.currentText())
            self.fightDataSaved.emit(rewards, remainhp, result, fight)
            self.accept()
class ImportDialogBox(QtWidgets.QDialog):
      global CURRENT_STYLESHEET
      progress_signal = pyqtSignal(int)
      updated_records = []
      has_imported = False
      counter = 0
      max_counter = 0
      def __init__(self):
            super().__init__()
            uic.loadUi(os.path.join('_internal','_ui','pss-ttt-importdialog.ui'), self)
            self.importTargetsButton.clicked.connect(self.import_data)
            self.importBrowse.clicked.connect(self.open_fileBrowser)
            self.importSeeChanges.clicked.connect(self.printChangesList)

            self.progress_signal.connect(self.updateProgressBar, QtCore.Qt.ConnectionType.DirectConnection)
      def setStyle(self):
            if CURRENT_STYLESHEET == "default":
                  self.setStyleSheet("")
            elif CURRENT_STYLESHEET == "dark":
                  self.setStyleSheet(DARK_MODE_STYLESHEET)
      def closeEvent(self, event):
            self.has_imported = False
            super().closeEvent(event)
      def printChangesList(self):
            header = ["Player Name", "Fleet Name", "Last Stars", "Best Stars", "Notes"]

            with open(os.path.join('_internal', 'importedChanges.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                  writer = csv.writer(csvfile)
                  writer.writerow(header)
                  for record in self.updated_records:
                        writer.writerow(record)
      def open_fileBrowser(self):
            options = QFileDialog.Option.DontUseNativeDialog
            selected_files, _ = QFileDialog.getOpenFileNames(self, "Select File", "", "All Files (*)", options=options)
            for file_path in selected_files:
                  self.importFilenameBox.appendPlainText(file_path)
      def import_data(self):
            self.importDialogLabel.setText("Data importing has begun.<br>Please note the application may appear to freeze<br>It is not frozen and just processing in the background<br>This will update once finished")
            QApplication.processEvents()
            file_path = self.importFilenameBox.toPlainText().strip()
            self.updated_records = []
            
            if not file_path:
                  throwErrorMessage("Import Error", "No file provided or name is incorrect")
                  return
            if file_path.lower().endswith('.csv'):
                  self.max_counter = total_targets_imported = self.importCSV(file_path)
                  file_type = "CSV"
            else:
                  throwErrorMessage("Unsupported file format", "Only able to accept manicured csv (/pasttfleets) from Dolores 2.0 bot")
                  return
            self.importDialogLabel.setText(f"Total Targets Import ({file_type}): {total_targets_imported} targets")
            for i in range(self.max_counter):
                  self.progress_signal.emit(self.counter)
            self.has_imported = True
      def updateProgressBar(self, value):
            self.importProgressBar.setValue(int((value / self.max_counter) * 100))
      def importCSV(self, file_path):
            data_to_insert = []
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                  reader = csv.reader(csvfile, delimiter=';')
                  next(reader)
                  for row in reader:
                        playername, fleetname, laststars, beststars, notes = row[2], row[1], row[7], row[7], ' '
                        beststars_int = int(beststars)
                        notes_str = notes
            
                        db = QSqlDatabase.database("targetdb")
                        query = QSqlQuery(db)
                        query.prepare("SELECT beststars, notes FROM players WHERE playername = ? AND fleetname = ?")
                        query.addBindValue(playername)
                        query.addBindValue(fleetname)
                        query.exec()
                        if query.next():
                              beststars_db = int(query.value(0))
                              notes_db = str(query.value(1))
                              if beststars_int < beststars_db:
                                    beststars_int = beststars_db
                              if notes_db != ' ':
                                    notes_str = notes_db
                              if beststars_int != int(row[7]) or notes_str != row[6]:
                                    self.updated_records.append((f"NEW-{playername}", fleetname, laststars, beststars_int, notes_str))
                                    self.updated_records.append((f"OLD-{playername}", fleetname, laststars, int(row[7]), row[6]))
                        data_to_insert.append((playername, fleetname, laststars, beststars_int, notes_str))
            db = QSqlDatabase.database("targetdb")
            if not db.open():
                  throwErrorMessage("Targets Database Error", "Unable to open targets database for import")
                  return self.counter
    
            query = QSqlQuery(db)
            query.exec("CREATE TABLE IF NOT EXISTS players (playername TEXT PRIMARY KEY, fleetname TEXT NOT NULL, laststars TEXT NOT NULL, beststars TEXT NOT NULL, notes TEXT NOT NULL)")
    
            self.max_counter = len(data_to_insert)
            for specific_data in data_to_insert:
                  playername, fleetname, laststars, beststars, notes = specific_data
                  count_query = QSqlQuery(db)
                  count_query.prepare("SELECT COUNT(*) FROM players WHERE playername = ? AND fleetname = ?")
                  count_query.addBindValue(playername)
                  count_query.addBindValue(fleetname)
                  count_query.exec()
                  count_query.next()
                  count = count_query.value(0)
                  
                  query.prepare("INSERT OR REPLACE INTO players (playername, fleetname, laststars, beststars, notes) VALUES (?, ?, ?, ?, ?)")
                  query.addBindValue(playername)
                  query.addBindValue(fleetname)
                  query.addBindValue(laststars)
                  query.addBindValue(beststars)
                  query.addBindValue(notes)
        
                  if query.exec():
                        self.counter += 1
                        self.progress_signal.emit(self.counter)
                  else:
                        throwErrorMessage("Database Error", query.lastError().text())
            db.commit()
            return self.counter
class StarsCalculatorDialogBox(QtWidgets.QDialog):
      global CURRENT_STYLESHEET
      def __init__(self, profile_name):
            super().__init__()
            uic.loadUi(os.path.join('_internal','_ui','pss-ttt-tsc.ui'), self)
            
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
            self.tournamentTable = self.findChild(QTableView, "starsTableView")
            self.model = self.StarsTableModel(self.starsTable, self)
            self.tournamentTable.setModel(self.model)
            for i in range(7):
                  self.tournamentTable.setColumnWidth(i,50)
            self.calculateStars.clicked.connect(self.calculateStarsGoal)     
            self.resetStarsTableButton.clicked.connect(self.resetStarsTable)
            self.profile_path = profile_name
            self.loadStarsTableFromCSV()
      def setProfilePath(self, profile_name):
            self.profile_path = profile_name
      def getStarsFilePath(self):
            file_path = os.path.join('_profiles', self.profile_path, 'starstable.csv')
            return file_path
      def closeEvent(self, event):
            self.saveStarsTableToCSV()
            print("Saving Data")
            super().closeEvent(event)
      def updateActualStarsBox(self):
            total_sum = sum(self.model.getCellValue(7, col) for col in range(self.model.columnCount(None)))
            self.actualStarsBox.setPlainText(str(total_sum))
            self.saveStarsTableToCSV()
      def setStyle(self):
            if CURRENT_STYLESHEET == "default":
                  self.setStyleSheet("")
            elif CURRENT_STYLESHEET == "dark":
                  self.setStyleSheet(DARK_MODE_STYLESHEET)
            for i in range(7):
                  self.tournamentTable.setColumnWidth(i,50)
      def saveStarsTableToCSV(self):
            file_path = self.getStarsFilePath()
            try:
                  with open(file_path, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerows(self.starsTable)
            except Exception as e:
                  print(f"Error saving data to CSV: {e}")
      def loadStarsTableFromCSV(self):
            file_path = self.getStarsFilePath()
            if os.path.exists(file_path):
                  try:
                        with open(file_path, 'r', newline='') as csvfile:
                              reader = csv.reader(csvfile)
                              self.starsTable = [list(map(int, row)) for row in reader]
                              self.model._data = self.starsTable
                              self.model.layoutChanged.emit()
                  except Exception as e:
                        print(f"Error loading data from CSV: {e}")
                        self.initializeStarsTable()
            else:
                  print(f"File not found: {file_path}. Initializing with default values.")
                  self.initializeStarsTable()
      def initializeStarsTable(self):
            self.starsTable = [
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
            ]
            self.model._data = self.starsTable
            self.model.layoutChanged.emit()
            self.saveStarsTableToCSV()
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
            self.model._data = self.starsTable
            self.model.layoutChanged.emit()
            self.saveStarsTableToCSV()
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
      class StarsTableModel(QAbstractTableModel):
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
                        try:
                              int_value = int(value)
                              self._data[index.row()][index.column()] = int_value
                              self.parent.starsTable[index.row()][index.column()] = int_value
                        except ValueError:
                              self._data[index.row()][index.column()] = 0
                              self.parent.starsTable[index.row()][index.column()] = 0
                        self.dataChanged.emit(index, index)
                        for col in range(self.columnCount(None)):
                              try:
                                    self._data[7][col] = sum(int(self._data[i][col]) for i in range(1,7))
                                    self.parent.starsTable[7][col] = self._data[7][col]
                              except ValueError:
                                    self._data[7][col] = 0
                                    self.parent.starsTable[7][col] = 0
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
                        self.estStarsBox.setPlainText(str(end_value))
            self.tournamentTable.show()
            self.saveStarsTableToCSV()
class CrewTrainerDialogBox(QtWidgets.QDialog):
      global CURRENT_STYLESHEET
      def __init__(self):
            super().__init__()
            uic.loadUi(os.path.join('_internal','_ui','pss-ttt-crewtrainer.ui'), self)

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
            self.chartTable = self.findChild(QTableView, "trainingChartTable")
            self.chartModel = self.TrainingChartTableModel(self.trainingChart, self.trainingStatBox)
            self.trainingStatBox = self.findChild(QtWidgets.QComboBox, "trainingStatBox")
            self.statsTable.setModel(self.model)
            self.setStyle()
            self.statsTable.setColumnWidth(0,50)
            self.statsTable.setColumnWidth(1,90)
            self.statsTable.setColumnWidth(2,90)
            self.chartTable.setModel(self.chartModel)
            self.trainingPointsBox.currentIndexChanged.connect(self.onComboBoxValueChanged)
            self.trainingStatBox.currentIndexChanged.connect(self.onComboBoxValueChanged)
            self.mergeTierBox.currentIndexChanged.connect(self.mergedMaxTP)
            self.fatigueBox.currentIndexChanged.connect(self.onComboBoxValueChanged)

            self.presetsDialog = self.CrewTrainerPresetDialog(self.crewStats, parent=self)

            self.openPresetsButton.clicked.connect(self.open_presetWindow)

            self.model.dataChanged.connect(self.checkSumValidity)
            
            for i in range(10):
                  if i == 0:
                        self.chartTable.setColumnWidth(i,125)
                  else:
                        self.chartTable.setColumnWidth(i,1)
            self.testPushButton.clicked.connect(self.wipeCrewStats)
            self.onComboBoxValueChanged()
      def setStyle(self):
            if CURRENT_STYLESHEET == "default":
                  self.setStyleSheet("")
                  self.chartTable.setStyleSheet("")
                  self.statsTable.setStyleSheet("")
            elif CURRENT_STYLESHEET == "dark":
                  self.setStyleSheet(DARK_MODE_STYLESHEET)
                  self.chartTable.setStyleSheet(DARK_MODE_STYLESHEET)
                  self.statsTable.setStyleSheet(DARK_MODE_STYLESHEET)
            self.statsTable.setColumnWidth(0,50)
            self.statsTable.setColumnWidth(1,90)
            self.statsTable.setColumnWidth(2,90)
            for i in range(10):
                  if i == 0:
                        self.chartTable.setColumnWidth(i,125)
                  else:
                        self.chartTable.setColumnWidth(i,1)
      def checkSumValidity(self):
            sum_of_values = sum(row[0] for row in self.crewStats)
            max_TP = self.mergedMaxTP()
            if sum_of_values > max_TP:
                  message = f"Sum of training values is above maximum TP ({max_TP}) for this crew."
                  QMessageBox.warning(self, "Warning", message)
            self.TPLabel.setText(f"Current TP total [{sum_of_values}]")
      def open_presetWindow(self):
            self.presetsDialog.exec()
      def calculateTrainingChart(self):
            selected_item = self.trainingStatBox.currentText()
            selected_key = selected_item[:3]
            selected_data_list = [(name, data) for key, name, data in self.trainingList if key.startswith(selected_key)]
            self.model = self.TrainingChartTableModel(selected_data_list, self.trainingStatBox)
            self.chartTable.setModel(self.model)
      def mergedMaxTP(self):
            merge_tier = self.mergeTierBox.currentText()
            maxTP = int(self.trainingPointsBox.currentText())
            if merge_tier == "Gold":
                  maxTP += 10
            elif merge_tier == "Silver":
                  maxTP += 10
            elif merge_tier == "Bronze":
                  maxTP += 6
            self.maxTPLabel.setText(f"Max TP [{maxTP}]")
            return maxTP
      def updateFatigueMod(self):
            max_training_points = self.mergedMaxTP()
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
            stat_names = [('hp', 1), ('atk', 1), ('abl', 1), ('sta', 1), ('rpr', 1), ('plt', 1), ('sci', 1), ('eng', 1), ('wpn', 1)]
            for i, (stat_name, _) in enumerate(stat_names):
                  crew_stat_value = self.crewStats[i][0]
                  crew_stats_m[stat_name] = float(fatigue_m) * (1 - (total_tp / max_training_points)) * (1 - (float(crew_stat_value) / max_training_points))
            for i, (stat_name, _) in enumerate(stat_names):
                  self.crewStats[i][1] = round(crew_stats_m[stat_name],3)
            self.statsTable.viewport().update()
            return
      def modifyTrainingMethods(self):
            selected_training_stat = self.trainingStatBox.currentText()
            modified_data_list = []
            header_labels = self.getHeaderLabels(self.chartTable)
            default_limits = {}
            
            for item in self.trainingList:
                  key, name, data = item[0], item[1], item[2]
                  if key.startswith(selected_training_stat[:3]):
                        modified_data_list.append((name, key, data))

            self.resetTrainingData()
            if selected_training_stat == "RPR":
                  default_limits = {6: 4, 5: 2, 4: 1}
            else:
                  default_limits = {9: 4, 8: 2, 7: 1}

            num_rows = 7 if selected_training_stat == "RPR" else 10
            for i in range(num_rows):
                  for j in range(9):
                        modified_data_list[i][2][j] *= self.crewStats[j][1]
                        modified_data_list[i][2][j] = math.floor(modified_data_list[i][2][j])
                        if i in default_limits and modified_data_list[i][2][j] <= default_limits[i]:
                              if selected_training_stat == header_labels[j+1]:
                                    modified_data_list[i][2][j] = default_limits[i]
      def getHeaderLabels(self, tableView):
            model = tableView.model()
            if model is None:
                  print("No model set for the table view.")
                  return []
            header_labels = []
            for column in range(model.columnCount(0)):
                  header_label = model.headerData(column, Qt.Orientation.Horizontal)
                  header_labels.append(header_label)
            return header_labels
      def onComboBoxValueChanged(self):
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
            self.statsTable.viewport().update()
            sum_of_values = sum(row[0] for row in self.crewStats)
            self.TPLabel.setText(f"Current TP total [{sum_of_values}]")
            self.onComboBoxValueChanged()
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
                  return 1
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
      class TrainingChartTableModel(QAbstractTableModel):
            def __init__(self, data, trainingStatBox, parent=None):
                  super().__init__(parent)
                  self._data = data
                  self.trainingStatBox = trainingStatBox
                  self.horizontalHeaders = ['Training', 'HP','ATK','ABL','STA','RPR','PLT','SCI','ENG','WPN']
                  self.verticalHeaders = [''] * len(data)
            def setStyle(self):
                  if CURRENT_STYLESHEET == "default":
                        self.setStyleSheet("")
                  elif CURRENT_STYLESHEET == "dark":
                        self.setStyleSheet(DARK_MODE_STYLESHEET)
            def rowCount(self, index):
                  return len(self._data)
            def columnCount(self, index):
                  return len(self.horizontalHeaders)
            def data(self, index, role=Qt.ItemDataRole.DisplayRole):
                  if role == Qt.ItemDataRole.DisplayRole:
                        row = index.row()
                        col = index.column()
                        if col == 0:
                              return self._data[row][0]
                        elif 0 < col <= len(self.horizontalHeaders) - 1:
                              item_data = self._data[row][1]
                              if isinstance(item_data, str):
                                    return ""
                              else:
                                    return item_data[col - 1]
                  elif role == Qt.ItemDataRole.BackgroundRole:
                        value = self.data(index, Qt.ItemDataRole.DisplayRole)
                        col = index.column()
                        if CURRENT_STYLESHEET=="dark":
                              if value == 0:
                                    return QColor(76,175,80)
                              elif self.trainingStatBox.currentText() == self.horizontalHeaders[col]:
                                    return QColor(25,118,210)
                              else:
                                    return QColor(51,51,51)
                        elif CURRENT_STYLESHEET=="default":
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
      class CrewTrainerPresetDialog(QtWidgets.QDialog):
            def __init__(self, crewStats, parent=None):
                  super().__init__(parent)
                  uic.loadUi(os.path.join('_internal','_ui','pss-ttt-ctp.ui'), self)
                  self.crewStats = crewStats
                  self.savePresetButton.clicked.connect(self.savePresetData)
                  self.loadPresetButton.clicked.connect(self.loadPresetData)
                  self.deletePresetButton.clicked.connect(self.deleteSelectedPreset)

                  self.model = QStandardItemModel()
                  self.presetTableView.setModel(self.model)
                  self.model.setHorizontalHeaderLabels(['Crew Name', 'HP','ATK','ABL','STA','RPR','PLT','SCI','ENG','WPN'])
                  for i in range(self.model.columnCount()):
                        if i==0:
                              self.presetTableView.setColumnWidth(i,100)
                        else:
                              self.presetTableView.setColumnWidth(i,20)
                  self.loadPresetCSV()
            def loadPresetData(self):
                  selected_row = self.presetTableView.currentIndex().row()
                  if selected_row != -1:
                        for i in range(1, self.model.columnCount()):
                              data = self.model.index(selected_row, i).data()
                              self.crewStats[i - 1][0] = data
                              self.crewStats[i - 1][1] = 1.0
                  self.accept()
                  self.parent().updateFatigueMod()
            def savePresetData(self):
                  first_column_data = [row[0] for row in self.crewStats]
                  preset_name = self.presetCrewNameBox.toPlainText()

                  row_count = self.model.rowCount()
                  self.model.insertRow(row_count)
                  self.model.setData(self.model.index(row_count, 0), preset_name)
                  for i, data in enumerate(first_column_data):
                        self.model.setData(self.model.index(row_count, i + 1), data)
                  for i in range(self.model.columnCount()):
                        if i==0:
                              self.presetTableView.setColumnWidth(i,100)
                        else:
                              self.presetTableView.setColumnWidth(i,20)
                  self.savePresetCSV()
            def savePresetCSV(self):
                  with open(os.path.join('_internal','_crew','trainingpresets.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        for i in range(self.model.rowCount()):
                              row_data = []
                              for j in range(self.model.columnCount()):
                                    data = self.model.index(i, j).data()
                                    row_data.append(data)
                              writer.writerow(row_data)
            def loadPresetCSV(self):
                  os.makedirs(os.path.join('_internal','_crew'),exist_ok=True)
                  filename = os.path.join('_internal','_crew','trainingpresets.csv')
                  if os.path.exists(filename):
                        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                              reader = csv.reader(csvfile)
                              self.model.removeRows(0, self.model.rowCount())
                              for row in reader:
                                    row_position = self.model.rowCount()
                                    self.model.insertRow(row_position)
                                    for column, value in enumerate(row):
                                          item = QtGui.QStandardItem(value)
                                          self.model.setItem(row_position, column, item)
                  else:
                        self.savePresetCSV()
            def deleteSelectedPreset(self):
                  selected_index = self.presetTableView.selectionModel().selectedRows()
                  for index in sorted(selected_index, reverse=True):
                        self.model.removeRow(index.row())
                  self.savePresetCSV()
class StarTargetTrackDialogBox(QtWidgets.QDialog):
      global CURRENT_STYLESHEET
      copyStarsTargetTrackClicked = QtCore.pyqtSignal(str, bool)
      currentStarsTarget = ' '
      global API_CALL_COUNT
      def __init__(self, profile_name, parent=None):
            super().__init__(parent)
            self.client = PssApiClient()
            uic.loadUi(os.path.join('_internal','_ui','pss-ttt-stt.ui'), self)

            self.table_widgets = {
            "dayFour": {"button_add": self.dayFourAdd, "button_remove": self.dayFourRemove, "model": QtGui.QStandardItemModel()},
            "dayFive": {"button_add": self.dayFiveAdd, "button_remove": self.dayFiveRemove, "model": QtGui.QStandardItemModel()},
            "daySix": {"button_add": self.daySixAdd, "button_remove": self.daySixRemove, "model": QtGui.QStandardItemModel()},
            "daySeven": {"button_add": self.daySevenAdd, "button_remove": self.daySevenRemove, "model": QtGui.QStandardItemModel()}
            }

            for day, widgets in self.table_widgets.items():
                  table = getattr(self, f"{day}Table")
                  widgets["model"].setHorizontalHeaderLabels(['Player Name', 'Fleet Name', 'Stars', 'Max Trophy'])
                  table.setModel(widgets["model"])
                  widgets["button_add"].clicked.connect(lambda _, day=day: self.addToTargetTable(day))
                  widgets["button_remove"].clicked.connect(lambda _, day=day: self.removeTargetTable(day))
            self.trackerResetButton.clicked.connect(self.resetStarsTargetList)
            for day in ["dayFour", "dayFive", "daySix", "daySeven"]:
                        getattr(self, f"{day}Copy").clicked.connect(lambda _, day=day: self.copyDayToSearchBox(day))
            self.profile_path = profile_name
            self.loadStarsCSV()
      def setProfilePath(self, profile_name):
            self.profile_path = profile_name
      def setStyle(self):
            if CURRENT_STYLESHEET == "default":
                  self.setStyleSheet("")
            elif CURRENT_STYLESHEET == "dark":
                  self.setStyleSheet(DARK_MODE_STYLESHEET)
      def getStarsFilePath(self):
            return os.path.join('_profiles', self.profile_path, 'starstrack.csv')
      def copyDayToSearchBox(self, day):
            table = getattr(self, f"{day}Table")
            selected_indexes = table.selectionModel().selectedRows()
            if not selected_indexes:
                  throwErrorMessage("No row selected", "Please select a row")
                  return

            selected_row = selected_indexes[0].row()            
            player_name = table.model().index(selected_row, 0).data()
            parent_widget = self.parent()
            if parent_widget:
                  parent_widget.playerNameSearchBox.setPlainText(player_name)
                  parent_widget.searchPlayer()
                  self.close()
            else:
                  throwErrorMessage("Error finding Main Window", "Close and reopen the application fully")
      def keyPressEvent(self, event):
            if event.key() == QtCore.Qt.Key.Key_Escape:
                  self.close()
            else:
                  super().keyPressEvent(event)
      def closeEvent(self, event):
            self.saveStarsCSV()
            super().closeEvent(event)
      def addToTargetTable(self, day):
            player_name = self.playerNameSTTBox.toPlainText()
            fleet_name = self.fleetNameSTTBox.toPlainText()
            last_stars = self.lastStarsSTTBox.toPlainText()
            max_trophies = self.maxTrophiesSTTBox.toPlainText()

            target_table = getattr(self, f"{day}Table")
            target_model = target_table.model()

            if target_model is None:
                  throwErrorMessage("Error", traceback.extract_stack()[-2].lineno)
            new_row = [QtGui.QStandardItem(player_name), QtGui.QStandardItem(fleet_name), QtGui.QStandardItem(last_stars), QtGui.QStandardItem(max_trophies)]

            target_model = target_table.model()
            target_table.setColumnWidth(1,100)
            target_table.setColumnWidth(2,50)
            target_table.setColumnWidth(3,75)
            if target_model is not None:
                  target_model.appendRow(new_row)
            else:
                  print("No model set for the target table")
            self.saveStarsCSV()
      async def fetch_user_maxtrophy(self, playername):
            global API_CALL_COUNT
            responses = await self.client.user_service.search_users(playername)
            API_CALL_COUNT += 1
            for response in responses:
                  return str(response.highest_trophy)
      def populateSTT(self, player_name):
            self.playerNameSTTBox.setPlainText(player_name)
            if not QSqlDatabase.database("targetdb").isOpen():
                  if not QSqlDatabase.database("targetdb").open():
                        throwErrorMessage("Database Connection Failure", "Targets DB did not open properly")
                        return
            query = QSqlQuery(QSqlDatabase.database("targetdb"))
            query.prepare("SELECT playername, fleetname, laststars FROM players WHERE playername = :player_name")
            query.bindValue(":player_name", player_name)
            if not query.exec():
                  throwErrorMessage("Database Query Error [1666]", query.lastError().text())
                  return
    
            if query.next():
                  fleet_name, last_stars = query.value(1), query.value(2)
                  max_trophies = asyncio.run(self.fetch_user_maxtrophy(player_name))
                  self.fleetNameSTTBox.setPlainText(fleet_name)
                  self.lastStarsSTTBox.setPlainText(str(last_stars))
                  self.maxTrophiesSTTBox.setPlainText(max_trophies)
            else:
                  self.fleetNameSTTBox.setPlainText(" ")
                  self.lastStarsSTTBox.setPlainText(" ")
                  self.maxTrophiesSTTBox.setPlainText(" ")
                  self.playerNameSTTBox.setPlainText(" ")
      def removeTargetTable(self, day):
            target_table = getattr(self, f"{day}Table")
            selected_indexes = target_table.selectionModel().selectedRows()
            for index in selected_indexes:
                  target_table.model().removeRow(index.row())
            self.saveStarsCSV()
      def resetStarsTargetList(self):
            confirmation_dialog = self.StarsTargetTrackConfirmationDialog(self)
            confirmation_dialog.exec()
      def saveStarsCSV(self):
            with open(self.getStarsFilePath(), 'w', newline='', encoding='utf-8') as csvfile:
                  writer = csv.writer(csvfile)
                  for day, widgets in self.table_widgets.items():
                        model = widgets["model"]
                        for row in range(model.rowCount()):
                              data = [model.index(row, col).data() for col in range(model.columnCount())]
                              writer.writerow([day] + data)
      def loadStarsCSV(self):
            try:
                  with open(self.getStarsFilePath(), 'r', newline='', encoding='utf-8') as csvfile:
                        reader = csv.reader(csvfile)
                        for row in reader:
                              day = row[0]
                              data = row[1:]
                              widgets = self.table_widgets[day]
                              model = widgets["model"]
                              model.appendRow([QtGui.QStandardItem(item) for item in data])
                              table = getattr(self, f"{day}Table")
                              table.setColumnWidth(0, 90)
                              table.setColumnWidth(1, 100)
                              table.setColumnWidth(2, 25)
                              table.setColumnWidth(3, 75)
            except FileNotFoundError:
                  print("CSV file not found, no data loaded. [StarTargetTrack]")
      class StarsTargetTrackConfirmationDialog(QtWidgets.QDialog):
            def __init__(self, parent=None):
                  super().__init__(parent)
                  uic.loadUi(os.path.join('_internal','_ui','pss-ttt-stt-confirm.ui'), self)

                  self.cancelButton.clicked.connect(self.reject)
                  self.confirmButton.clicked.connect(self.accept)
            def accept(self):
                  super().accept()

                  if self.parent():
                        self.parent().dayFourTable.model().clear()
                        self.parent().dayFiveTable.model().clear()
                        self.parent().daySixTable.model().clear()
                        self.parent().daySevenTable.model().clear()
                  else:
                        print("Parent not found")
            def reject(self):
                  super().reject()
class CrewLoadoutBuilderDialogBox(QtWidgets.QDialog):
      global CURRENT_STYLESHEET
      HEAD_LIST = []
      BODY_LIST = []
      LEG_LIST = []
      WEP_LIST = []
      ACC_LIST = []
      PET_LIST = []
      CREW_LIST = []

      EQUIPMENT_SLOTS: list[str] = ["Head", "Body", "Leg", "Weapon", "Accessory", "Pet"]
      
      def __init__(self, parent=None):
            super().__init__(parent)
            self.client = PssApiClient()
            uic.loadUi(os.path.join('_internal', '_ui', 'pss-ttt-clb.ui'), self)
            os.makedirs(os.path.join('_internal', '_equip'), exist_ok=True)
            os.makedirs(os.path.join('_internal', '_crew'), exist_ok=True)
            self.bodyEquipBox = self.findChild(QLineEdit, 'bodyEquipBox')
            self.headEquipBox = self.findChild(QLineEdit, 'headEquipBox')
            self.legEquipBox = self.findChild(QLineEdit, 'legEquipBox')
            self.wepEquipBox = self.findChild(QLineEdit, 'wepEquipBox')
            self.accessEquipBox = self.findChild(QLineEdit, 'accessEquipBox')
            self.petEquipBox = self.findChild(QLineEdit, 'petEquipBox')
            self.crewNameBox = self.findChild(QLineEdit, 'crewNameBox')

            version = asyncio.run(self.get_db_version())
            if api_database_needs_update(version):
                  print("Loading from API data as update is needed")
                  asyncio.run(self.fetch_item_list())
                  asyncio.run(self.fetch_crew_list())
            else:
                  print("Loading from established CSV due to no update needed")
                  self.loadItemsFromCSV()
                  self.loadCrewFromCSV()
            self.setup_completer(self.bodyEquipBox, self.BODY_LIST, "item")
            self.setup_completer(self.headEquipBox, self.HEAD_LIST, "item")
            self.setup_completer(self.legEquipBox, self.LEG_LIST, "item")
            self.setup_completer(self.wepEquipBox, self.WEP_LIST, "item")
            self.setup_completer(self.accessEquipBox, self.ACC_LIST, "item")
            self.setup_completer(self.petEquipBox, self.PET_LIST, "item")
            self.setup_completer(self.crewNameBox, self.CREW_LIST, "crew")
            self.finalChart = [[0,0] for _ in range(12)]
            self.finalTable = self.findChild(QTableView, "finalTableStats")
            self.finalModel = self.FinalStatsTableModel(self.finalChart, self)
            self.finalTable.setModel(self.finalModel)
            self.finalTable.setColumnWidth(0,50)
            self.finalTable.setColumnWidth(1,50)
            self.tpChart = [[0] for _ in range(9)]
            self.tpTable = self.findChild(QTableView, "crewTPTable")
            self.model = self.StatsTableModel(self.tpChart, self)
            self.tpTable.setModel(self.model)
            self.tpTable.setColumnWidth(0,50)
            self.tpTable.setColumnWidth(1,90)
            self.tpTable.setColumnWidth(2,90)

            self.loadCrewDataButton.clicked.connect(self.loadCrewData)
      def setStyle(self):
            if CURRENT_STYLESHEET == "default":
                  self.setStyleSheet("")
            elif CURRENT_STYLESHEET == "dark":
                  self.setStyleSheet(DARK_MODE_STYLESHEET)
      async def fetch_crew_list(self):
            global API_CALL_COUNT
            version = await self.get_db_version()
            config_data = load_config()
            if not config_data.get('config'):
                  throwErrorMessage("Fatal Error [fetch_crew_list]", "Config data not loaded properly")
            for entry in config_data['config']:
                  entry['item_database'] = version
                  save_config(config_data)
            crew_list = await self.client.character_service.list_all_character_designs()
            API_CALL_COUNT += 1
            all_crew_data = []
            for crew in crew_list:
#                 Crew Name, Equipment Mask, Rarity, Special, Collection, HP, Attack, RPR, ABL, PLT, SCI, ENG, WPN, RST, Walk, Run, TP
                  crew_data = [crew.character_design_name, crew.equipment_mask, crew.rarity, crew.special_ability_final_argument, crew.collection_design_id, crew.final_hp, crew.final_attack, 
                               crew.final_repair, crew.special_ability_final_argument, crew.final_pilot, crew.final_science, crew.final_engine, crew.final_weapon,
                               crew.fire_resistance, crew.walking_speed, crew.run_speed, crew.training_capacity]
                  self.CREW_LIST.append(crew_data)
                  all_crew_data.append(crew_data)
            self.saveCrewtoCSV(all_crew_data)
      def loadCrewData(self):
            crew_name = self.crewNameBox.text()
            for crew in self.CREW_LIST:
                  if crew[0] == crew_name:
                        crew_name, equipment_mask, rarity, special, collection, hp, attack, rpr, abl, plt, sci, eng, wpn, rst, walk, run, tp = crew[0], crew[1], crew[2], crew[3], crew[4], crew[5], crew[6], crew[7], crew[8], crew[9], crew[10], crew[11], crew[12], crew[13], crew[14], crew[15], crew[16]
                        equip = self.equipSlots(equipment_mask)
                        self.selectEquipmentBoxes(equip)
                        self.finalTable[0][0] = hp
                        self.finalTable[0][1] = attack
                        self.finalTable[0][2] = rpr
                        self.finalTable[0][3] = abl
                        self.finalTable[0][4] = plt
                        self.finalTable[0][5] = sci
                        self.finalTable[0][6] = eng
                        self.finalTable[0][7] = wpn
                        self.finalTable[0][8] = rst
                        self.finalTable[0][9] = walk
                        self.finalTable[0][10] = run
                        self.finalTable[0][11] = tp
      def selectEquipmentBoxes(self, equipmask):
            size = len(equipmask)
            self.hideAllEquipBoxes()
            for i in range(size):
                  if equipmask[i] == "Weapon":
                        self.wepHeroSideDD.show()
                        self.wepHeroSideStat.show()
                        self.wepEquipLabel.show()
                        self.wepEquipBox.show()
                  elif equipmask[i] == "Accessory":
                        self.accHeroSideDD.show()
                        self.accHeroSideStat.show()
                        self.accEquipLabel.show()
                        self.accessEquipBox.show()
                  elif equipmask[i] == "Leg":
                        self.legHeroSideDD.show()
                        self.legHeroSideStat.show()
                        self.legEquipLabel.show()
                        self.legEquipBox.show()
                  elif equipmask[i] == "Head":
                        self.headHeroSideDD.show()
                        self.headHeroSideStat.show()
                        self.headEquipLabel.show()
                        self.headEquipBox.show()
                  elif equipmask[i] == "Body":
                        self.bodyHeroSideDD.show()
                        self.bodyHeroSideStat.show()
                        self.bodyEquipLabel.show()
                        self.bodyEquipBox.show()
                  elif equipmask[i] == "Pet":
                        self.petHeroSideDD.show()
                        self.petHeroSideStat.show()
                        self.petEquipLabel.show()
                        self.petEquipBox.show()
                  else:
                        throwErrorMessage("Item Data incorrect [selectEquipmentBoxes]", "Equipment Mask data did not load properly")
                        return
      def hideAllEquipBoxes(self):
            self.petHeroSideDD.hide()
            self.petHeroSideStat.hide()
            self.petEquipLabel.hide()
            self.petEquipBox.hide()
            self.wepHeroSideDD.hide()
            self.wepHeroSideStat.hide()
            self.wepEquipLabel.hide()
            self.wepEquipBox.hide()
            self.accHeroSideStat.hide()
            self.accHeroSideDD.hide()
            self.accEquipLabel.hide()
            self.accessEquipBox.hide()
            self.legHeroSideStat.hide()
            self.legHeroSideDD.hide()
            self.legEquipLabel.hide()
            self.legEquipBox.hide()
            self.headHeroSideStat.hide()
            self.headHeroSideDD.hide()
            self.headEquipLabel.hide()
            self.headEquipBox.hide()
            self.bodyHeroSideStat.hide()
            self.bodyHeroSideDD.hide()
            self.bodyEquipLabel.hide()
            self.bodyEquipBox.hide()
      def readCrewFromCSV(self):
            data_list = []
            try:
                  with open(os.path.join('_internal', '_crew', 'crewlist.csv'), 'r', newline='', encoding='utf-8') as csvfile:
                        reader = csv.reader(csvfile)
                        next(reader)
                        for row in reader:
                              data_list.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16]))
            except FileNotFoundError:
                  print(f"File crewlist.csv not found")
            return data_list
      def loadCrewFromCSV(self):
            self.CREW_LIST.clear()
            self.CREW_LIST.extend(self.readCrewFromCSV())
      def saveCrewtoCSV(self, data_list):
            with open(os.path.join('_internal','_crew','crewlist.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                  writer = csv.writer(csvfile)
                  header = ["Crew Name", "Equipment Mask", "Rarity", "Special", "Collection", "HP", "Attack", "RPR", "ABL", "PLT", "SCI", "ENG", "WPN", "RST", "Walk", "Run", "TP"]
                  writer.writerow(header)
                  writer.writerows(data_list)
      def equipSlots(self, mask):
            equipment_mask = int(mask)
            output = [int(x) for x in f"{equipment_mask:06b}"]
            return [self.EQUIPMENT_SLOTS[5-i] for i, b in enumerate(output) if b]
      def setup_completer(self, line_edit, list, type):
            word_list = self.initiateCompleterList(list, type)
            completer = QCompleter(word_list, parent=self)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            line_edit.setCompleter(completer)
      def initiateCompleterList(self, data_list, type):
            if type == "item":
                  word_list = []
                  for line in data_list:
                        item_design_name, rarity, enhancement_type, enhancement_value = line
                        if enhancement_type == "FireResistance":
                              enhancement_type = "RST"
                        elif enhancement_type == "Pilot":
                              enhancement_type = "PLT"
                        elif enhancement_type == "Ability":
                              enhancement_type = "ABL"
                        elif enhancement_type == "Weapon":
                              enhancement_type = "WPN"
                        elif enhancement_type == "Engine":
                              enhancement_type = "ENG"
                        elif enhancement_type == "Science":
                              enhancement_type = "SCI"
                        elif enhancement_type == "Attack":
                              enhancement_type = "ATK"
                        elif enhancement_type == "Stamina":
                              enhancement_type = "STA"
                        elif enhancement_type == "Repair":
                              enhancement_type = "RPR"
                        elif enhancement_type == "Hp":
                              enhancement_type = "HP"
                        text = f"{item_design_name} ({enhancement_type} +{enhancement_value})"
                        word_list.append(text)
                  return word_list
            elif type == "crew":
                  word_list = []
                  for line in data_list:
                        #Crew Name,Equipment Mask,Rarity,Special,Collection,HP,Attack,RPR,ABL,PLT,SCI,ENG,WPN,RST,Walk,Run,TP
                        crew_name, equipment_mask, rarity, special, collection, hp, attack, rpr, abl, plt, sci, eng, wpn, rst, walk, run, tp = line
                        text = crew_name
                        word_list.append(text)
                  return word_list
      async def get_db_version(self):
            global API_CALL_COUNT
            version = await self.client.get_latest_version()
            API_CALL_COUNT += 1
            return version.recommended_version
      async def fetch_item_list(self):
            global API_CALL_COUNT
            # Item_Design_Name,Enhancement_Type,Enhancement_Value,Item_Sub_Type  ,Rarity
            # La Paula        ,Ability         ,17.0             ,EquipmentWeapon,Hero
            version = await self.get_db_version()
            config_data = load_config()
            if not config_data.get('config'):
                  throwErrorMessage("Fatal Error [fetch_item_list]", "Config data not loaded properly")
            for entry in config_data['config']:
                  entry['item_database'] = version
                  save_config(config_data)
            item_designs = await self.client.item_service.list_item_designs()
            API_CALL_COUNT += 1
            for item in item_designs:
                  if item.item_sub_type == 'EquipmentHead':
                        self.HEAD_LIST.append((item.item_design_name, item.rarity, item.enhancement_type, item.enhancement_value))
                  elif item.item_sub_type == 'EquipmentWeapon':
                        self.WEP_LIST.append((item.item_design_name, item.rarity, item.enhancement_type, item.enhancement_value))
                  elif item.item_sub_type == 'EquipmentBody':
                        self.BODY_LIST.append((item.item_design_name, item.rarity, item.enhancement_type, item.enhancement_value))
                  elif item.item_sub_type == 'EquipmentLeg':
                        self.LEG_LIST.append((item.item_design_name, item.rarity, item.enhancement_type, item.enhancement_value))
                  elif item.item_sub_type == 'EquipmentAccessory':
                        self.ACC_LIST.append((item.item_design_name, item.rarity, item.enhancement_type, item.enhancement_value))
                  elif item.item_sub_type == 'EquipmentPet':
                        self.PET_LIST.append((item.item_design_name, item.rarity, item.enhancement_type, item.enhancement_value))
            self.saveItemsToCSVfiles()
      def write_itemlist_to_csv(self, file_name, data_list):
            with open(os.path.join('_internal','_equip',file_name), 'w', newline='', encoding='utf-8') as csvfile:
                  writer = csv.writer(csvfile)
                  header = ["Item_Design_Name", "Enhancement_Type", "Enhancement_Value", "Item_Sub_Type", "Rarity"]
                  writer.writerow(header)
                  writer.writerows(data_list)
      def saveItemsToCSVfiles(self):
            listedcsv = [
                  ('HEAD_LIST.csv', self.HEAD_LIST),
                  ('WEP_LIST.csv', self.WEP_LIST),
                  ('BODY_LIST.csv', self.BODY_LIST),
                  ('LEG_LIST.csv', self.LEG_LIST),
                  ('ACC_LIST.csv', self.ACC_LIST),
                  ('PET_LIST.csv', self.PET_LIST)]
            for file_name, data_list in listedcsv:
                  self.write_itemlist_to_csv(file_name, data_list)
      def read_itemlist_from_csv(self, file_name):
            data_list = []
            try:
                  with open(os.path.join('_internal','_equip',file_name), 'r', newline='', encoding='utf-8') as csvfile:
                        reader = csv.reader(csvfile)
                        next(reader)
                        for row in reader:
                              data_list.append((row[0], row[1], row[2], row[3]))
            except FileNotFoundError:
                  print(f"File {file_name} not found")
            return data_list
      def loadItemsFromCSV(self):
            listedcsv = [
                  ('HEAD_LIST.csv', self.HEAD_LIST),
                  ('WEP_LIST.csv', self.WEP_LIST),
                  ('BODY_LIST.csv', self.BODY_LIST),
                  ('LEG_LIST.csv', self.LEG_LIST),
                  ('ACC_LIST.csv', self.ACC_LIST),
                  ('PET_LIST.csv', self.PET_LIST)]
            
            for file_name, data_list in listedcsv:
                  data_list.clear()
                  data_list.extend(self.read_itemlist_from_csv(file_name))
      class StatsTableModel(QAbstractTableModel):
            def __init__(self, data, parent=None):
                  super().__init__()
                  self._data = data
                  self.parent = parent
                  self.verticalHeaders = ['HP','ATK','ABL','STA','RPR','PLT','SCI','ENG','WPN']
                  self.horizontalHeaders = ['TP']
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
      class FinalStatsTableModel(QAbstractTableModel):
            def __init__(self, data, parent=None):
                  super().__init__()
                  self._data = data
                  self.parent = parent
                  self.verticalHeaders = ['HP','ATK','RPR','ABL','STA','PLT','SCI','ENG','WPN','RST','Walk','Run']
                  self.horizontalHeaders = ['Stat', 'Base', 'Final']
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
if __name__ == "__main__":
      app = QtWidgets.QApplication(sys.argv)
      if create_connection(getDefaultProfile()):
            create_table()
      else:
            sys.exit(1)
      modify_SQL()
      window = MainWindow()
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      asyncio.run(window.main())
      app.exec()