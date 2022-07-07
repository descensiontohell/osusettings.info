from envyaml import EnvYAML

from backend.app.web.config import DatabaseConfig, Config, Credentials, SessionConfig, SuperuserConfig, RedisConfig


def get_config(config_path):
    env = EnvYAML(config_path)
    return Config(
        credentials=Credentials(
            client_id=env["credentials.client_id"],
            client_secret=env["credentials.client_secret"],
            grant_type=env["credentials.grant_type"],
            scope=env["credentials.scope"],
            server_name=env["credentials.server_name"],
        ),
        session=SessionConfig(
            key=env["session.key"],
        ),
        superuser=SuperuserConfig(
            login=env["superuser.login"],
            password=env["superuser.password"],
        ),
        database=DatabaseConfig(
            host=env["database.host"],
            user=env["database.user"],
            password=env["database.password"],
            database=env["database.database"],
        ),
        redis=RedisConfig(
            host=env["redis.host"],
        ),
    )
