### What is that?
osusettings is codename for a website that is a successor of [osu! Top Mouse Player List](https://docs.google.com/spreadsheets/d/1EOWc7kf9TdyvT31VfzlY284udUNOrtz0uyRtQ2t4MHY/edit#gid=0). We are working on this project to move the list to its own website to make it fancy and maintainable. 

### What is implemented:
 - Players list with settings retrieval (filters are supported)
- Items, players, player settings history retrieval
- Sample OAuth page that adds (or updates) player to the database on login
- Automated rank updating for players in the database
- Superuser endpoints to manage players with admin rights

### Goals:
- See [Terms of Reference](https://github.com/descensiontohell/osusettings.info/blob/main/docs/en_Terms_of_Reference.md)

### Development:
 1. Clone the repo:
```
git clone https://github.com/descensiontohell/osusettings.info.git && cd osusettings.info
```
2. Register new OAuth application on https://osu.ppy.sh/home/account/edit
	- Application Callback URL **must** be `http://localhost:8080/callback`
3. Set according variables in `.env` file:
```
CLIENT_ID=oauth_app_client_id
CLIENT_SECRET=oauth_app_client_secret
SERVER_NAME=http://localhost:8080

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```
4. Run the containers:
```
docker-compose up
```
5. Navigate to Swagger UI: `http://localhost:8080/api/docs`
6. Rebuild the app after changes:
```
docker-compose down && docker-compose up --build
```
### Next  tasks:
- Finish update player endpoint
- Modify playstyle models & implement playstyle retrieval 
