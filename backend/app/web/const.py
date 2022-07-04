
class Const:
    ENABLE_CACHING = True
    CACHE_EX = 300
    MIN_RANK: int = 1
    MAX_RANK: int = 10000
    TOKEN_API_PATH: str = "https://osu.ppy.sh/oauth/token"
    TOKEN_EXPIRE_HANDICAP: int = 2000
    PLAYER_STATS_PATH: str = "https://osu.ppy.sh/api/v2/users/{osu_id}/osu"
