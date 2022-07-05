import asyncio
import os

from backend.rank_updater.poller import RankPoller

if os.environ.get("IS_IN_DOCKER", False):
    config_name = "config.yml"
else:
    config_name = "config_local.yml"

poller = RankPoller(config_path=os.path.join(os.path.abspath("."), config_name))

asyncio.run(poller.poll())
