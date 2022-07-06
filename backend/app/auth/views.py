import logging

from aiohttp.web_exceptions import HTTPUnauthorized

from backend.app.web.app import View
from backend.app.web.response import json_response


class AuthView(View):
    async def get(self):
        params = self.request.rel_url.query
        if len(params) != 1 or "code" not in params:
            raise HTTPUnauthorized
        log = logging.getLogger("SUS")
        log.info(params)
        return json_response()
