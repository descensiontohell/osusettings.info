import typing

from backend.app.store.database.database import Database

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from backend.app.store.service_api.service_api import ServiceAccessor
        from backend.app.store.leaderboard.accessor import LeaderboardAccessor
        from backend.app.store.users.accessor import UserAccessor
        from backend.app.store.items.accessor import ItemsAccessor
        from backend.app.store.redis.redis import setup_redis
        from backend.app.store.auth.accessor import AuthAccessor

        self.redis = setup_redis(app)
        self.service = ServiceAccessor(app)
        self.leaderboard = LeaderboardAccessor(app)
        self.users = UserAccessor(app)
        self.items = ItemsAccessor(app)
        self.auth = AuthAccessor(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.store = Store(app)
    app.on_cleanup.append(app.database.disconnect)
