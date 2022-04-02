from typing import Optional
from aiohttp.web import (
    Application as AiohttpApplication,
    View as AiohttpView,
    Request as AiohttpRequest,
)

from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_session import setup as setup_session
from aioredis.client import Redis
from aiohttp_session.redis_storage import RedisStorage

from backend.app.web.redis import setup_redis
from backend.app.web.logger import setup_logging
from backend.app.store import setup_store, Store
from backend.app.store.database.database import Database
from backend.app.web.config import Config, setup_config
#from middlewares import setup_middlewares
#from routes import setup_routes
from backend.app.web.routes import setup_routes


class Application(AiohttpApplication):
    config: Optional[Config] = None
    store: Optional[Store] = None
    database: Optional[Database] = None
    redis: Optional[Redis] = None


class Request(AiohttpRequest):
    player_name: Optional[str] = None
    player_id: Optional[int] = None

    @property
    def app(self) -> "Application":
        return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def store(self) -> Store:
        return self.request.app.store


app = Application()


def setup_app(config_path: str) -> Application:
    setup_logging(app)
    setup_config(app, config_path)
    setup_routes(app)
    setup_redis(app)
    setup_session(app, RedisStorage(app.redis))
    setup_aiohttp_apispec(app, title="osusettings", url="/api/docs/json", swagger_path="/api/docs")
 #   setup_middlewares(app)
    setup_store(app)
    return app





