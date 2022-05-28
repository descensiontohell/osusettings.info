import asyncio
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
        self.db_session = self.app.database.db()  # Is callable because it's a factory
        asyncio.create_task(self._timer())

    async def _timer(self):
        while True:
            self.update_token_in -= 1
            if self.update_token_in <= 0:
                await self.get_access_token()
            await asyncio.sleep(1)

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
        async with self.db_session as session:
            result = await session.execute(query)
        ids_list = result.scalars().all()
        return ids_list

    async def request_player_stats(self, osu_id: int) -> PlayerStats:
        async with self.session.get(
            url=self.app.const.PLAYER_STATS_PATH.format(osu_id=osu_id),
            headers={"Authorization": f"Bearer {self.access_token}"}
        ) as resp:

            # If player is restricted
            if resp.status == 404:
                return PlayerStats(osu_id=osu_id, is_restricted=True)

            data = await resp.json()
            name = data["username"]
            global_rank = data["statistics"]["global_rank"]
            performance = round(data["statistics"]["pp"])

            # If player went inactive
            if global_rank is None and performance == 0:
                return PlayerStats(osu_id=osu_id, name=name, is_active=False, is_restricted=False)

            # If not restricted and not inactive: update rank, pp and name
            return PlayerStats(
                name=name,
                osu_id=osu_id,
                global_rank=global_rank,
                performance=performance,
                is_restricted=False,
                is_active=True,
            )

    async def update_player(self, stats: PlayerStats) -> None:
        self.logger.info(stats)
        query = update(PlayerModel).where(PlayerModel.osu_id == stats.osu_id).values(**stats.to_dict())
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

#    async def _set_inactive(self, stats: PlayerStats) -> None:
#        query = update(PlayerModel).where(PlayerModel.osu_id == stats.osu_id).values(is_active=False, is_restricted=False)
#        async with self.db_session as session:
#            await session.execute(query)
#            await session.commit()
#
#    async def _set_restricted(self, stats: PlayerStats) -> None:
#        query = update(PlayerModel).where(PlayerModel.osu_id == stats.osu_id).values(is_restricted=True)
#        async with self.db_session as session:
#            await session.execute(query)
#            await session.commit()
#
#    async def _set_new_player_stats(self, stats: PlayerStats) -> None:
#        update_columns = {"is_restricted": False, "is_active": True}
#        if stats.name:
#            update_columns["name"] = stats.name
#        if stats.global_rank:
#            update_columns["global_rank"] = stats.global_rank
#        if stats.performance:
#            update_columns["performance"] = stats.performance
#        print(update_columns)
#        query = update(PlayerModel).where(PlayerModel.osu_id == stats.osu_id).values(**update_columns)
#        async with self.db_session as session:
#            await session.execute(query)
#            await session.commit()
#