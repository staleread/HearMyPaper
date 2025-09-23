# HearMyPaper (Client)

Cross-platform client for HearMyPaper built with [BeeWare Toga](https://beeware.org/).

---

## 🛠️ Development Setup

### 1. Prerequisites
- Python **3.13** (as defined in `pyproject.toml`)
- [uv](https://github.com/astral-sh/uv) package/dependency manager

Install `uv` if not already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create a virtual environment & install dependencies
From the project root:

```bash
uv venv .venv
. .venv/bin/activate
uv sync
```

This will install dependencies listed in `pyproject.toml` into `.venv`.

3. Run the app in development mode
Inside the venv:

```bash
briefcase dev
```

This starts the app in development mode — changes under src/hearmypaper/ are picked up immediately without rebuilding.

4. Run tests

```bash
uv run pytest
```

## 📦 Building the App
BeeWare can package the app for multiple platforms:

Windows / macOS / Linux desktop

iOS / Android mobile

### Build & run a packaged app

```bash
briefcase create
briefcase build
briefcase run
```

Make a distributable installer

```bash
briefcase package
```

## 📚 Useful Links
- BeeWare Toga docs: https://toga.readthedocs.io/
- BeeWare Briefcase docs: https://briefcase.readthedocs.io/en/latest/
- Tutorial: https://beeware.org/project/projects/tutorials/
- uv docs: https://docs.astral.sh/uv/

## 📂 Project Structure

```bash
hearmypaper/
├── src/hearmypaper/        # App source code
│   ├── app.py              # Entry point
│   ├── ui/                 # UI screens
│   ├── services/           # Business logic & API calls
│   └── utils/              # Helpers (navigator, etc.)
├── tests/                  # Unit tests
├── pyproject.toml          # Project metadata & dependencies
└── README.md               # You are here 🚀
```
