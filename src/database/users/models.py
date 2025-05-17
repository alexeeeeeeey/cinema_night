from uuid import UUID, uuid4

from sqlalchemy import Enum as PgEnum
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from database.users.schemas import PermissionEnum


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid(),
    )
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    fullname: Mapped[str]
    permission: Mapped["PermissionEnum"] = mapped_column(
        PgEnum(PermissionEnum, name="permission_enum", create_constraint=True),
        server_default=PermissionEnum.USER.value,
        default=PermissionEnum.USER,
    )
