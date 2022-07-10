from backend.app.web.app import Application


def setup_routes(app: Application):
    from backend.app.players.views import (
        ApiLeaderboardView,
        LeaderboardView,
        SinglePlayerView,
        PlayerSettingsHistoryView,
    )

    app.router.add_view("/api/players", ApiLeaderboardView)
    app.router.add_view("/api/players/{osu_id}", SinglePlayerView)
    app.router.add_view("/api/settings/{osu_id}", PlayerSettingsHistoryView)
    app.router.add_view("/", LeaderboardView)
