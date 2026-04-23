# Documentation CI/CD

This document describes how documentation for the HearMyPaper system is kept up to date automatically as the codebase changes.

## Documentation Artifacts

| Artifact | Tool | Published at |
|----------|------|-------------|
| API reference (OpenAPI + Swagger UI) | FastAPI (auto-generated) | `<server-url>/docs` and `<server-url>/openapi.json` |
| Project documentation site | MkDocs Material | [staleread.github.io/HearMyPaper](https://staleread.github.io/HearMyPaper/) |
| UI component showcase (Storybook) | Toga / Briefcase | [staleread/hmp-storybook](https://github.com/staleread/hmp-storybook) |

## Pipelines

### API Documentation — Leader Service

FastAPI generates the OpenAPI specification and Swagger UI directly from route definitions and Pydantic schemas at application startup. No separate build step is required.

**Trigger:** push to `main` or `prod` branch of the server repository.

**Pipeline** (defined in `.github/workflows/cd.yml`):

```
push → main / prod
  └─ Build Docker image
  └─ Push image to GHCR
  └─ Deploy to DigitalOcean App Platform
       └─ FastAPI starts → /docs and /openapi.json are live
```

The deployed Swagger UI always reflects the current server code because it is generated at runtime from the same source. No manual sync is possible; stale documentation is structurally prevented.

### Project Documentation Site — MkDocs

The MkDocs static site is rebuilt and published to GitHub Pages automatically on every push to `main` that touches documentation sources.

**Trigger:** push to `main` with changes inside `docs/` or `mkdocs.yml`.

**Pipeline** (defined in `.github/workflows/docs.yml`):

```
push → main  (docs/** or mkdocs.yml changed)
  └─ Install dependencies (pip install .[dev])
  └─ mkdocs gh-deploy --force
       └─ Builds static site
       └─ Force-pushes to gh-pages branch
       └─ GitHub Pages picks up the update
```

**Versioning:** the documentation site version tracks the `version` field in `pyproject.toml`. A documentation breaking change (restructured nav, removed page) warrants a new minor or major version bump alongside the code change.

### UI Documentation — Storybook

The Storybook project lives at [staleread/hmp-storybook](https://github.com/staleread/hmp-storybook). It is a Toga desktop application, not a web artifact, so it is not "deployed" in the traditional sense.

- During development: clone the repo and run `briefcase dev` from its root.
- Stories cover the shared UI patterns of the desktop client: `catalog_screen`, `item_info_screen`, `DateTimePicker`, and the standard form layout (login, create-project, export).

A future improvement would add a Briefcase packaging step to a CI pipeline in `staleread/hmp-storybook`, producing a standalone binary that can be downloaded and run by anyone reviewing UI changes without needing a Python environment.

## Trigger Summary

| Event | API Docs | MkDocs Site | Storybook |
|-------|----------|-------------|-----------|
| Push to feature branch | — | — | run locally |
| Push to `main` (server) | ✅ deployed | — | — |
| Push to `main` (client, docs changed) | — | ✅ published | — |
| Push to `main` (storybook) | — | — | ✅ (planned binary) |
