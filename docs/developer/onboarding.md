# Developer Onboarding

## Prerequisites

- Python 3.13+
- pip
- Git

## Setup

Clone the repo and install dependencies (including dev tools):

```bash
git clone https://github.com/staleread/hearmypaper.git
cd hearmypaper/client
pip install -e .[dev]
```

This installs the app in editable mode along with: ruff, mypy, pre-commit, mkdocs, mkdocs-material, and type stubs.

## Running the app

```bash
briefcase dev
```

## Code quality

```bash
ruff check .        # lint
mypy src/           # type check
```

Pre-commit hooks run both automatically on each commit:

```bash
pre-commit install  # one-time setup
```

## Running tests

```bash
briefcase dev --test
```

## Docs

Preview the docs site locally:

```bash
mkdocs serve
```

## Project structure

```
src/hearmypaper/    # application source
tests/              # test suite
docs/               # MkDocs documentation site
  architecture/     # SSD, SDD, ISD
  quality/          # test strategy, traceability matrix
  developer/        # this file
```

## Key architectural concepts

All cryptographic operations run **client-side** — plaintext never leaves the user's device. The desktop app authenticates via a hardware token (USB), signs a server challenge with the token's private key, and receives a short-lived JWT stored only in memory.

See [SDD](../architecture/SDD.md) for component details and [ISD](../architecture/ISD.md) for deployment.
