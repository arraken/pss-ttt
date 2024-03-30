I have a submission in to Microsoft to stop the program from triggering a false positive with Windows Defender. You can go into protection history with windows defender and restore the program if/when it quarantines the exe

Created an MSI for the program to properly install all necessary files and imports for the python. Recommend to download the /past fleets command from Dolores discord bot into the pss-ttt file location and then use the import option in the program to pull fleet/targets data in.

Default installation will be located below, but you can change it in the installer:
C:\Users\PC USERNAME HERE\AppData\Roaming\Pixel Starships - Target Tracking Tool


Gist of this app is to allow you to manually track targets as you come across them in pvp, Legends, and tournament fights. 

THIS APP DOES NOT PULL LIVE DATA (yet). You will need to download the pastfleets csv file from Dolores Bot. I recommend pulling it twice a month (day before tourny and day after tourny) and then using Import Data button you can populate/update the database for the tool. 

Both player name and fleet are searchable. Player names are case sensitive when searching. If you are having trouble finding them you can also use the Search browser which will hold the names of all players currently in your stored database of players. From this browser you can filter the names or you can limit them to the number of characters in the name. This window allows you to select a name and then copy it to the primary window for ease of access to players with non-english characters for fast searching

Fleet search button will populate a window based on the players in the fleet typed into the box. 

The Fleet Search Browser button will populate a window based on the fleets currently in your database. 

These 4 different search options allow you to quickly find players with non-english characters that are located in your database.

Export fights will essentially dump all your saved player and fights data into 2 files (exportedplayers.csv and exportedfights.csv) into the _internal folder for you to look through if you desire

Crew Trainer is a basic module that will help you figure out when to train specific stats and what training to use. This part of the app assumes you have level 3 for both gym and academy trained up. You may also save templates for crew so you can reference them later here

Tourny Stars Calc will help give you daily star goals for the monthly tournament based on your choices in the suggested fields on the left.

Start Target Track will allow you to compile a list of targets for days 4-7 for the tournament and will copy the data from the currently searched player for you to add to whichever days you are looking for. From this window you can also add/remove/or pull up the player by selecting the row they are on and clicking copy & search.