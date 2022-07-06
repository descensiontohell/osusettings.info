from aiohttp.web_app import Application


def setup_routes(app: "Application"):
    from backend.app.leaderboard.views import ApiPlayersView
    from backend.app.leaderboard.views import LeaderboardView

    app.router.add_view("/api/players", ApiPlayersView)
    app.router.add_view("/", LeaderboardView)
