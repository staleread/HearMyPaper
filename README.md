# 🎵 HearMyPaper

**Secure your course project, and only let the instructor listen!**

HearMyPaper is a modular monolith application designed to protect academic work
using end-to-end encryption. Students seal their submissions with the
instructor's public key, ensuring that only the intended recipient can access
the content.

## 🛠 Development Setup

This project uses a modern Python stack with `uv` for dependency management,
`mise` for task orchestration, and `Docker` for infrastructure.

### 1. Prerequisites

- [uv](https://docs.astral.sh/uv/) - Python package manager
- [mise](https://mise.jdx.dev/) - Universal task runner and tool manager
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)

### 2. Infrastructure

You can spin up the required infrastructure (Postgres, Redis, MinIO, RabbitMQ)
using Docker Compose profiles.

**Start only infrastructure:**
```bash
docker compose --profile infra up -d
```

**Start the full stack (Infra + Leader API):**
```bash
docker compose --profile infra --profile app up -d
```

### 3. Local Development (outside Docker)

If you prefer running the applications locally while using Docker only for the
database and services:

1. **Setup environment:**
   ```bash
   uv sync
   ```

2. **Run migrations:**
   ```bash
   mise run leader:migrate
   ```

3. **Launch applications:**
   We use `mise` to simplify common development tasks. You can run:
   - `mise run leader:dev`: Starts the Leader API (FastAPI) with hot-reload.
   - `mise run client:dev`: Launches the BeeWare Toga desktop client in development mode.

> [!IMPORTANT] **Briefcase & uv Integration**: Briefcase does not currently
> support `uv` workspace dependencies. Before running any `briefcase` command
> (including `mise run client:dev`), you must manually comment out the
> workspace-based dependencies in `apps/client/pyproject.toml` (e.g.,
> `shared-kernel`, `client-core`, etc.). The project is configured to include
> these sources directly via Briefcase's `sources` configuration.

### 4. Mise Tasks

`mise` acts as a powerful task runner. You can explore all available tasks by
running `mise tasks`. Key tasks include:
- `leader:init-user`: Creates an initial admin user in the system.
- `gen-session`: Generates a JWT session token for client authentication.

---

## 📄 License

HearMyPaper is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👥 Credits

**Developed by:**
- Mykola Ratushniak
- Neholiuk Oleksandr

**Built with:**
- [BeeWare Toga](https://beeware.org/) - Native GUI framework
- [uv](https://astral.sh/uv) - Fast Python package management
- [BlackSheep](https://www.blacksheepframework.com/) - Fast ASGI web framework
- [PyNaCl](https://pynacl.readthedocs.io/) - Networking and Cryptography library
