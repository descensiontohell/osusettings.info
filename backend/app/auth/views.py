import logging

from aiohttp.web_exceptions import HTTPUnauthorized, HTTPFound
from aiohttp_session import new_session, get_session

from backend.app.web.app import View


class AuthView(View):
    async def get(self):
        params = self.request.rel_url.query
        if len(params) != 1 or "code" not in params:
            raise HTTPUnauthorized

        code = params["code"]
        player = await self.store.auth.identify_player(oauth_code=code)

        if await self.store.service.is_user_admin(osu_id=player["osu_id"]):
            is_admin = True
        else:
            is_admin = False

        session = await new_session(request=self.request)
        session["player_name"] = player["name"]
        session["player_id"] = player["osu_id"]
        session["is_admin"] = is_admin

        await self.store.auth.add_or_update_player(player)

        raise HTTPFound(location=self.request.app.config.credentials.server_name)

    async def post(self):
        session = await get_session(self.request)
        session["player_name"] = None
        session["player_id"] = None
        session["is_admin"] = None
        session["is_superuser"] = None

        raise HTTPFound(location=self.request.app.config.credentials.server_name)
