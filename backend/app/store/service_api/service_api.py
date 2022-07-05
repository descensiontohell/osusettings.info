import typing
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from backend.app.store.players.dataclasses import Player
from backend.app.store.service_api.player_edpi import PlayerEdpi
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
        self.session = self.app.database.db()

    async def get_su_by_name(self, name: str) -> Optional[Superuser]:
        """Get superuser credentials from database table by name"""
        query = select(SuperuserModel).where(name == SuperuserModel.name)
        async with self.session as s:
            superuser = (await s.execute(query)).scalar()
        if superuser is not None:
            return superuser.to_dc()
        return None

    async def is_user_in_admins_list(self, osu_id: int) -> bool:
        """Checks if specified osu_id belongs to admin in Redis cache"""
        return osu_id in await self.get_admin_ids_list()

    async def user_exists(self, osu_id: int) -> bool:
        """Checks if user with specified osu_id exists in players database table"""
        query = select(PlayerModel.osu_id).where(PlayerModel.osu_id == osu_id)
        async with self.session as s:
            potential_user = (await s.execute(query)).scalar()
        if potential_user:
            return True
        return False

    async def add_new_admin(self, osu_id: int) -> None:
        """Adds new admin with given osu_id and name from players database table"""
        query = select(PlayerModel).where(PlayerModel.osu_id == osu_id)
        async with self.session as s:
            player = (await s.execute(query)).scalar()
        new_admin = AdminModel(osu_id=player.osu_id, name=player.name)
        async with self.session as session:
            session.add_all([new_admin])
            try:
                await session.commit()
            except IntegrityError:
                pass

    async def remove_admin(self, osu_id: int) -> None:
        """Removes admin from admins database table and from Redis cache"""
        query = select(AdminModel).where(AdminModel.osu_id == osu_id)
        async with self.session as s:
            admin = (await s.execute(query)).scalar()
        async with self.session as session:
            await session.delete(admin)
            await session.commit()

    async def get_admin_ids_list(self) -> list[int]:
        """Returns list of osu_ids that belong to admin from Redis cache"""
        admins = await self.get_admins()
        return [a.osu_id for a in admins]

    async def get_admins(self):
        """Returns list of AdminModel out of all records in admins database table"""
        async with self.session as s:
            models = await s.execute(select(AdminModel))
        admins = models.scalars().all()
        return [a.to_dc() for a in admins if a]

    async def update_players_edpi(self) -> None:
        player_models = await self.get_all_player_models()
        for model in player_models:
            player_edpi = self.assign_according_edpi(model)
            await self.update_edpi_for_player(player_edpi)

    async def get_all_player_models(self) -> list[Player]:
        async with self.session as s:
            query = (select(PlayerModel)
                     .options(selectinload(PlayerModel.mousepad))
                     .options(selectinload(PlayerModel.mouse))
                     .options(selectinload(PlayerModel.playstyle))
                     .options(selectinload(PlayerModel.keyboard))
                     .options(selectinload(PlayerModel.tablet))
                     .options(selectinload(PlayerModel.switch))
                     )
            models = (await s.execute(query)).scalars().all()
        return [m.to_dc() for m in models]

    async def update_edpi_for_player(self, player_edpi: PlayerEdpi) -> None:
        query = update(PlayerModel).where(PlayerModel.osu_id == player_edpi.osu_id).values(**player_edpi.to_dict())
        async with self.session as session:
            await session.execute(query)
            await session.commit()

    def assign_according_edpi(self, player: Player) -> PlayerEdpi:
        windows_sens_grades = [1/32, 1/16, 1/4, 1/2, 3/4, 1, 1.5, 2, 2.5, 3, 3.5]
        edpi = None
        play_area_height = None
        play_area_width = None
        dpi = player.dpi
        sens = player.multiplier
        os_sens = player.os_sens
        raw = player.raw_input
        res_height = player.res_height

        if sens is not None and res_height is not None and dpi is not None:
            if raw is True:
                base_edpi = dpi * sens
                res_ratio = 1080 / res_height
                edpi = base_edpi * res_ratio
                play_area_height = round((res_height / base_edpi) * 25.4)
                play_area_width = round(play_area_height * 4 / 3)

            elif os_sens is not None:
                os_multiplier = windows_sens_grades[os_sens-1]
                base_edpi = dpi * sens * os_multiplier
                res_ratio = 1080 / res_height
                edpi = base_edpi * res_ratio
                play_area_height = round((res_height / base_edpi) * 25.4)
                play_area_width = round(play_area_height * 4 / 3)

        return PlayerEdpi(
            osu_id=player.osu_id,
            edpi=edpi,
            area_width=play_area_width,
            area_height=play_area_height,
        )
