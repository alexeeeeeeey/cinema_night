from fastapi import Depends

from database.auth.schemas import JWTSchema
from services.users import UsersService
from utils.unit_of_work import UnitOfWork

from .auth import decode_jwt
from .unit_of_work import get_uow


async def get_user(
    jwt: JWTSchema = Depends(decode_jwt), uow: UnitOfWork = Depends(get_uow)
):
    async with uow:
        return await UsersService.get_user_by_id(uow, jwt.user_id)
