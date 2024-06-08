Pixel Starships - Target Tracking Tool

**I have a submission in to Microsoft to stop the program from triggering a false positive with Windows Defender. You can go into protection history with windows defender and restore the program if/when it quarantines the exe**

Created an MSI for the program to properly install all necessary files and imports for the python. Recommend to download the /past fleets command from Dolores discord bot into the pss-ttt file location and then use the import option in the program to pull fleet/targets data in.

Default installation will be located below, but you can change it in the installer:
C:\Users*PC USERNAME HERE*\AppData\Roaming\pss-ttt\Pixel Starships - Target Tracking Tool
![Pixel_Starships_Target_Tracking_Tool_qFgbXoyJ1g](https://github.com/arraken/pss-ttt/assets/52732965/9fa8baed-4c20-489e-8204-6c96daedb374)
![Pixel_Starships_Target_Tracking_Tool_zIBDbn6d7E](https://github.com/arraken/pss-ttt/assets/52732965/36fca101-d9c5-4839-ad07-03f71284e7dc)
![Pixel_Starships_Target_Tracking_Tool_NxRF54LnBZ](https://github.com/arraken/pss-ttt/assets/52732965/8dc07138-3f4d-4d22-ad54-6293b99b3a74)
![Pixel_Starships_Target_Tracking_Tool_O5cFvOw2cI](https://github.com/arraken/pss-ttt/assets/52732965/30b52d48-30cb-4677-b13c-85943a1e2cdb)
![Pixel_Starships_Target_Tracking_Tool_CjJo1T7R2u](https://github.com/arraken/pss-ttt/assets/52732965/84aab051-2d0f-4585-9ff8-29c30ba39035)
![Pixel_Starships_Target_Tracking_Tool_lCbDtHJHYD](https://github.com/arraken/pss-ttt/assets/52732965/ffd8343e-0b78-4200-9e0b-35123c707783)
![Pixel_Starships_Target_Tracking_Tool_VX48b0cXIR](https://github.com/arraken/pss-ttt/assets/52732965/bee16f47-71ba-43f7-88ca-33bcdf24e451)

Noteworthy changes:
- NOW ABLE TO PULL DATA FROM PSS API!
- Additional API calls are done to try to improve functionality for the app
- Ship profiles that let you manage fights for different accounts
- Profiles will convert your current databases to default profile you make upon loading app
- Various backend changes to databases for streamlining future changes
- UUID generation is done once per application/installation
- Merging crew is now accounted for during crew training
- Cleaned up file storage systems (3 new folders for UI, Crew Data, Equipment Data)

Known Bugs:
Tournament Stars are not updating/saving properly