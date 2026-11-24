from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from gist_core.db import create_db_engine, upgrade_db
from sqlalchemy.orm import sessionmaker


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    upgrade_db()
    engine = create_db_engine()
    app.state.sessions = sessionmaker(engine)
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)


def run() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8000)
