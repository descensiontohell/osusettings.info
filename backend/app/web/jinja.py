import typing

import aiohttp_jinja2
import jinja2

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


def setup_jinja(app: "Application"):
    aiohttp_jinja2.setup(app, enable_async=True, loader=jinja2.FileSystemLoader("frontend"))
    app["static_root_url"] = "static"
