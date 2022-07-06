import logging

from aiohttp.web_exceptions import HTTPUnauthorized, HTTPFound
from aiohttp_session import new_session, get_session

from backend.app.web.app import View
from backend.app.web.response import json_response


class AuthView(View):
    async def get(self):
        params = self.request.rel_url.query
        if len(params) != 1 or "code" not in params:
            raise HTTPUnauthorized

        code = params["code"]
        player = await self.request.app.store.auth.identify_player(oauth_code=code)

        # self.request.app.store.


        log = logging.getLogger("SUS")
        log.info(player)

        session = await new_session(request=self.request)
        session["player_name"] = player["name"]
        session["player_id"] = player["osu_id"]

        raise HTTPFound(location="http://localhost:8080")
        return json_response()

    async def post(self):
        session = await get_session(self.request)
        session["player_name"] = None
        session["player_id"] = None
        session["is_admin"] = None
        session["is_superuser"] = None

        raise HTTPFound(location="http://localhost:8080")
