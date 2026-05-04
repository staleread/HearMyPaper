FROM python:3.14-slim AS base

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Install dbmate
RUN curl -fsSL -o /usr/local/bin/dbmate \
    https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64 \
 && chmod +x /usr/local/bin/dbmate

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a different device
ENV UV_LINK_MODE=copy

# Install dependencies only (leverage caching)
# We use bind mounts to access configuration without copying yet
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=apps/hmp_manager/pyproject.toml,target=apps/hmp_manager/pyproject.toml \
    uv sync --frozen --no-install-workspace --package hmp-manager

# Copy the source code
COPY apps/hmp_manager /app/apps/hmp_manager

# Final sync to install the workspace members
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --package hmp-manager

# Place the virtual environment on the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Run from the app directory
WORKDIR /app/apps/hmp_manager

EXPOSE 8000

# Development target with hot reload
FROM base AS dev
CMD ["sh", "-c", "dbmate up && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]

# Production target
FROM base AS prod
CMD ["sh", "-c", "dbmate up && fastapi run main.py --port 8000"]
