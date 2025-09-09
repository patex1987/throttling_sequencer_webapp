from pydantic_settings import BaseSettings

# from throttling_sequencer.core.uvicorn_log_config import LOGGING_CONFIG


class UvicornServerConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "info"
    reload: bool = False
    log_config_path: str = "./throttling_sequencer/core/log_config_json.json"

    class Config:
        env_prefix = "uvicorn_"

