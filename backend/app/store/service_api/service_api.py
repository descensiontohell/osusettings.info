import typing

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.app.players.models import PlayerModel
from backend.app.store.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class ServiceAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, "API", *args, **kwargs)
        self.app = app

    async def connect(self, app: "Application"):
        pass

    async def test(self):
        players = select(PlayerModel).options(selectinload(PlayerModel.playstyle), selectinload(PlayerModel.mouse))
        res = (await self.app.database.db.scalar(players))
        print(res)
        print(res.playstyle)
        print(res.name)
        print(res.mouse.model)
        print(res.to_dc())
