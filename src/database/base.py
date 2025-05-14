from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from core.config import settings

T = TypeVar("T", bound=BaseModel)

engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = async_sessionmaker(engine, autoflush=False, expire_on_commit=True)


class Base(DeclarativeBase):
    def to_read_model(self, schema: type[T]) -> T:
        return schema.model_validate(self, from_attributes=True)

    def __repr__(self):
        cols = []
        for _idx, col in enumerate(self.__table__.columns.keys()):
            cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
