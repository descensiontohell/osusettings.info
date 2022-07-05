import yaml

from backend.app.web.config import DatabaseConfig, Config, Credentials, SessionConfig, SuperuserConfig, RedisConfig


def get_config(config_path):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)
    return Config(
        credentials=Credentials(
            client_id=raw_config["credentials"]["client_id"],
            client_secret=raw_config["credentials"]["client_secret"],
            grant_type=raw_config["credentials"]["grant_type"],
            scope=raw_config["credentials"]["scope"],
            server_name=raw_config["credentials"]["server_name"],
        ),
        session=SessionConfig(
            key=raw_config["session"]["key"],
        ),
        superuser=SuperuserConfig(
            login=raw_config["superuser"]["login"],
            password=raw_config["superuser"]["password"],
        ),
        database=DatabaseConfig(
            host=raw_config["database"]["host"],
            user=raw_config["database"]["user"],
            password=raw_config["database"]["password"],
            database=raw_config["database"]["database"],
        ),
        redis=RedisConfig(
            host=raw_config["redis"]["host"],
        ),
    )
