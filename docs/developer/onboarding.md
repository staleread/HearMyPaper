# Developer Onboarding

Welcome to HearMyPaper! This guide gets you from a fresh checkout to a running system in one sitting. The project has two independent codebases — start with the server (it's what the client talks to), then bring up the desktop app.

## Repositories

| Repo | What it is |
|------|-----------|
| [staleread/hearmypaper](https://github.com/staleread/hearmypaper) | Desktop client (Python / Toga / Briefcase) |
| [staleread/hmp-server](https://github.com/staleread/hmp-server) | Backend API (FastAPI / PostgreSQL / Redis) |
| [staleread/hmp-storybook](https://github.com/staleread/hmp-storybook) | UI component showcase (Toga / Briefcase) |
| [staleread/hmp-infra](https://github.com/staleread/hmp-infra) | Kubernetes / Helm / ArgoCD config |

---

## Part 1 — Server

### Prerequisites

- Docker and Docker Compose

That's it. Everything else (Python, PostgreSQL, Redis) runs inside containers.

### Start the stack

```bash
git clone https://github.com/staleread/hmp-server.git
cd hmp-server
docker compose up
```

Docker Compose starts three services:

| Container | Role | Port |
|-----------|------|------|
| `hmp-api` | FastAPI application | `8000` |
| `hmp-postgres` | PostgreSQL database | — (internal) |
| `hmp-redis` | Redis (response cache) | `6379` |

The API container mounts `./app` and `./db` as live volumes, so changes to Python files are picked up without a rebuild.

Once the stack is healthy:

- **API** → `http://localhost:8000`
- **Swagger UI** → `http://localhost:8000/docs`
- **OpenAPI JSON** → `http://localhost:8000/openapi.json`
- **Health check** → `http://localhost:8000/health` → `"I'm good"`

### Cleanup

```bash
docker compose down -v   # stops containers and removes volumes
```

### Server entry point

`app/main.py` is the entry point. It creates the FastAPI app, registers all routers, and wires up the Redis cache on startup:

```
app/
  main.py              ← FastAPI app, router registration
  auth/                ← JWT auth, token validation, user identity
  project/             ← course project management
  submission/          ← encrypted student submissions
  audit/               ← action log for all write operations
  pdf_to_audio/        ← PDF → audio conversion microservice proxy
  admin/               ← admin-only user management
  shared/
    config/
      env.py           ← pydantic-settings, reads env vars / .env file
      db.py            ← SQLAlchemy engine factory
```

### Configuration

The server reads all settings from environment variables (or a `.env` file). The Docker Compose file pre-populates everything needed for local development. Key variables:

| Variable | Purpose |
|----------|---------|
| `JWT_SECRET` | Signs and verifies JWTs |
| `POSTGRES_*` | Database connection |
| `REDIS_*` | Cache connection |

Settings are loaded once via `get_env_settings()` (LRU-cached) and available anywhere via `from app.shared.config.env import get_env_settings`.

### Database migrations

Migrations live in `db/migrations/` and are managed with **dbmate**. They run automatically inside the API container on startup. If you need to add a migration manually:

```bash
docker compose exec api dbmate new <migration_name>
docker compose exec api dbmate up
```

### Code quality (server)

```bash
uv sync --frozen --dev
uv run ruff check . --output-format=github   # lint
uv run mypy .                                 # type check
uv run pytest -q                              # tests
```

CI runs all three on every push (`.github/workflows/ci.yml`).

---

## Part 2 — Desktop Client

### Prerequisites

- Python 3.13+
- pip

### Setup

```bash
git clone https://github.com/staleread/hearmypaper.git
cd hearmypaper/client
pip install -e .[dev]
pre-commit install        # sets up ruff + mypy hooks
```

### Run the app

```bash
briefcase dev
```

The app starts at the login screen. It expects the server at `http://localhost:8000` by default (configured in `src/hearmypaper/resources/config.toml`).

### Client entry point

`src/hearmypaper/app.py` is the entry point. It creates the `Navigator`, registers every screen by name, and navigates to `"login"` on startup:

```
src/hearmypaper/
  app.py                    ← toga.App subclass, screen registry
  shared/
    utils/
      navigator.py          ← Navigator: screen registry + toga.MainWindow content swap
      session.py            ← ApiSession: thin HTTP wrapper around requests
    ui/
      catalog_screen.py     ← generic Result-aware table screen
      item_info_screen.py   ← generic Result-aware key-value detail screen
      components/
        datetime_picker.py  ← custom composite date/time picker widget
  auth/ui/login_screen.py   ← entry screen, token file + password
  project/ui/               ← project CRUD screens
  submission/ui/            ← submission upload, open, convert screens
  user/ui/                  ← user management screens
  audit/ui/                 ← audit log catalog + CSV export
```

### Navigation model

The `Navigator` is the central piece of the client. Screens are registered by name and rendered on demand:

```python
navigator.navigate("projects_catalog")   # swaps MainWindow.content
```

Each screen factory receives the `navigator` as its only argument and returns a `toga.Widget`. The navigator holds the `ApiSession` (HTTP client) and the logged-in user's `credentials_path`.

### Shared UI patterns

Two generic screens eliminate almost all boilerplate:

- **`catalog_screen`** — takes a `Result[list]` and renders either a `Table` or an inline error message. Used for every list view (users, projects, submissions, audit logs).
- **`item_info_screen`** — takes a `Result[dict]` and renders a scrollable key-value form. Used for every detail view.

The `Result` type comes from the [`result`](https://github.com/rustedpy/result) library (`Ok` / `Err`). Service functions always return `Result` — screens never raise exceptions from API calls.

### Code quality (client)

```bash
ruff check .        # lint
mypy src/           # type check
briefcase dev --test   # run tests
```

Pre-commit hooks run ruff and mypy automatically on each commit.

### Docs site

```bash
mkdocs serve        # preview at http://127.0.0.1:8000
```

---

## Part 3 — UI Storybook

The storybook is a standalone Toga app that showcases shared UI patterns from the client without needing a running server.

```bash
git clone https://github.com/staleread/hmp-storybook.git
cd hmp-storybook
briefcase dev
```

Double-click any story in the sidebar to preview it. Forms use stub navigators that show dialogs instead of making real API calls.

---

## Key architectural concepts

- **All crypto runs client-side.** Plaintext never leaves the user's device. The desktop app authenticates with a hardware token (USB), signs a server challenge with the token's private key, and receives a short-lived JWT stored only in memory.
- **Submissions are end-to-end encrypted.** A PDF is encrypted with the instructor's public key before upload. Only the instructor's token can decrypt it.
- **The server never sees plaintext.** It stores and forwards ciphertext only. This is why the audit log exists — it's the only way to observe what happened.

See [SDD](../architecture/SDD.md) for component details and [ISD](../architecture/ISD.md) for deployment.
