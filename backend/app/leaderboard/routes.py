from backend.app.web.app import Application


def setup_routes(app: Application):
    from backend.app.leaderboard.views import ApiLeaderboardView, LeaderboardView, SinglePlayerView

    app.router.add_view("/api/players", ApiLeaderboardView)
    app.router.add_view("/api/players/{osu_id}", SinglePlayerView)
    app.router.add_view("/", LeaderboardView)
