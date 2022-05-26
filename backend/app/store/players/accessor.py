import typing

from aiohttp.web_exceptions import HTTPBadRequest
from multidict import MultiDictProxy
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload, joinedload

from backend.app.leaderboard.filter import LeaderboardFilter
from backend.app.store.database.models import PlayerModel, SuperuserModel, MousepadModel, MouseModel, KeyboardModel, \
    SwitchModel, TabletModel
from backend.app.store.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class PlayersAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, "Players", *args, **kwargs)
        self.app = app
        self.page_size = 50
#        self.filters = ["order_by", "min_rank", "max_rank", "is_mouse", "playstyle", "page", "name", "country",
#                        "min_edpi", "max_edpi", "min_area_width", "min_area_height", "max_area_width",
#                        "max_area_height", "mouse", "mousepad", "tablet", "keyboard", "switch"]
#        self.int_filters = ["min_rank", "max_rank", "is_mouse", "playstyle", "page",
#                            "min_edpi", "max_edpi", "min_area_width", "min_area_height", "max_area_width",
#                            "max_area_height"]

    async def connect(self, app: "Application"):
        self.session_factory = self.app.database.db

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
            query = query.filter(PlayerModel.global_rank >= pf.min_rank)
        if pf.max_rank is not None:
            query = query.filter(PlayerModel.global_rank <= pf.max_rank)

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

#    def parse_filters(self, query: MultiDictProxy) -> dict:
#        result = {}
#        try:
#            if query["is_mouse"] == "true":
#                is_mouse = True
#            else:
#                is_mouse = False
#        except KeyError:
#            is_mouse = True
#            result["is_mouse"] = is_mouse
#
#        for key in query:
#            if key not in self.filters:
#                continue
#            if key == "is_mouse":
#                result["is_mouse"] = is_mouse
#                continue
#            if key == "playstyle":
#                ps_list = query[key].split(",")
#                try:
#                    ps = [int(v) for v in ps_list]
#                    result["playstyle"] = ps
#                    continue
#                except ValueError:
#                    raise HTTPBadRequest(reason="Playstyle should contain a single integer or comma separated integers")
#            if key in self.int_filters:
#                try:
#                    result[key] = int(query[key])
#                    continue
#                except ValueError:
#                    raise HTTPBadRequest(reason=f"{key} should be a number")
#            else:
#                result[key] = query[key]
#        for key in query:
#            if is_mouse and key in ["min_area_width", "min_area_height", "max_area_width", "max_area_height", "tablet"]:
#                result.pop(key, None)
#            if not is_mouse and key in ["min_edpi", "max_edpi", "mouse", "mousepad"]:
#                result.pop(key, None)
#        return result
