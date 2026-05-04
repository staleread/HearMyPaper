# --------------------------------
# Builder
# --------------------------------
FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# 1. Install dependencies (Layer caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=libs/hmp_core/pyproject.toml,target=libs/hmp_core/pyproject.toml \
    --mount=type=bind,source=apps/hmp_converter/pyproject.toml,target=apps/hmp_converter/pyproject.toml \
    uv sync --frozen --no-install-workspace --no-dev --package hmp-converter

COPY libs/hmp_core /app/libs/hmp_core
COPY apps/hmp_converter /app/apps/hmp_converter

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --package hmp-converter


# --------------------------------
# Runtime Base
# --------------------------------
FROM python:3.14-slim AS runtime

# Install system runtime-only dependencies (e.g., shared libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libespeak-ng1 \
    espeak-ng \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY libs/hmp_core /app/libs/hmp_core
COPY apps/hmp_converter /app/apps/hmp_converter
EXPOSE 8000


# --------------------------------
# Development
# --------------------------------
FROM runtime AS dev
WORKDIR /app/apps/hmp_converter
CMD ["uvicorn", "src.hmp_converter.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# --------------------------------
# Production
# --------------------------------
FROM runtime AS prod
WORKDIR /app/apps/hmp_converter
CMD ["fastapi", "run", "src/hmp_converter/main.py", "--port", "8000"]
