import typing
from typing import Optional

from osu import AsynchronousClient, AuthHandler, Scope
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from backend.app.store.base.base_accessor import BaseAccessor
from backend.app.store.database.models import PlayerModel

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class AuthAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, "Auth", *args, **kwargs)
        self.app = app
        self.auth: Optional[AuthHandler] = None
        self.session_factory: Optional[sessionmaker] = None

    async def connect(self, app: "Application"):
        self.session_factory = self.app.database.db
        self.auth = AuthHandler(
            client_id=self.app.config.credentials.client_id,
            client_secret=self.app.config.credentials.client_secret,
            redirect_url=f"{self.app.config.credentials.server_name}/callback",
            scope=Scope.identify(),
        )

    async def identify_player(self, oauth_code: str) -> dict:
        self.auth.get_auth_token(oauth_code)
        osu_api_client = AsynchronousClient(self.auth)
        user = await osu_api_client.get_own_data("osu")

        if user.statistics.global_rank is None and user.statistics.pp == 0:
            is_active = False
        else:
            is_active = True

        return {
            "osu_id": user.id,
            "name": user.username,
            "global_rank": user.statistics.global_rank,
            "performance": round(user.statistics.pp),
            "country_code": user.country_code,
            "is_restricted": user.is_restricted,
            "is_active": is_active,
        }

    async def add_or_update_player(self, player: dict) -> None:
        try:
            await self.add_player(player)
        except IntegrityError:
            await self.update_player(player)

    async def add_player(self, player: dict) -> None:
        new_player = PlayerModel(
            osu_id=player["osu_id"],
            name=player["name"],
            global_rank=player["global_rank"],
            performance=player["performance"],
            country_code=player["country_code"],
            is_restricted=player["is_restricted"],
            is_active=player["is_active"],
            is_banned=False,
            updated_by="",
        )
        async with self.session_factory() as session:
            session.add_all([new_player])
            await session.commit()

    async def update_player(self, player: dict) -> None:
        osu_id = player["osu_id"]

        if player["is_active"] is False:
            player.pop("performance")
            player.pop("global_rank")
        player.pop("osu_id")

        query = update(PlayerModel).where(PlayerModel.osu_id == osu_id).values(**player)
        async with self.session_factory() as session:
            await session.execute(query)
            await session.commit()
            self.logger.info("Stats updated")
