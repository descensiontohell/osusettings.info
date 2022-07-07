from backend.app.web.app import Application


def setup_routes(app: Application):
    from backend.app.auth.views import AuthView

    app.router.add_view("/callback", AuthView)
