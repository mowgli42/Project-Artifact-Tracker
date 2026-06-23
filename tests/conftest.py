import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def client(tmp_path, monkeypatch):
    import importlib
    import os

    db_path = str(tmp_path / "test_projects.db")
    monkeypatch.setattr("database.DB_NAME", db_path)

    import database

    importlib.reload(database)
    import app as app_module

    importlib.reload(app_module)
    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as test_client:
        yield test_client

    if os.path.exists(db_path):
        os.unlink(db_path)
