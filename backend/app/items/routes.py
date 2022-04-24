from aiohttp.web_app import Application


def setup_routes(app: "Application"):
    from backend.app.items.views import GetItemListView

    app.router.add_view("/api/items/{item_type}", GetItemListView)

