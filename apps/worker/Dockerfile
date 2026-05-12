# --------------------------------
# Builder
# --------------------------------
FROM python:3.14-slim AS builder

# Install build-only tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# Copy the entire mono-repo to resolve all workspace members
COPY . /app

# Sync dependencies for the worker package
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package worker


# --------------------------------
# Runtime
# --------------------------------
FROM python:3.14-slim AS runtime

# Install runtime dependencies for TTS and PDF parsing
RUN apt-get update && apt-get install -y --no-install-recommends \
    espeak-ng \
    libespeak-ng1 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the venv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy the necessary files for the app
COPY . /app

ENV PATH="/app/.venv/bin:$PATH"
# Ensure we can find the app and shared modules
ENV PYTHONPATH="/app/apps/worker:/app"

WORKDIR /app/apps/worker

CMD ["python", "main.py"]
