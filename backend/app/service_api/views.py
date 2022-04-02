from hashlib import sha256

from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session

from backend.app.web.response import json_response, error_json_response
from backend.app.service_api.schemas import SuperuserSchema
from backend.app.web.app import View


class SuperuserLoginView(View):
    @request_schema(SuperuserSchema)
    @response_schema(SuperuserSchema, 200)
    async def post(self):
        name, password = self.data["name"], self.data["password"]
        superuser = await self.store.service.get_su_by_name(name=name)
        if not superuser or superuser.password != sha256(password.encode()).hexdigest():
            raise HTTPUnauthorized
        superuser_data = SuperuserSchema().dump(superuser)
        response = json_response(data=superuser_data)
        session = await new_session(request=self.request)
        session["superuser"] = superuser.name
        return response
