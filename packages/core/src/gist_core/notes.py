from sqlalchemy.orm import Session

from gist_core.models import Note


def create_note(session: Session, content: str) -> Note:
    if not content.strip():
        raise ValueError("Note content must not be empty")

    note = Note(content=content)
    session.add(note)
    session.commit()
    return note
