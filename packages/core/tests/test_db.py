from pathlib import Path

import pytest
from gist_core.db import create_db_engine, database_path
from sqlalchemy import text


def test_database_path_is_in_local_app_data(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))

    assert database_path() == tmp_path / "GistKeeper" / "gist-keeper.db"


def test_engine_creates_missing_folder(tmp_path: Path) -> None:
    path = tmp_path / "GistKeeper" / "gist-keeper.db"

    engine = create_db_engine(path)
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    assert path.exists()
