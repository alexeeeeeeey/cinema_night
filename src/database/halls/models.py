from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from database.movies.models import Movie
    from database.users.models import User


class Hall(Base):
    __tablename__ = "halls"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    hall_name: Mapped[str]

    seats: Mapped[list["Seat"]] = relationship(
        back_populates="hall",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    movies: Mapped[list["Movie"]] = relationship(
        back_populates="hall",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Seat(Base):
    __tablename__ = "seats"
    __table_args__ = (
        UniqueConstraint(
            "hall_id", "hall_row", "hall_column", name="uix_seat_position"
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    hall_id: Mapped[UUID] = mapped_column(ForeignKey("halls.id", ondelete="CASCADE"))
    hall_row: Mapped[int]
    hall_column: Mapped[int]
    status: Mapped[str]  # TODO
    reserved_until: Mapped[datetime | None] = mapped_column(nullable=True)

    hall: Mapped["Hall"] = relationship(back_populates="seats")
    user: Mapped[Optional["User"]] = relationship(back_populates="seats")
