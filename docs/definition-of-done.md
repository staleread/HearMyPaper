# Definition of Done — Documentation

A change is considered **done** only when the documentation that describes it is also complete and verifiable. The rules below are organized by the type of change being made.

## Rules by Change Type

### New API Endpoint Added

| Required action | How it is verified |
|----------------|--------------------|
| Route definition includes a docstring or `summary=` / `description=` parameter | Visible in Swagger UI at `/docs` |
| Request body and response schemas are typed with Pydantic models | FastAPI generates schemas automatically; check `/openapi.json` |
| Possible error responses are declared with `responses=` | Visible in Swagger UI |
| `CHANGELOG` in the server repo is updated | Code review |

### Existing Endpoint Changed (request/response shape, status codes)

| Required action | How it is verified |
|----------------|--------------------|
| Pydantic models are updated to reflect the new contract | `/openapi.json` reflects the change after deploy |
| If the change is breaking, the API version is bumped in `info.version` of the OpenAPI spec | `/openapi.json` `info.version` field |
| Affected integration tests are updated | CI test job passes |
| `CHANGELOG` is updated | Code review |

### New UI Component or Screen Added to the Client

| Required action | How it is verified |
|----------------|--------------------|
| A story is added to the Storybook (`storybook/src/hmp_storybook/stories/`) covering at least the success state and one alternative state (error or empty) | `briefcase dev` runs without error in `storybook/` |
| If the component is a new shared widget, it is registered in `stories/__init__.py` | Story appears in the sidebar when Storybook is launched |

### Existing UI Component Changed

| Required action | How it is verified |
|----------------|--------------------|
| Affected story is updated to reflect the new behavior or appearance | `briefcase dev` runs and the story renders correctly |

### Architecture or Infrastructure Change

| Required action | How it is verified |
|----------------|--------------------|
| The relevant document (SDD, ISD, or SSD) in `docs/` is updated | MkDocs build passes (`mkdocs build --strict`) |
| If a new service or external dependency is introduced, it appears in the SDD component diagram | Code review |

### Developer Experience or Onboarding Change (tooling, setup steps)

| Required action | How it is verified |
|----------------|--------------------|
| `docs/developer/onboarding.md` is updated | Code review; new developer can follow the guide end to end |

## Automated Checks in CI

The following checks run on every pull request and must pass before merge:

| Check | Pipeline | What it catches |
|-------|----------|----------------|
| `ruff check` + `mypy` | `ci.yml` (client) | Type errors that would break Pydantic schema generation |
| `uv run pytest` | `ci.yml` (server) | Regression in API behavior vs. documented contract |
| `mkdocs build --strict` | add to `ci.yml` (client) | Broken links, missing pages referenced in `mkdocs.yml` |

## Non-functional Changes

Purely internal refactors (renaming a private variable, reformatting) that do not change observable behavior, API contracts, or UI components do not require documentation updates. When in doubt, update anyway.
