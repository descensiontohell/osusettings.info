import aiohttp_jinja2
from aiohttp.web_exceptions import HTTPNotFound, HTTPBadRequest, HTTPUnauthorized, HTTPForbidden, HTTPConflict
from aiohttp_apispec import response_schema, querystring_schema, docs
from requests import HTTPError
from sqlalchemy.exc import IntegrityError

from backend.app.players.filter import LeaderboardFilter
from backend.app.players.schemas import LeaderboardSchema, GetPlayersQuerySchema, PlayerSchema, SettingsHistorySchema
from backend.app.web.response import json_response
from backend.app.web.app import View


"""
Users views:

1. GET - /api/users/{osu_id}
    Returns all player stats, player settings AND settings_history field

    Codes:
        - 200 - returned requested user
        - 404 - user not found


2. POST - /api/users/{osu_id} (admin only)
    Adds a new user with given osu_id and gets their stats from osu!api

    Codes:
        - 201 - user created (client should be redirected)
        - 401 - not logged in
        - 403 - logged in but the user is not admin
        - 409 - conflict - user exists (client should be redirected to according userpage)


3. PATCH - /api/users/{osu_id} (admin OR owner of the osu_id)
    Updates user settings:
        - Put old settings into settings_history
        - Patch settings with new ones (settings that are not updated with the request stay the same)
        - Fills updated_by field with session["username"] username
        - Fills last_updated field with datetime.now()

    Codes:
        - 200 - user updated
        - 400 - invalid schema
        - 401 - not logged in
        - 403 - logged in but the user is not admin or osu_id owner
        - 409 - conflict - client should be redirected to according userpage
        - 422 - can't update settings with given request body (add_new_item is True, but no item id provided etc.)
"""


class LeaderboardView(View):
    @aiohttp_jinja2.template("index.html")
    async def get(self):
        is_logged_in = True if self.request.player_id else False
        return {
            "is_logged_in": is_logged_in,
            "player_id": self.request.player_id,
            "player_name": self.request.player_name,
            "is_admin": self.request.is_admin,
            "redirect_uri": f"{self.request.app.config.credentials.server_name}/callback",
            "server_name": self.request.app.config.credentials.server_name,
            "client_id": self.request.app.config.credentials.client_id,
        }


class ApiLeaderboardView(View):
    @docs(
        tags=["Players"],
        summary="Get leaderboard with players and their settings",
        description="""Returns a list of mouse players or a list of tablet players.
                    For filtering multiple playstyles you need to put it in query string multiple times (see example)

                    /api/players?is_mouse=true&playstyle=1&playstyle=2&page=2&min_rank=100&name=potato&mouse=razer&order_by=pp
                    """,
        responses={
            200: {"description": "Ok. Leaderboard returned in response[\"data\"]", "schema": LeaderboardSchema},
            400: {"description": "Unprocessable Entity. Wrong filters applied"}
        },
    )
    @response_schema(LeaderboardSchema, 200)
    @querystring_schema(GetPlayersQuerySchema)
    async def get(self):
        args = self.request["querystring"]
        players_filter = LeaderboardFilter(**args)

        is_mouse_list = args.get("is_mouse", True)
        players = await self.store.players.get_players(players_filter)
        return json_response(
            data=LeaderboardSchema().dump({"players": players, "is_mouse_list": is_mouse_list}))


class SinglePlayerView(View):
    @docs(
        tags=["Players"],
        summary="Get single player data",
        description="Returns player data by osu_id.",
        responses={
            200: {"description": "Success", "schema": PlayerSchema},
            400: {"description": "osu_id is not a valid integer"},
            404: {"description": "Player not found"}
        },
    )
    @response_schema(PlayerSchema(), 200)
    async def get(self):
        try:
            osu_id = int(self.request.match_info["osu_id"])
            if osu_id > 2147483647 or osu_id < -2147483647:
                raise ValueError
        except ValueError:
            raise HTTPBadRequest()

        user = await self.store.players.get_user_by_osu_id_or_name(osu_id)

        if not user:
            raise HTTPNotFound(reason=f"User {osu_id} not found")

        return json_response(data=PlayerSchema().dump(user))

    @docs(
        tags=["Players"],
        summary="Add new player [admin]",
        description="Adds new player to the system or does nothing if the player exists. \
Sets according osu! stats if the player is added",
        responses={
            200: {"description": "Success"},
            400: {"description": "osu_id is not a valid integer"},
            409: {"description": "Player already exists"}
        },
    )
    async def post(self):
        # if not self.request.player_id:
        #     raise HTTPUnauthorized
        #
        # if not self.request.is_admin:
        #     raise HTTPForbidden

        try:
            osu_id = int(self.request.match_info["osu_id"])
            if osu_id > 2147483647 or osu_id < -2147483647:
                raise ValueError
        except ValueError:
            raise HTTPBadRequest()

        try:
            await self.store.players.add_new_player(osu_id=osu_id)
        except HTTPError:
            raise HTTPNotFound(reason=f"User {osu_id} not found")
        except IntegrityError:
            raise HTTPConflict(reason=f"User {osu_id} exists")

        return json_response()


class PlayerSettingsHistoryView(View):
    @docs(
        tags=["Players"],
        summary="Get player settings history",
        description="""Returns settings history of player with id=osu_id. 
        Returns empty list if there is no history or player does not exist.""",
        responses={
            200: {"description": "Success", "schema": SettingsHistorySchema},
            400: {"description": "osu_id is not a valid integer"},
        },
    )
    @response_schema(SettingsHistorySchema, 200)
    async def get(self):
        try:
            osu_id = int(self.request.match_info["osu_id"])
            if osu_id > 2147483647 or osu_id < -2147483647:
                raise ValueError
        except ValueError:
            raise HTTPBadRequest(reason="osu_id must be an integer")

        settings_list = await self.store.players.get_settings_history_by_osu_id(osu_id)

        if settings_list is None:
            raise HTTPNotFound(reason=f"User {osu_id} not found")

        return json_response(data=SettingsHistorySchema().dump({"settings": settings_list}))
