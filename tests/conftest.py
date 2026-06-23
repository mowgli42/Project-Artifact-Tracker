import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test_projects.db")
    monkeypatch.setenv("PROJECTS_DB_PATH", db_path)

    for name in list(sys.modules):
        if name in ("app", "database"):
            del sys.modules[name]

    import app as app_module

    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as test_client:
        yield test_client

    if os.path.exists(db_path):
        os.unlink(db_path)
