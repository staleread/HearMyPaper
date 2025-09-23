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
pip install -r requirements.txt
```

If you prefer to install directly from `pyproject.toml`:

```bash
pip install .
```

### 3. Run the app in development mode

Inside the venv:

```bash
briefcase dev
```

This launches the app in development mode — changes under `src/hearmypaper/` are picked up immediately without rebuilding.

### 4. Run tests

```bash
pytest
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

---

## 📚 Useful Links

* [BeeWare Toga docs](https://toga.readthedocs.io/)
* [BeeWare Briefcase docs](https://briefcase.readthedocs.io/en/latest/)
* [BeeWare Tutorial](https://beeware.org/project/projects/tutorials/)

---

## 📂 Project Structure

```bash
.
├── src/hearmypaper/        # App source code
│   ├── app.py              # App entry point
│   ├── __main__.py         # Allows running as `python -m hearmypaper`
│   ├── models/             # Data models
│   ├── resources/          # Assets, static files
│   ├── services/           # API clients, auth, repositories
│   ├── ui/                 # UI screens (login, register, etc.)
│   └── utils/              # Helpers (e.g., navigator)
├── tests/                  # Unit tests
├── pyproject.toml          # Project metadata & dependencies
├── LICENSE                 # License info
├── CHANGELOG               # Version history
└── README.md               # You are here 🚀
```

