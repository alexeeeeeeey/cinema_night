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


class UserGetSchema(BaseModel):
    id: UUID
    username: str
    fullname: str


class UserRegisterSchema(BaseModel):
    username: str
    password: str
    fullname: str


class UserLoginSchema(BaseModel):
    username: str
    password: str
