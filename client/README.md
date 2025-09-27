# HearMyPaper (Client)

Cross-platform client for HearMyPaper, built with [PyQt5](https://pypi.org/project/PyQt5/).

---

## 🛠️ Development Setup

### 1. Prerequisites

* Python `>=3.13` (as defined in `pyproject.toml`)
* [uv](https://docs.astral.sh/uv/) for dependency management and running tasks

### 2. Create and sync the environment

From the project root:

```bash
uv sync --extra dev
```

To enter the environment:

```bash
source .venv/bin/activate   # On Windows use: .venv\Scripts\activate
```

### 3. Run the app in development mode

Inside the venv:

```bash
python -m app
```
