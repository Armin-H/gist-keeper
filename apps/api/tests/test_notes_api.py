import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from gist_api.main import app, get_session
from gist_core.db import create_db_engine, upgrade_db
from gist_core.models import Note
from sqlalchemy.orm import Session, sessionmaker


@pytest.fixture
def sessions(tmp_path: Path) -> sessionmaker[Session]:
    path = tmp_path / "gist-keeper.db"
    upgrade_db(path)
    return sessionmaker(create_db_engine(path))


@pytest.fixture
def client(sessions: sessionmaker[Session]) -> Iterator[TestClient]:
    def get_test_session() -> Iterator[Session]:
        with sessions() as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_note_is_created(client: TestClient, sessions: sessionmaker[Session]) -> None:
    response = client.post("/notes", json={"content": "AEST is UTC+10"})

    assert response.status_code == 201
    body = response.json()
    assert body["content"] == "AEST is UTC+10"
    with sessions() as session:
        saved = session.get(Note, uuid.UUID(body["id"]))
        assert saved is not None
        assert saved.content == "AEST is UTC+10"


@pytest.mark.parametrize("content", ["", "   ", "\n\t"])
def test_empty_content_is_rejected(
    client: TestClient, sessions: sessionmaker[Session], content: str
) -> None:
    response = client.post("/notes", json={"content": content})

    assert response.status_code == 422
    with sessions() as session:
        assert session.query(Note).count() == 0


def test_missing_content_is_rejected(client: TestClient) -> None:
    response = client.post("/notes", json={})

    assert response.status_code == 422
