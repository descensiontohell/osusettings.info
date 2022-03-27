Terms of Reference
0. Technology Stack:

   Backend:
   - Python
   - aiohttp / fastapi (TBD)
   - postgresql 
   - sqlalchemy orm
   - alembic
   Frontend:
   - TBD

1. Project goal
   
   To create a system to keep track of player settings for the online game osu! This system is a development of [osu! Top Mouse Player List](https://docs.google.com/spreadsheets/d/1EOWc7kf9TdyvT31VfzlY284udUNOrtz0uyRtQ2t4MHY/edit#gid=0). This system is designed for players who want to know about the settings and devices of other players, as well as those wishing to share their own, which can be stored in one place.

2. System Description.
   
   The system has the following main components:
   1. Functionality for administrators (adding and editing information about players, their playstyle, settings, devices)
   2. Functionality for displaying players' information on the main page (leaderboard) with that can be filtered by nickname, country, rank, each of their settings items, and devices.
   3. Functionality for keeping track of each player's settings history
   4. Functionality for automatic update of the players' ranks in the database
   5. Functionality for viewing the page of a particular player and the history of their settings
   Extras:
   1. Functionality for authorization with osu!auth for players, so they can change their data without the participation of the administrator
   2. The ability to generate a card with the data about the player and their settings as an image that can be placed in the userpage, stream description or anywhere else.

3. Registration and authorization
   
   The first version of the system does not provide registration and authorization of users. Only users who are administrators can authorize. Administrator accounts are created via api for user management
   In subsequent versions may be implemented registration and authorization through osu!auth to allow players edit their data

4. Possibilities of administrators
   
   The first version of the system implies the following capabilities for administrators:
   - Adding new players to the system
   - Editing settings of players in the system
   - Deleting players from the system

5. Players' data in the system
   
   The system is designed to record the following data:
   1. Nick, rank, rank in country, country, performance points of the player
   2. Playstyle
    - If the device is a mouse:
        1. DPI
        2. OS sens
        3. ingame sens
        4. resolution
        5. raw input
        6. area
        7. mouse model
        8. mousepad
        9. sensor
        10. weight
        11. length
        12. width
        13. height
        14. mouse switch
        15. keyboard model
        16. keyboard switch
    - If the device is a tablet:
        1. TBD

6. Updating the ranks of players in the system
   
   For the time being, there is no functionality for player authorization in the system:
   - The script gets the information from osu!api and updates it in the database one by one for each player in the database
   After the authorization functionality is implemented:
   - For players with a global rank of 1-10000 there is an automatic update of rank and performance points. The script gets information from osu!api and updates it in the database
   - For players with a rank below 10000 the updating of a rank and points of productivity happens only when they log in

7. Tracking history of player settings
   
   TBD

8. Authorized Users Features
   
   TBD

9.  Generating a card with settings
    
   TBD


