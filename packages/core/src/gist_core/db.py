import os
from pathlib import Path

from sqlalchemy import Engine, create_engine


def database_path() -> Path:
    return Path(os.environ["LOCALAPPDATA"]) / "GistKeeper" / "gist-keeper.db"


def create_db_engine(path: Path | None = None) -> Engine:
    path = path or database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite:///{path}")
