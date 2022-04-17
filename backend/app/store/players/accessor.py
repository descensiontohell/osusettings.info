import typing

from aiohttp.web_exceptions import HTTPBadRequest
from multidict._multidict import MultiDictProxy
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload, joinedload

from backend.app.store.database.models import PlayerModel, SuperuserModel, MousepadModel, MouseModel, KeyboardModel, \
    SwitchModel, TabletModel
from backend.app.store.base.base_accessor import BaseAccessor
from backend.app.store.service_api.dataclasses import Superuser

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class PlayersAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, "Players", *args, **kwargs)
        self.app = app
        self.page_size = 50
        self.filters = ["is_mouse", "playstyle", "page", "name", "country",
                        "min_edpi", "max_edpi", "min_area_width", "min_area_height", "max_area_width",
                        "max_area_height", "mouse", "mousepad", "tablet", "keyboard", "switch"]
        self.int_filters = ["is_mouse", "playstyle", "page",
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
                    raise HTTPBadRequest(reason=f"{key} should contain a single integer")
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

        if name is not None:
            name = f"%{name}%"
            query = query.filter(PlayerModel.name.ilike(name))

        if country is not None:
            query = query.filter(PlayerModel.country_code == country)

        if min_edpi is not None:
            query = query.filter(PlayerModel.mouse_edpi >= min_edpi)
        if max_edpi is not None:
            query = query.filter(PlayerModel.mouse_edpi <= max_edpi)

        if min_area_width is not None:
            query = query.filter(PlayerModel.tablet_area_width >= min_area_width)
        if min_area_height is not None:
            query = query.filter(PlayerModel.tablet_area_height >= min_area_height)
        if max_area_width is not None:
            query = query.filter(PlayerModel.tablet_area_width <= max_area_width)
        if max_area_height is not None:
            query = query.filter(PlayerModel.tablet_area_height <= max_area_height)

        if mouse is not None:
            mouse = f"%{mouse}%"
            query = query.join(PlayerModel.mouse).filter(or_(MouseModel.brand.ilike(mouse), MouseModel.model.ilike(mouse)))

        if mousepad is not None:
            mousepad = f"%{mousepad}%"
            query = query.join(PlayerModel.mousepad).filter(MousepadModel.name.ilike(mousepad))

        if keyboard is not None:
            keyboard = f"%{keyboard}%"
            query = query.join(PlayerModel.keyboard).filter(or_(KeyboardModel.brand.ilike(keyboard), KeyboardModel.model.ilike(keyboard)))

        if switch is not None:
            switch = f"%{switch}%"
            query = query.join(PlayerModel.switch).filter(SwitchModel.name.ilike(switch))

        if tablet is not None:
            tablet = f"%{tablet}%"
            query = query.join(PlayerModel.tablet).filter(TabletModel.name.ilike(tablet))

        players = (query
                  .options(selectinload(PlayerModel.mousepad))
                  .options(selectinload(PlayerModel.mouse))
                  .options(selectinload(PlayerModel.playstyle))
                  .options(selectinload(PlayerModel.keyboard))
                  .options(selectinload(PlayerModel.tablet))
                  .options(selectinload(PlayerModel.switch))
                  .limit(self.page_size).offset((page-1)*self.page_size))

        result = await self.app.database.db.execute(players)

        models = result.scalars().all()

        return [m.to_dc() for m in models]
