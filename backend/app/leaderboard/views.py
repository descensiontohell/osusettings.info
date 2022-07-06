import aiohttp_jinja2
from aiohttp_apispec import response_schema, querystring_schema, docs

from backend.app.leaderboard.filter import LeaderboardFilter
from backend.app.leaderboard.schemas import LeaderboardSchema, GetPlayersQuerySchema
from backend.app.web.response import json_response
from backend.app.web.app import View


class LeaderboardView(View):
    @aiohttp_jinja2.template("index.html")
    async def get(self):
        is_logged_in = True if self.request.player_id else False
        return {
            "is_logged_in": is_logged_in,
            "player_id": self.request.player_id,
            "player_name": self.request.player_name,
        }


class ApiPlayersView(View):
    @docs(
        tags=["Leaderboard"],
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
