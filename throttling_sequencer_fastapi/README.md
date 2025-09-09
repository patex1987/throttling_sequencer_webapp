# Service

## Health checks
Periodically executing a check against a dummy endpoint (you can define more advanced checks)
```json
{"event": "new request id has been created", "timestamp": "2025-09-08T17:11:06.045360Z", "service_name": "throttling_sequencer_fastapi", "version": "0.1", "level": "info"}
INFO:     127.0.0.1:44232 - "GET /api/v1/health/dummy-health HTTP/1.1" 200 OK
```

# Development

## Running from IDE

## Running from docker

### Build in development mode

1. Navigate to the `throttling_sequencer_fastapi` folder
2. Execute:
```shell
docker build --target dev -t fastapi_graphql:local_dev -f ./Dockerfile .
```

enter the container with non-running service:
```shell
docker run -it --rm fastapi_graphql:local_dev /bin/bash 
```

run the container with the fastapi service (the entrypoint should be configured for the fastapi app):
```shell
docker run -p 8080:8080 --rm fastapi_graphql:local_dev  
```
Note: this enters the container in attached mode

Output:
```text
INFO:     Will watch for changes in these directories: ['/app']
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
INFO:     Started reloader process [7] using StatReload
WARNING:  ASGI app factory detected. Using it, but please consider setting the --factory flag explicitly.
INFO:     Started server process [9]
INFO:     Waiting for application startup.
{"event": "New genetic config instance 139721989980032", "timestamp": "2025-09-08T16:36:56.301388Z", "service_name": "throttling_sequencer_fastapi", "version": "0.1", "level": "info"}
INFO:     Application startup complete.
```

### Build in production mode
1. Navigate to the `throttling_sequencer_fastapi` folder
2. Execute:
```shell
docker build --target prod -t fastapi_graphql:local_prod -f ./Dockerfile .
```

enter the container with non-running service:
```shell
docker run -it --rm fastapi_graphql:local_prod /bin/bash 
```

run the container with the fastapi service (the entrypoint should be configured for the fastapi app):
```shell
docker run --rm fastapi_graphql:local_prod
```
Note: this enters the container in attached mode

Output:
```text
WARNING:  ASGI app factory detected. Using it, but please consider setting the --factory flag explicitly.
INFO:     Started server process [7]
INFO:     Waiting for application startup.
{"event": "New genetic config instance 139841738420688", "timestamp": "2025-09-08T16:50:44.417217Z", "service_name": "throttling_sequencer_fastapi", "version": "0.1", "level": "info"}
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
{"event": "new request id has been created", "timestamp": "2025-09-08T16:51:22.070389Z", "service_name": "throttling_sequencer_fastapi", "version": "0.1", "level": "info"}
{"event": "headers detected by fastapi CustomAuthenticationMiddleware: Headers({'host': '127.0.0.1:8080', 'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:142.0) Gecko/20100101 Firefox/142.0', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'accept-language': 'en-US,en;q=0.5', 'accept-encoding': 'gzip, deflate, br, zstd', 'connection': 'keep-alive', 'upgrade-insecure-requests': '1', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'priority': 'u=0, i'})", "request_id": "27792f90-65af-43e4-a5e2-ac9d925043ca", "user_id": "main_user_xyz", "timestamp": "2025-09-08T16:51:22.070797Z", "service_name": "throttling_sequencer_fastapi", "version": "0.1", "level": "info"}
{"event": "Fastapi validation: Unknown auth scheme detected: ", "request_id": "27792f90-65af-43e4-a5e2-ac9d925043ca", "user_id": "main_user_xyz", "timestamp": "2025-09-08T16:51:22.070966Z", "service_name": "throttling_sequencer_fastapi", "version": "0.1", "level": "info"}
INFO:     172.17.0.1:44302 - "GET / HTTP/1.1" 404 Not Found
{"event": "new request id has been created", "timestamp": "2025-09-08T16:51:22.112120Z", "service_name": "throttling_sequencer_fastapi", "version": "0.1", "level": "info"}
```