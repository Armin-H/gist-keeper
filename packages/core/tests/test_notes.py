from collections.abc import Iterator

import pytest
from gist_core.models import Base, Note
from gist_core.notes import create_note
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_note_is_saved(session: Session) -> None:
    note = create_note(session, "AEST is UTC+10")
    session.expire_all()

    saved = session.get(Note, note.id)

    assert saved is not None
    assert saved.content == "AEST is UTC+10"
    assert saved.created_at is not None


@pytest.mark.parametrize("content", ["", "   ", "\n\t"])
def test_empty_content_is_rejected(session: Session, content: str) -> None:
    with pytest.raises(ValueError):
        create_note(session, content)

    assert session.query(Note).count() == 0
