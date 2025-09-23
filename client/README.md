# HearMyPaper (Client)

Cross-platform client for HearMyPaper, built with [BeeWare Toga](https://beeware.org/).

---

## 🛠️ Development Setup

### 1. Prerequisites

* Python `>=3.13` (as defined in `pyproject.toml`)
* [pip](https://pip.pypa.io/) for dependency management
* [BeeWare Briefcase](https://briefcase.readthedocs.io/) for building & packaging

### 2. Create a virtual environment & install dependencies

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows use: .venv\Scripts\activate
pip install .[dev]
```

### 3. Run the app in development mode

Inside the venv:

```bash
briefcase dev
```

---

## 📦 Building the App

BeeWare can package the app for multiple platforms:

* **Windows / macOS / Linux** (desktop)
* **iOS / Android** (mobile)

### Build & run a packaged app

```bash
briefcase create
briefcase build
briefcase run
```

### Make a distributable installer

```bash
briefcase package
```
