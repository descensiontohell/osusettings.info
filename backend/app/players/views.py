from hashlib import sha256
from urllib.parse import parse_qsl

from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session
from multidict._multidict import MultiDictProxy, MultiDict

from backend.app.players.schemas import LeaderboardSchema
from backend.app.web.response import json_response, error_json_response
from backend.app.service_api.schemas import SuperuserSchema
from backend.app.web.app import View


class GetPlayersView(View):
    async def get(self):
        args = self.store.players.parse_filters(self.request.rel_url.query)
        players = await self.store.players.get_players(**args)
        return json_response(
            data=LeaderboardSchema().dump({"players": players}))
