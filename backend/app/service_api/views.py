from aiohttp.web_exceptions import HTTPUnauthorized, HTTPConflict, HTTPNotFound
from aiohttp_apispec import request_schema, response_schema
from aiohttp_cors import CorsViewMixin
from aiohttp_session import new_session

from backend.app.web.app import View
from backend.app.web.mixins import SuperuserRequiredMixin
from backend.app.web.response import json_response
from backend.app.service_api.schemas import SuperuserLoginRequestSchema, SuperuserLoginResponseSchema, \
    SuperuserManageAdminsSchema, ListAdminsSchema


class SuperuserLoginView(View, CorsViewMixin):
    @request_schema(SuperuserLoginRequestSchema)
    async def post(self):
        name = self.data["name"]
        password = self.data["password"]

        superuser = await self.store.service.get_su_by_name(name=name)
        if not superuser or not superuser.is_valid_password(password):
            raise HTTPUnauthorized

        session = await new_session(request=self.request)
        session["is_superuser"] = True
        return json_response(data=SuperuserLoginResponseSchema().dump({"name": superuser.name}))


class SuperuserManageAdminsView(SuperuserRequiredMixin, View, CorsViewMixin):
    @request_schema(SuperuserManageAdminsSchema)
    @response_schema(ListAdminsSchema, 200)
    async def post(self):
        osu_id = self.data["osu_id"]
        if await self.store.service.is_user_in_admins_list(osu_id):
            raise HTTPConflict
        if not await self.store.service.user_exists(osu_id):
            raise HTTPNotFound
        await self.store.service.add_new_admin(osu_id)
        admins = await self.store.service.get_admins()
        return json_response(data=ListAdminsSchema().dump({"admins": admins}))

    @request_schema(SuperuserManageAdminsSchema)
    @response_schema(ListAdminsSchema, 200)
    async def delete(self):
        osu_id = self.data["osu_id"]
        if not await self.store.service.is_user_in_admins_list(osu_id):
            raise HTTPNotFound
        await self.store.service.remove_admin(osu_id)
        admins = await self.store.service.get_admins()
        return json_response(data=ListAdminsSchema().dump({"admins": admins}))

    @response_schema(ListAdminsSchema, 200)
    async def get(self):
        admins = await self.store.service.get_admins()
        return json_response(data=ListAdminsSchema().dump({"admins": admins}))


class SuperuserCalculateEdpiView(SuperuserRequiredMixin, View, CorsViewMixin):
    async def post(self):
        await self.store.service.update_players_edpi()
        return json_response()
