from aiohttp.web_response import json_response
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session
from sqlalchemy import select

from backend.app.players.models import PlayerModel
from backend.app.web.app import View
from aiohttp.web import HTTPForbidden, HTTPUnauthorized, HTTPNotImplemented


class TestView(View):
    async def get(self):
        await self.store.api.test()
        return json_response(data={"status": "ok"})

