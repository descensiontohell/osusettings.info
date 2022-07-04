from requests import HTTPError
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
        self.poller = RankPoller(app)

        await self.poller.start()
        self.db_session = self.app.database.db  # Is callable because it's a factory

    async def get_players_ids(self) -> list[int]:
        query = select(PlayerModel.osu_id).order_by(PlayerModel.global_rank)
        async with self.db_session() as session:
            result = await session.execute(query)
        ids_list = result.scalars().all()
        self.logger.info("Acquired list of player ids")
        return ids_list

    async def request_player_stats(self, osu_id: int) -> PlayerStats:
        self.logger.info(f"Requesting stats {osu_id}")
        try:
            user = await self.app.store.osu_api.get_user(user=osu_id, mode="osu")
        except HTTPError:  # api wrapper raises 404 HTTPError if user is restricted
            return PlayerStats(osu_id=osu_id, is_restricted=True)

        name = user.username
        global_rank = user.statistics.global_rank
        performance = round(user.statistics.pp)
        self.logger.info(f"Stats {osu_id} obtained")

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
        self.logger.info(f"Stats for update: {stats}")
        query = update(PlayerModel).where(PlayerModel.osu_id == stats.osu_id).values(**stats.to_dict())
        async with self.db_session() as session:
            await session.execute(query)
            await session.commit()
            self.logger.info("Stats updated")
