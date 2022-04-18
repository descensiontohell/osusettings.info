from aiohttp.web_app import Application


def setup_routes(app: "Application"):

    from backend.app.leaderboard.views import GetPlayersView
    app.router.add_view("/api/players.get", GetPlayersView)

