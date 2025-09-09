# TODO: bridge this with /throttling_sequencer/app.py
import uvicorn

from throttling_sequencer.app import create_app
from throttling_sequencer.core.uvicorn_log_config import load_json_log_config
from throttling_sequencer.core.uvicorn_server_config import UvicornServerConfig


def main():
    uvicorn_server_config = UvicornServerConfig()
    log_config = load_json_log_config(uvicorn_server_config.log_config_path)
    uvicorn.run(
        create_app(),
        host=uvicorn_server_config.host,
        port=uvicorn_server_config.port,
        log_level=uvicorn_server_config.log_level,
        log_config=log_config,
        reload=uvicorn_server_config.reload,
    )


if __name__ == "__main__":
    main()
