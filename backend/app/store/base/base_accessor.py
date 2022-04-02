import typing
from logging import getLogger

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class BaseAccessor:
    def __init__(self, app: "Application", name: str = None, *args, **kwargs):
        self.app = app
        if name is not None:
            self.logger = getLogger(name)
        else:
            self.logger = getLogger("accessor")
        app.on_startup.append(self.connect)
        app.on_cleanup.append(self.disconnect)

    async def connect(self, app: "Application"):
        return

    async def disconnect(self, app: "Application"):
        return

