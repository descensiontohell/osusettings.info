import asyncio
import logging
from logging import getLogger

from requests import HTTPError
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.app.store.database.models import PlayerModel
from backend.app.web.player_stats import PlayerStats
from backend.rank_updater.config import get_config
from backend.rank_updater.osu_api import setup_osu_api


class RankUpdater:
    def __init__(self, config_path):
        logging.basicConfig(level=logging.INFO)
        self.config = get_config(config_path)
        self.osu_api = setup_osu_api(self.config)
        self.logger = getLogger("RANKS")
        self.get_connection()

    def get_connection(self):
        try:
            self._engine = create_async_engine(
                f"postgresql+asyncpg://{self.config.database.user}:{self.config.database.password}@\
{self.config.database.host}/{self.config.database.database}",
                pool_size=20,
                max_overflow=0,
            )
        except Exception as e:
            self.logger.error("Exception", exc_info=e)
        self.db_session = sessionmaker(
            self._engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def get_players_ids(self) -> list[int]:
        query = select(PlayerModel.osu_id).order_by(PlayerModel.global_rank)
        async with self.db_session() as session:
            result = await session.execute(query)
        ids_list = result.scalars().all()
        if not ids_list:
            await asyncio.sleep(1)
        self.logger.info("Acquired list of player ids")
        return ids_list

    async def request_player_stats(self, osu_id: int) -> PlayerStats:
        try:
            user = await self.osu_api.get_user(user=osu_id, mode="osu")
        except HTTPError:  # api wrapper raises 404 HTTPError if user is restricted
            return PlayerStats(osu_id=osu_id, is_restricted=True)

        name = user.username
        global_rank = user.statistics.global_rank
        performance = round(user.statistics.pp)

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
