from uuid import UUID

from fastapi import Request

from database.users.schemas import UserSchema
from permissions.base import BaseModelPermissions
from utils.unit_of_work import UnitOfWork


class User(BaseModelPermissions):
    @staticmethod
    async def is_user(request: Request, user: UserSchema, uow: UnitOfWork):
        user_id = UUID(request.path_params.get("user_id"))
        return user.id == user_id
