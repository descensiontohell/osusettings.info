import asyncio
from asyncio import Task
from typing import Optional

from backend.app.web.app import Application


class RankPoller:
    def __init__(self, app: "Application"):
        self.app = app
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        self.is_running = True
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self):
        self.is_running = False
        await self.poll_task

    async def poll(self):
        while self.is_running:
            list_of_ids = await self.app.store.rank_updater.get_players_ids()

            for player_id in list_of_ids:
                stats = await self.app.store.rank_updater.request_player_stats(player_id)
                await self.app.store.rank_updater.update_player(stats)
                await asyncio.sleep(1)
