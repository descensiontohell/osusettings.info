import typing

from backend.app.store.base.base_accessor import BaseAccessor


if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class AuthAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, "Auth", *args, **kwargs)
        self.app = app

    async def connect(self, app: "Application"):
        ...
