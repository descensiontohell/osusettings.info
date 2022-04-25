from hashlib import sha256

from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session

from backend.app.web.app import View
from backend.app.web.mixins import SuperuserRequiredMixin
from backend.app.web.response import json_response, error_json_response
from backend.app.service_api.schemas import SuperuserLoginSchema


class SuperuserLoginView(View):
    @request_schema(SuperuserLoginSchema)
    async def post(self):
        name = self.data["name"]
        password = self.data["password"]

        superuser = await self.store.service.get_su_by_name(name=name)

        if not superuser or not superuser.is_valid_password(password):
            raise HTTPUnauthorized

        session = await new_session(request=self.request)
        session["superuser"] = superuser.name
        return json_response()


# class SuperuserGrantAdminView(View):
#     @request_schema
#     @response_schema
#
#
# class SuperuserRevokeAdminView(View):
#     @request_schema
#     @response_schema


