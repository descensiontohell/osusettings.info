import typing

from aiohttp.web_exceptions import HTTPBadRequest
from multidict import MultiDictProxy
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload, joinedload

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
        self.filters = ["order_by", "min_rank", "max_rank", "is_mouse", "playstyle", "page", "name", "country",
                        "min_edpi", "max_edpi", "min_area_width", "min_area_height", "max_area_width",
                        "max_area_height", "mouse", "mousepad", "tablet", "keyboard", "switch"]
        self.int_filters = ["min_rank", "max_rank", "is_mouse", "playstyle", "page",
                            "min_edpi", "max_edpi", "min_area_width", "min_area_height", "max_area_width",
                            "max_area_height"]

    def parse_filters(self, query: MultiDictProxy) -> dict:
        result = {}
        try:
            if query["is_mouse"] == "true":
                is_mouse = True
            else:
                is_mouse = False
        except KeyError:
            is_mouse = True
            result["is_mouse"] = is_mouse

        for key in query:
            if key not in self.filters:
                continue
            if key == "is_mouse":
                result["is_mouse"] = is_mouse
                continue
            if key == "playstyle":
                ps_list = query[key].split(",")
                try:
                    ps = [int(v) for v in ps_list]
                    result["playstyle"] = ps
                    continue
                except ValueError:
                    raise HTTPBadRequest(reason="Playstyle should contain a single integer or comma separated integers")
            if key in self.int_filters:
                try:
                    result[key] = int(query[key])
                    continue
                except ValueError:
                    raise HTTPBadRequest(reason=f"{key} should be a number")
            else:
                result[key] = query[key]
        for key in query:
            if is_mouse and key in ["min_area_width", "min_area_height", "max_area_width", "max_area_height", "tablet"]:
                result.pop(key, None)
            if not is_mouse and key in ["min_edpi", "max_edpi", "mouse", "mousepad"]:
                result.pop(key, None)
        return result

    async def get_players(
            self,
            is_mouse: bool,
            order_by: str = None,
            min_rank: int = None,
            max_rank: int = None,
            playstyle: list[int] = None,
            page: int = 1,
            name: str = None,
            country: str = None,
            min_edpi: int = None,
            max_edpi: int = None,
            min_area_width: int = None,
            min_area_height: int = None,
            max_area_width: int = None,
            max_area_height: int = None,
            mouse: str = None,
            mousepad: str = None,
            tablet: str = None,
            keyboard: str = None,
            switch: str = None,
    ):

        query = select(PlayerModel)

        if is_mouse is not None:
            query = query.filter(PlayerModel.is_mouse == is_mouse)

        if playstyle is not None:
            query = query.filter(PlayerModel.playstyle_id.in_(playstyle))

        # If name and ranks not specified, set default rank constraints
        # If name is specified and ranks are not, rank constraints are None
        # If name and rank constraints are specified, use them
        if not min_rank and not max_rank and not name:
            min_rank = self.app.const.MIN_RANK
            max_rank = self.app.const.MAX_RANK

        if not order_by:
            order_by = PlayerModel.performance.desc()
        elif order_by == "pp":
            order_by = PlayerModel.performance.desc()
        elif order_by == "-pp":
            order_by = PlayerModel.performance
        elif order_by == "edpi":
            order_by = PlayerModel.mouse_edpi
        elif order_by == "-edpi":
            query = query.filter(PlayerModel.mouse_edpi.is_not(None))
            order_by = PlayerModel.mouse_edpi.desc()

        if name is not None:
            query = query.filter(PlayerModel.name.ilike(f"%{name}%"))

        if country is not None:
            query = query.filter(PlayerModel.country_code == country)

        if min_edpi is not None:
            query = query.filter(PlayerModel.mouse_edpi >= min_edpi)
        if max_edpi is not None:
            query = query.filter(PlayerModel.mouse_edpi <= max_edpi)

        if min_rank is not None:
            query = query.filter(PlayerModel.global_rank >= min_rank)
        if max_rank is not None:
            query = query.filter(PlayerModel.global_rank <= max_rank)

        if min_area_width is not None:
            query = query.filter(PlayerModel.tablet_area_width >= min_area_width)
        if min_area_height is not None:
            query = query.filter(PlayerModel.tablet_area_height >= min_area_height)
        if max_area_width is not None:
            query = query.filter(PlayerModel.tablet_area_width <= max_area_width)
        if max_area_height is not None:
            query = query.filter(PlayerModel.tablet_area_height <= max_area_height)

        if mouse is not None:
            query = query.join(PlayerModel.mouse).filter(
                or_(MouseModel.brand.ilike(f"%{mouse}%"), MouseModel.model.ilike(f"%{mouse}%")))

        if mousepad is not None:
            query = query.join(PlayerModel.mousepad).filter(MousepadModel.name.ilike(f"%{mousepad}%"))

        if keyboard is not None:
            query = query.join(PlayerModel.keyboard).filter(
                or_(KeyboardModel.brand.ilike(f"%{keyboard}%"), KeyboardModel.model.ilike(f"%{keyboard}%")))

        if switch is not None:
            query = query.join(PlayerModel.switch).filter(SwitchModel.name.ilike(f"%{switch}%"))

        if tablet is not None:
            query = query.join(PlayerModel.tablet).filter(TabletModel.name.ilike(f"%{tablet}%"))

        players = (query
                   .options(selectinload(PlayerModel.mousepad))
                   .options(selectinload(PlayerModel.mouse))
                   .options(selectinload(PlayerModel.playstyle))
                   .options(selectinload(PlayerModel.keyboard))
                   .options(selectinload(PlayerModel.tablet))
                   .options(selectinload(PlayerModel.switch))
                   .order_by(order_by)
                   .limit(self.page_size)
                   .offset((page - 1) * self.page_size))

        result = await self.app.database.db.execute(players)

        models = result.scalars().all()

        return [m.to_dc() for m in models]
