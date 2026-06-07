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

## Issue Tracking

This project uses **bd (beads)** for issue tracking. Run `bd prime` for workflow context, or install hooks with `bd hooks install` for automatic context injection.

Quick reference:

- `bd ready` - find unblocked work
- `bd create "Title" --type task --priority 2` - create an issue
- `bd close <id>` - close completed work
- `bd dolt push` - push Beads data when using a shared Beads remote

For full workflow details, run `bd prime`.
