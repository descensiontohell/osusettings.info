from backend.app.web.app import Application


def setup_routes(app: Application):
    from backend.app.items.views import GetAllItemsView, GetItemListView

    app.router.add_view("/api/items", GetAllItemsView)
    app.router.add_view("/api/items/{item_type}", GetItemListView)
