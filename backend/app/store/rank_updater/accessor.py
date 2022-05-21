from typing import Optional

from aiohttp import ClientSession, TCPConnector
from sqlalchemy import select, update

from backend.app.store.base.base_accessor import BaseAccessor
from backend.app.store.database.models import PlayerModel
from backend.app.store.rank_updater.player_stats import PlayerStats
from backend.app.store.rank_updater.poller import RankPoller
from backend.app.web.app import Application


class RankUpdater(BaseAccessor):
    def __init__(self, app: "Application", **kwargs):
        super().__init__(app=app, name=kwargs.get("name"))
        self.app = app
        self.session: Optional[ClientSession] = None
        self.update_token_in: int = 0
        self.access_token: Optional[str] = None
        self.client_id = app.config.credentials.client_id
        self.client_secret = app.config.credentials.client_secret
        self.grant_type = app.config.credentials.grant_type
        self.scope = app.config.credentials.scope
        self.poller = RankPoller(app)

    async def connect(self, app):
        self.session = ClientSession(connector=TCPConnector(verify_ssl=True))
        await self.get_access_token()
        await self.poller.start()

    async def get_access_token(self):
        async with self.session.post(
                url=self.app.const.TOKEN_API_PATH,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": self.grant_type,
                    "scope": self.scope,
                },
        ) as resp:
            data = await resp.json()
            self.update_token_in = data["expires_in"] - self.app.const.TOKEN_EXPIRE_HANDICAP
            self.access_token = data["access_token"]

    async def get_players_ids(self) -> list[int]:
        query = select(PlayerModel.osu_id).order_by(PlayerModel.global_rank)
        result = await self.app.database.db.execute(query)
        ids_list = result.scalars().all()
        return ids_list

    async def request_player_stats(self, osu_id: int) -> PlayerStats:
        async with self.session.get(
            url=self.app.const.PLAYER_STATS_PATH.format(osu_id=osu_id),
            headers={"Authorization": f"Bearer {self.access_token}"}
        ) as resp:
            if resp.status == 404:
                return PlayerStats(osu_id=osu_id, is_restricted=True)
            data = await resp.json()
            return PlayerStats(
                name=data["username"],
                osu_id=osu_id,
                global_rank=data["statistics"]["global_rank"],
                performance=data["statistics"]["pp"],
                is_restricted=False,
            )

    async def update_player(self, stats: PlayerStats) -> None:
        if stats.is_restricted:  # if player is restricted
            return await self._set_restricted(stats)
        if stats.performance == 0 and stats.global_rank is None:  # if player is inactive
            return await self._set_inactive(stats)
        await self._set_new_player_stats(stats)

    async def _set_inactive(self, stats: PlayerStats) -> None:
        query = update(PlayerModel).where(PlayerModel.osu_id == stats.osu_id).values(is_active=False, is_restricted=False)
        await self.app.database.db.execute(query)
        await self.app.database.db.commit()

    async def _set_restricted(self, stats: PlayerStats) -> None:
        query = update(PlayerModel).where(PlayerModel.osu_id == stats.osu_id).values(is_restricted=True)
        await self.app.database.db.execute(query)
        await self.app.database.db.commit()

    async def _set_new_player_stats(self, stats: PlayerStats) -> None:
        update_columns = {"is_restricted": False}
        if stats.name:
            update_columns["name"] = stats.name
        if stats.global_rank:
            update_columns["global_rank"] = stats.global_rank
        if stats.performance:
            update_columns["performance"] = stats.performance

        query = update(PlayerModel).where(PlayerModel.osu_id == stats.osu_id).values(**update_columns)
        await self.app.database.db.execute(query)
        await self.app.database.db.commit()
