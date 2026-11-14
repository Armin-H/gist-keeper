from collections.abc import Iterator

import pytest
from gist_core.models import Base, Note
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_note_is_saved(session: Session) -> None:
    note = Note(content="AEST is UTC+10", created_tz="Australia/Sydney")
    session.add(note)
    session.commit()
    session.expire_all()

    saved = session.get(Note, note.id)

    assert saved is not None
    assert saved.content == "AEST is UTC+10"
    assert saved.created_tz == "Australia/Sydney"
    assert saved.created_at is not None
    assert saved.id.version == 7
