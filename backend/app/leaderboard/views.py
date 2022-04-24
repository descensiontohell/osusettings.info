from aiohttp_apispec import request_schema, response_schema

from backend.app.leaderboard.schemas import LeaderboardSchema
from backend.app.web.response import json_response, error_json_response
from backend.app.web.app import View


class GetPlayersView(View):
    @response_schema(LeaderboardSchema, 200)
    async def get(self):
        args = self.store.players.parse_filters(self.request.rel_url.query)

        if args.get("is_mouse") is True:
            is_mouse_list = True
        else:
            is_mouse_list = False

        players = await self.store.players.get_players(**args)

        return json_response(
            data=LeaderboardSchema().dump({"players": players, "is_mouse_list": is_mouse_list}))

