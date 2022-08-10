import typing
from typing import Optional

from aiohttp.web_exceptions import HTTPBadRequest
from osu import AsynchronousClient
from sqlalchemy import select, or_, desc
from sqlalchemy.orm import selectinload

from backend.app.players.filter import LeaderboardFilter
from backend.app.store.database.models import PlayerModel, MousepadModel, MouseModel, KeyboardModel, \
    SwitchModel, TabletModel, SettingsModel
from backend.app.store.base.base_accessor import BaseAccessor
from backend.app.store.players.dataclasses import Player, Settings

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class PlayerAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, "Players", *args, **kwargs)
        self.app = app
        self.client_id = self.app.config.credentials.client_id
        self.client_secret = self.app.config.credentials.client_secret
        self.redirect_url = f"{self.app.config.credentials.server_name}/callback"
        self.page_size = 50

    async def connect(self, app: "Application"):
        self.session_factory = self.app.database.db
        self.osu_api = AsynchronousClient.from_client_credentials(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_url=self.redirect_url,
        )

    async def get_players(self, player_filter: LeaderboardFilter):
        query = self._build_query(player_filter)
        async with self.session_factory() as session:
            models = await session.execute(query)
        result = models.scalars().all()
        return [r.to_dc() for r in result]

    def _build_query(self, pf: LeaderboardFilter):
        query = select(PlayerModel)
        if pf.is_mouse is not None:
            query = query.filter(PlayerModel.is_mouse == pf.is_mouse)

        if pf.playstyle is not None:
            query = query.filter(PlayerModel.playstyle_id.in_(pf.playstyle))

        # If name and ranks not specified, set default rank constraints
        # If name is specified and ranks are not, rank constraints are None
        # If name and rank constraints are specified, use them
        if not pf.min_rank and not pf.max_rank and not pf.name:
            pf.min_rank = self.app.const.MIN_RANK
            pf.max_rank = self.app.const.MAX_RANK

        if not pf.order_by:
            pf.order_by = PlayerModel.performance.desc()
        elif pf.order_by == "pp":
            pf.order_by = PlayerModel.performance.desc()
        elif pf.order_by == "-pp":
            pf.order_by = PlayerModel.performance
        elif pf.order_by == "edpi":
            pf.order_by = PlayerModel.mouse_edpi
        elif pf.order_by == "-edpi":
            query = query.filter(PlayerModel.mouse_edpi.is_not(None))
            pf.order_by = PlayerModel.mouse_edpi.desc()

        if pf.name is not None:
            query = query.filter(PlayerModel.name.ilike(f"%{pf.name}%"))

        if pf.country is not None:
            query = query.filter(PlayerModel.country_code == pf.country)

        if pf.min_edpi is not None:
            query = query.filter(PlayerModel.mouse_edpi >= pf.min_edpi)
        if pf.max_edpi is not None:
            query = query.filter(PlayerModel.mouse_edpi <= pf.max_edpi)

        if pf.min_rank is not None:
            query = query.filter(or_(PlayerModel.global_rank >= pf.min_rank, PlayerModel.global_rank == None))
        if pf.max_rank is not None:
            query = query.filter(or_(PlayerModel.global_rank <= pf.max_rank, PlayerModel.global_rank == None))

        if pf.min_area_width is not None:
            query = query.filter(PlayerModel.tablet_area_width >= pf.min_area_width)
        if pf.min_area_height is not None:
            query = query.filter(PlayerModel.tablet_area_height >= pf.min_area_height)
        if pf.max_area_width is not None:
            query = query.filter(PlayerModel.tablet_area_width <= pf.max_area_width)
        if pf.max_area_height is not None:
            query = query.filter(PlayerModel.tablet_area_height <= pf.max_area_height)

        if pf.mouse is not None:
            query = query.join(PlayerModel.mouse).filter(MouseModel.name.ilike(f"%{pf.mouse}%"))

        if pf.mousepad is not None:
            query = query.join(PlayerModel.mousepad).filter(MousepadModel.name.ilike(f"%{pf.mousepad}%"))

        if pf.keyboard is not None:
            query = query.join(PlayerModel.keyboard).filter(KeyboardModel.name.ilike(f"%{pf.keyboard}%"))

        if pf.switch is not None:
            query = query.join(PlayerModel.switch).filter(SwitchModel.name.ilike(f"%{pf.switch}%"))
        if pf.tablet is not None:
            query = query.join(PlayerModel.tablet).filter(TabletModel.name.ilike(f"%{pf.tablet}%"))

        players = (query
                   .options(selectinload(PlayerModel.mousepad))
                   .options(selectinload(PlayerModel.mouse))
                   .options(selectinload(PlayerModel.playstyle))
                   .options(selectinload(PlayerModel.keyboard))
                   .options(selectinload(PlayerModel.tablet))
                   .options(selectinload(PlayerModel.switch))
                   .order_by(pf.order_by)
                   .limit(self.page_size)
                   .offset((pf.page - 1) * self.page_size))

        return players

    async def get_user_by_osu_id_or_name(self, osu_id: int) -> Optional[Player]:
        query = (select(PlayerModel)
                 .filter(PlayerModel.osu_id == osu_id)
                 .options(selectinload(PlayerModel.mousepad))
                 .options(selectinload(PlayerModel.mouse))
                 .options(selectinload(PlayerModel.playstyle))
                 .options(selectinload(PlayerModel.keyboard))
                 .options(selectinload(PlayerModel.tablet))
                 .options(selectinload(PlayerModel.switch))
                 )

        async with self.session_factory() as session:
            models = await session.execute(query)
        result = models.scalars().first()

        if result:
            return result.to_dc()

    async def get_settings_history_by_osu_id(self, osu_id: int) -> list[Settings]:
        query = (select(SettingsModel)
                 .filter(SettingsModel.osu_id == osu_id)
                 .options(selectinload(SettingsModel.mousepad))
                 .options(selectinload(SettingsModel.mouse))
                 .options(selectinload(SettingsModel.playstyle))
                 .options(selectinload(SettingsModel.keyboard))
                 .options(selectinload(SettingsModel.tablet))
                 .options(selectinload(SettingsModel.switch))
                 .order_by(desc(SettingsModel.id))
                 )

        async with self.session_factory() as session:
            models = await session.execute(query)
        result = models.scalars().all()

        return [s.to_dc() for s in result if s]

    async def add_new_player(self, osu_id) -> None:
        player = await self.osu_api.get_user(user=osu_id)

        if player.statistics.global_rank is None and player.statistics.pp == 0:
            is_active = False
        else:
            is_active = True

        player_stats_dict = {
            "osu_id": player.id,
            "name": player.username,
            "global_rank": player.statistics.global_rank,
            "performance": round(player.statistics.pp),
            "country_code": player.country_code,
            "is_active": is_active,
            "is_restricted": False,
        }

        await self.app.store.auth.add_player(player_stats_dict)

    async def validate_update_player_data(self, data: dict) -> None:
        items = ["mouse", "mousepad", "tablet", "keyboard", "switch"]
        keys = list(data)
        for item in items:
            # If user provides add_new_mouse field they should also provide mouse field (and vice versa)
            # Otherwise 400 Bad Request
            if (f"add_new_{item}" not in keys and item in keys) or (f"add_new_{item}" in keys and item not in keys):
                raise HTTPBadRequest(text=f"If add_new_{item} field is provided you should also provide {item} field")

            item_content = data.get(item)
            if not item_content:
                continue

            # If user provides add_new_mouse field:
            # If add_new_mouse is True, mouse field should contain mouse name and specs and not id
            # If add_new_mouse if False, mouse field should only contain id
            item_keys = list(item_content)

            if data.get(f"add_new_{item}") is True:
                if "id" in item_keys or not "name" in item_keys:
                    raise HTTPBadRequest(text=f"If add_new_{item} is True, you should provide {item} specs and not id")

            if data.get(f"add_new_{item}") is False:
                if item_keys != ["id"]:
                    raise HTTPBadRequest(text=f"If add_new_{item} is False, you should provide {item} id and not specs")

        if "is_mouse" not in keys:
            raise HTTPBadRequest(text="Missing is_mouse field. It determines your playstyle and available device fields")

        elif data["is_mouse"] is True:
            if any([
                "tablet" in keys,
                "add_new_tablet" in keys,
                "tablet_area_height" in keys,
                "tablet_area_width" in keys,
            ]):
                raise HTTPBadRequest(text="Mouse player is not supposed to have tablet, "
                                          "add_new_tablet, tablet_area_height or tablet_area_width fields")

        elif data["is_mouse"] is False:
            if any([
                "mouse" in keys,
                "add_new_mouse" in keys,
                "dpi" in keys,
                "add_new_mousepad" in keys,
                "mousepad" in keys,
            ]):
                raise HTTPBadRequest(text="Tablet player is not supposed to have mouse, add_new_mouse, "
                                          "dpi, add_new_mousepad or mousepad fields")

        if all(["res_width" in keys, "res_height" in keys, data["res_height"] > data["res_width"]]):
            raise HTTPBadRequest(text="We expect your monitor resolution height to be less than resolution width")

        if "playstyle" in keys:
            playstyles = await self.app.store.items.get_playstyles(is_mouse=data["is_mouse"])
            playstyle_names = [p.name for p in playstyles]
            if data["playstyle"] not in playstyle_names:
                raise HTTPBadRequest(text="Specified playstyle does not match given is_mouse parameter")
