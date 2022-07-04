import typing

from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from backend.app.leaderboard.filter import LeaderboardFilter
from backend.app.store.database.models import PlayerModel, MousepadModel, MouseModel, KeyboardModel, \
    SwitchModel, TabletModel
from backend.app.store.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class PlayersAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, "Players", *args, **kwargs)
        self.app = app
        self.page_size = 50

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
