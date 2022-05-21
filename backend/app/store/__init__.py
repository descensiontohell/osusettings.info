import typing

from backend.app.store.database.database import Database

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from backend.app.store.service_api.service_api import ServiceAccessor
        from backend.app.store.players.accessor import PlayersAccessor
        from backend.app.store.items.accessor import ItemsAccessor
        from backend.app.store.redis.redis import setup_redis
        from backend.app.store.rank_updater.accessor import RankUpdater

        self.redis = setup_redis(app)
        self.rank_updater = RankUpdater(app)
        self.service = ServiceAccessor(app)
        self.players = PlayersAccessor(app)
        self.items = ItemsAccessor(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.store = Store(app)
    app.on_cleanup.append(app.database.disconnect)
    app.on_startup.append(app.database.connect)
