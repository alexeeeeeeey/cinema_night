from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class PermissionEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class UserIDSchema(BaseModel):
    id: UUID


class UserAddSchema(BaseModel):
    username: str
    password: str
    fullname: str
    permission: PermissionEnum


class UserSchema(UserAddSchema, UserIDSchema):
    pass
