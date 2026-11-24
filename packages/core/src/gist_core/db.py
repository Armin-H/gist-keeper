import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine


def database_path() -> Path:
    return Path(os.environ["LOCALAPPDATA"]) / "GistKeeper" / "gist-keeper.db"


def create_db_engine(path: Path | None = None) -> Engine:
    path = path or database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite:///{path}")


def upgrade_db(path: Path | None = None) -> None:
    config = Config()
    config.set_main_option("script_location", str(Path(__file__).parent / "migrations"))
    config.attributes["path"] = path
    command.upgrade(config, "head")
