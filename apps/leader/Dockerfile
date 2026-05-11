# --------------------------------
# Builder
# --------------------------------
FROM python:3.14-slim AS builder

# Install build-only tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Download dbmate binary
RUN curl -fsSL -o /usr/local/bin/dbmate \
    https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64 \
 && chmod +x /usr/local/bin/dbmate

# Install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# Copy the entire mono-repo to resolve all workspace members
COPY . /app

# Sync dependencies for the leader package
# This creates a virtual environment in /app/.venv
RUN --mount=type=cache,target=/root/.cache/uv \
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
# .dockerignore will prevent overwriting .venv from host
COPY . /app

ENV PATH="/app/.venv/bin:$PATH"
# Ensure we can find the app module
ENV PYTHONPATH="/app/apps/leader:/app"

WORKDIR /app/apps/leader
EXPOSE 8000


# --------------------------------
# Development
# --------------------------------
FROM runtime AS dev
# Ensure leader-migrate is executable
RUN chmod +x /app/scripts/leader-migrate
CMD ["sh", "-c", "cd /app && ./scripts/leader-migrate && cd /app/apps/leader && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]


# --------------------------------
# Production
# --------------------------------
FROM runtime AS prod
RUN chmod +x /app/scripts/leader-migrate
CMD ["sh", "-c", "cd /app && ./scripts/leader-migrate && cd /app/apps/leader && uvicorn main:app --host 0.0.0.0 --port 8000"]
