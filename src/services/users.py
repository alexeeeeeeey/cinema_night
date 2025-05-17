from database.users.schemas import UserAddSchema, UserSchema
from utils.unit_of_work import UnitOfWork


class UsersService:
    @staticmethod
    async def get_users(uow: UnitOfWork):
        async with uow:
            users = await uow.users.find_all(UserSchema)
            return users

    @staticmethod
    async def get_user_by_id(uow: UnitOfWork, user_id: str):
        async with uow:
            users = await uow.users.find_one(UserSchema, id=user_id)
            return users

    @staticmethod
    async def add_user(uow: UnitOfWork, user: UserAddSchema):
        user_dict = user.model_dump()
        async with uow:
            user_id = await uow.users.add_one(user_dict)
            await uow.commit()
            return user_id

    @staticmethod
    async def update_user(uow: UnitOfWork, user_id: str, user: UserAddSchema):
        user_dict = user.model_dump()
        async with uow:
            user_id = await uow.users.edit_one(user_id, user_dict)
            await uow.commit()
            return user_id

    @staticmethod
    async def delete_user(uow: UnitOfWork, user_id: str):
        async with uow:
            user_id = await uow.users.delete_one(id=user_id)
            await uow.commit()
            return user_id
