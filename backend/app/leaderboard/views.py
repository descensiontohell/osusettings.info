from aiohttp_apispec import request_schema, response_schema, querystring_schema, docs

from backend.app.leaderboard.schemas import LeaderboardSchema, GetPlayersQuerySchema
from backend.app.web.response import json_response, error_json_response
from backend.app.web.app import View


class GetPlayersView(View):
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
        # args = self.store.players.parse_filters(self.request.rel_url.query)
        print(args)

        if args.get("is_mouse") is True:
            is_mouse_list = True
        else:
            is_mouse_list = False

        players = await self.store.players.get_players(**args)

        return json_response(
            data=LeaderboardSchema().dump({"players": players, "is_mouse_list": is_mouse_list}))

