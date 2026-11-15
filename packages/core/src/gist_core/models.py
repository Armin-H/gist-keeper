import uuid
from datetime import UTC, datetime

from sqlalchemy import CheckConstraint, DateTime, MetaData, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utc_now() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "pk": "pk_%(table_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
        }
    )


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid7)
    content: Mapped[str] = mapped_column(
        Text, CheckConstraint("length(trim(content)) > 0", name="content_not_empty")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
    created_tz: Mapped[str]
