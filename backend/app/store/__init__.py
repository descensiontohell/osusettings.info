import typing

from backend.app.store.database.database import Database


if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from backend.app.store.service_api.service_api import ServiceAccessor
        from backend.app.store.players.accessor import PlayersAccessor

        self.service = ServiceAccessor(app)
        self.players = PlayersAccessor(app)

def setup_store(app: "Application"):
    app.database = Database(app)
    app.store = Store(app)
    app.on_cleanup.append(app.database.disconnect)
    app.on_startup.append(app.database.connect)

