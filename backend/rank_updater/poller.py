import asyncio

from backend.rank_updater.accessor import RankUpdater


class RankPoller:
    def __init__(self, config_path):
        self.accessor = RankUpdater(config_path)

    async def poll(self):
        while True:
            list_of_ids = await self.accessor.get_players_ids()

            for player_id in list_of_ids:
                stats = await self.accessor.request_player_stats(player_id)
                await self.accessor.update_player(stats)
                await asyncio.sleep(0.5)
