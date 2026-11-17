from pathlib import Path

import gist_core
import pytest
from alembic import command
from alembic.config import Config
from gist_core.db import create_db_engine
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def path(tmp_path: Path) -> Path:
    path = tmp_path / "gist-keeper.db"
    config = Config()
    config.set_main_option(
        "script_location", str(Path(gist_core.__file__).parent / "migrations")
    )
    config.attributes["path"] = path
    command.upgrade(config, "head")
    return path


def test_migrations_create_notes_table(path: Path) -> None:
    engine = create_db_engine(path)

    assert "notes" in inspect(engine).get_table_names()


def test_migrated_notes_reject_empty_content(path: Path) -> None:
    engine = create_db_engine(path)

    with pytest.raises(IntegrityError), engine.begin() as connection:
        connection.execute(
            text(
                "INSERT INTO notes (id, content, created_at) "
                "VALUES ('1', '  ', '2026-01-01')"
            )
        )
