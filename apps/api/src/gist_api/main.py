import uuid
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, Request
from gist_core.db import create_db_engine, upgrade_db
from gist_core.notes import create_note
from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy.orm import Session, sessionmaker


class NoteCreate(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def content_not_blank(cls, content: str) -> str:
        if not content.strip():
            raise ValueError("must not be empty")
        return content


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    content: str


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    upgrade_db()
    engine = create_db_engine()
    app.state.sessions = sessionmaker(engine)
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)


def get_session(request: Request) -> Iterator[Session]:
    with request.app.state.sessions() as session:
        yield session


@app.post("/notes", status_code=201)
def post_note(
    body: NoteCreate, session: Annotated[Session, Depends(get_session)]
) -> NoteRead:
    note = create_note(session, body.content)
    return NoteRead.model_validate(note)


def run() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8000)
