from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from database.halls.models import Hall


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    hall_id: Mapped[UUID] = mapped_column(ForeignKey("halls.id", ondelete="CASCADE"))
    name: Mapped[str]
    description: Mapped[str]
    genres: Mapped[str]

    hall: Mapped["Hall"] = relationship(back_populates="movies")
    rates: Mapped[list["Rate"]] = relationship(
        back_populates="movie",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Rate(Base):
    __tablename__ = "rates"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    movie_id: Mapped[UUID] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"))
    rate: Mapped[int]
    max_rate: Mapped[int]
    service_name: Mapped[str]
    service_link: Mapped[str]

    movie: Mapped["Movie"] = relationship(back_populates="rates")
