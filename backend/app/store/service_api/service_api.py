import typing
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from backend.app.store.database.models import PlayerModel, SuperuserModel, AdminModel
from backend.app.store.base.base_accessor import BaseAccessor
from backend.app.store.service_api.dataclasses import Superuser

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class ServiceAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, "API", *args, **kwargs)
        self.app = app

    async def connect(self, app: "Application"):
        pass

    async def get_su_by_name(self, name: str) -> Optional[Superuser]:
        """Get superuser credentials from database table by name"""
        query = select(SuperuserModel).where(name == SuperuserModel.name)
        superuser = (await self.app.database.db.scalar(query))
        if superuser is not None:
            return superuser.to_dc()
        return None

    async def is_user_in_admins_list(self, osu_id: int) -> bool:
        """Checks if specified osu_id belongs to admin in Redis cache"""
        return osu_id in await self.get_admin_ids_list()

    async def user_exists(self, osu_id: int) -> bool:
        """Checks if user with specified osu_id exists in players database table"""
        query = select(PlayerModel.osu_id).where(PlayerModel.osu_id == osu_id)
        potential_user = await self.app.database.db.scalar(query)
        if potential_user:
            return True
        return False

    async def add_new_admin(self, osu_id: int) -> None:
        """Adds new admin with given osu_id and name from players database table"""
        query = select(PlayerModel).where(PlayerModel.osu_id == osu_id)
        player = await self.app.database.db.scalar(query)
        new_admin = AdminModel(osu_id=player.osu_id, name=player.name)
        async with self.app.database.db as session:
            session.add_all([new_admin])
            try:
                await session.commit()
            except IntegrityError:
                pass
        await self.cache_new_admin(osu_id)

    async def remove_admin(self, osu_id: int) -> None:
        """Removes admin from admins database table and from Redis cache"""
        query = select(AdminModel).where(AdminModel.osu_id == osu_id)
        admin = await self.app.database.db.scalar(query)
        async with self.app.database.db as session:
            await session.delete(admin)
            await session.commit()
        await self.remove_admin_id_from_cache(osu_id)

    async def remove_admin_id_from_cache(self, osu_id: int) -> None:
        """Removes specified osu_id from Redis cache"""
        await self.app.store.redis.lrem("admins", 0, osu_id)

    async def cache_new_admin(self, osu_id: int) -> None:
        """Adds specified osu_id to admin list in Redis cache if it's not in there yet"""
        admin_ids = await self.get_admin_ids_list()
        if osu_id not in admin_ids:
            await self.app.store.redis.rpush("admins", osu_id)

    async def get_admin_ids_list(self) -> list[int]:
        """Returns list of osu_ids that belong to admin from Redis cache"""
        byte_admin_ids = await self.app.store.redis.lrange("admins", 0, -1)
        admin_ids = [int(aid) for aid in byte_admin_ids if aid]  # Transforms list[byte] into list[int]
        return admin_ids

    async def get_admins(self):
        """Returns list of AdminModel out of all records in admins database table"""
        models = await self.app.database.db.execute(select(AdminModel))
        admins = models.scalars().all()
        return [a.to_dc() for a in admins if a]

    async def cache_admins_on_startup(self):  # TODO cache on startup
        pass