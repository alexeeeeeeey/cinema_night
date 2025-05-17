from uuid import UUID

from fastapi import HTTPException, status

from database.users.schemas import UserLoginSchema, UserRegisterSchema, UserSchema
from utils.auth import Hasher
from utils.unit_of_work import UnitOfWork


class AuthService:
    @staticmethod
    async def register_user(user: UserRegisterSchema, uow: UnitOfWork) -> UUID:
        async with uow:
            user.password = Hasher.get_password_hash(user.password)

            user_id = await uow.users.add_one(user.model_dump())
            await uow.commit()

        return user_id

    @staticmethod
    async def login_user(uow: UnitOfWork, user: UserLoginSchema) -> UserSchema:
        async with uow:
            user_db = await uow.users.find_one(UserSchema, username=user.username)

            if not Hasher.verify_password(user.password, user_db.password):
                raise HTTPException(
                    status.HTTP_401_UNAUTHORIZED, detail="Wrong password"
                )

            return user_db
