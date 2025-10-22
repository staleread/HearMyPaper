FROM python:3.13-slim

# Install dependencies and clear cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    espeak-ng \
    libespeak-ng1 \
 && rm -rf /var/lib/apt/lists/*

# Install dbmate
RUN curl -fsSL -o /usr/local/bin/dbmate \
    https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64 \
 && chmod +x /usr/local/bin/dbmate

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml

RUN pip install --no-cache-dir --upgrade .

COPY ./app /code/app
COPY ./db /code/db
COPY ./secrets /code/secrets

EXPOSE 8000

CMD dbmate up && fastapi run app/main.py --port 8000
