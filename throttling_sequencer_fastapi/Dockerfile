# syntax=docker/dockerfile:1.7

ARG UV_IMAGE=ghcr.io/astral-sh/uv:python3.12-bookworm-slim
FROM ${UV_IMAGE} AS base

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_LINK_MODE=copy \
    VIRTUAL_ENV=/venv \
    PATH=/venv/bin:$PATH

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl tini \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---------- deps (cache-friendly) ----------
FROM base AS deps
# copy only metadata first
COPY pyproject.toml /app/pyproject.toml
# COPY uv.lock /app/uv.lock   # (optional if you keep a lock)

# install third-party deps only
RUN uv sync --no-install-project --no-dev --frozen || \
    uv sync --no-install-project --no-dev

# ---------- build (normal install) ----------
FROM deps AS build
COPY throttling_sequencer /app/throttling_sequencer
COPY manage.py /app/main.py
RUN uv sync --no-dev --compile-bytecode

# ---------- dev (editable install) ----------
FROM deps AS dev
COPY throttling_sequencer /app/throttling_sequencer
COPY manage.py /app/main.py
RUN uv sync --dev --editable
EXPOSE 8080
ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["uvicorn","throttling_sequencer.app:create_app","--host","0.0.0.0","--port","8080","--reload"]

# ---------- prod (lean runtime) ----------
FROM base AS prod
COPY --from=build /venv /venv
COPY --from=build /app /app
RUN useradd -r -u 10001 appuser && chown -R appuser:appuser /app /venv
USER appuser
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD \
  /bin/sh -c "wget -qO- http://127.0.0.1:8080/health || nc -z 127.0.0.1 8080 || exit 1"
ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["uvicorn","throttling_sequencer.app:create_app","--host","0.0.0.0","--port","8080"]
