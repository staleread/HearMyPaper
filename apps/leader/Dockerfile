# --------------------------------
# Builder
# --------------------------------
FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install build-only tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Download dbmate binary
RUN curl -fsSL -o /usr/local/bin/dbmate \
    https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64 \
 && chmod +x /usr/local/bin/dbmate

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Sync dependencies for the leader package
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=apps/leader/pyproject.toml,target=apps/leader/pyproject.toml \
    uv sync --frozen --no-install-workspace --package leader

# Copy the entire mono-repo for migration paths and package availability
# (Alternatively, we could selectively copy packages, but for dev this is easier)
COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --package leader


# --------------------------------
# Runtime Base
# --------------------------------
FROM python:3.14-slim AS runtime

WORKDIR /app

# Copy the venv and the dbmate binary from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /usr/local/bin/dbmate /usr/local/bin/dbmate

# Copy the necessary files for the app and migrations
COPY . /app

ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app/apps/leader
EXPOSE 8000


# --------------------------------
# Development
# --------------------------------
FROM runtime AS dev
# Ensure migrate.sh is executable
RUN chmod +x scripts/migrate.sh
CMD ["sh", "-c", "./scripts/migrate.sh && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]


# --------------------------------
# Production
# --------------------------------
FROM runtime AS prod
RUN chmod +x scripts/migrate.sh
CMD ["sh", "-c", "./scripts/migrate.sh && uvicorn main:app --host 0.0.0.0 --port 8000"]
