# CI/CD

## Variables and Secrets

- vars.BASE_URL: Base URL injected into client config.

## Local checks

```bash
pip install -e .[dev]
ruff check .
mypy .
```

## Releases

- Push tag starting with `v` that points to a commit on main.
- Windows, Ubuntu (DEB), and Arch packages are built and attached to the GitHub Release.

