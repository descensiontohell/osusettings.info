import typing
from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class Database:

    def __init__(self, app: "Application"):
        self.app = app
        self.db: Optional[AsyncSession] = None

    async def connect(self, *_, **kw):
        try:
            self._engine = create_async_engine(
                f"postgresql+asyncpg://elle_dev:dev_elle_pass@localhost:5432/dev_osu"
            )
        except Exception as e:
            self.app.logger.error("Exception", exc_info=e)
        self.db = AsyncSession(self._engine)

    async def disconnect(self, *_, **kw):
        if self.db:
            await self.db.pop_bind().close()
            self._engine = None
            self.db: Optional[AsyncSession] = None

