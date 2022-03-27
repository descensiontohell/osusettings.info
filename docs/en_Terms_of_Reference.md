# 1. Technology Stack:
   
Backend:
- Python
- aiohttp / fastapi (TBD)
- postgresql 
- sqlalchemy orm
- alembic

Frontend:
- TBD

# 2. Project goal

To create a system to keep track of player settings for the online game osu! This system is a development of [osu! Top Mouse Player List](https://docs.google.com/spreadsheets/d/1EOWc7kf9TdyvT31VfzlY284udUNOrtz0uyRtQ2t4MHY/edit#gid=0). This system is designed for players who want to know about the settings and devices of other players, as well as those wishing to share their own, which can be stored in one place.

# 3. System Description.

The system has the following main components:
- Functionality for administrators (adding and editing information about players, their playstyle, settings, devices)
- Functionality for displaying players' information on the main page (leaderboard) with that can be filtered by nickname, country, rank, each of their settings items, and devices.
- Functionality for keeping track of each player's settings history
- Functionality for automatic update of the players' ranks in the database
- Functionality for viewing the page of a particular player and the history of their settings

Extras:
- Functionality for authorization with osu!auth for players, so they can change their data without the participation of the administrator
- The ability to generate a card with the data about the player and their settings as an image that can be placed in the userpage, stream description or anywhere else.

# 4. Registration and authorization
   
The first version of the system does not provide registration and authorization of users. Only users who are administrators can authorize. Administrator accounts are created via api for user management
In subsequent versions may be implemented registration and authorization through osu!auth to allow players edit their data

# 5. Possibilities of administrators
   
The first version of the system implies the following capabilities for administrators:
- Adding new players to the system
- Editing settings of players in the system
- Deleting players from the system

# 6. Players' data in the system
   
The system is designed to record the following data:
- Nick, rank, rank in country, country, performance points of the player
- Playstyle
- If the device is a mouse:
   - DPI
   - OS sens
   - ingame sens
   - resolution
   - raw input
   - area
   - mouse model
   - mousepad
   - sensor
   - weight
   - length
   - width
   - height
   - mouse switch
   - keyboard model
   - keyboard switch
- If the device is a tablet:
   - TBD

# 6. Updating the ranks of players in the system
   
For the time being, there is no functionality for player authorization in the system:
- The script gets the information from osu!api and updates it in the database one by one for each player in the database
After the authorization functionality is implemented:
- For players with a global rank of 1-10000 there is an automatic update of rank and performance points. The script gets information from osu!api and updates it in the database
- For players with a rank below 10000 the updating of a rank and points of productivity happens only when they log in

# 7. Tracking history of player settings

TBD

# 8.  Authorized Users Features

TBD

# 9.  Generating a card with settings

TBD


