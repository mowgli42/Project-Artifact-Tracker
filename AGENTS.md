# AGENTS.md - guide for AI coding agents

## Project context

Project-Artifact-Tracker is a Flask project tracker with SQLite persistence.
Start with `README.md`, `app.py`, and `database.py` before editing.

## Local setup

Run from the repository root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Smoke test

```bash
.venv/bin/python -c "import database; import app"
```

## Agent notes

- Treat SQLite schema and migration changes carefully; document any data-impacting edits.
- Do not commit local database files unless they are documented fixtures.
- Preserve existing local user changes; stage only files you intentionally modify.
