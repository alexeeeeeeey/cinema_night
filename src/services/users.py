from database.users.schemas import UserAddSchema, UserSchema
from utils.unit_of_work import UnitOfWork


class UsersService:
    async def get_users(self, uow: UnitOfWork):
        async with uow:
            users = await uow.users.find_all(UserSchema)
            return users

    async def get_user_by_id(self, uow: UnitOfWork, user_id: str):
        async with uow:
            users = await uow.users.find_one(UserSchema, id=user_id)
            return users

    async def add_user(self, uow: UnitOfWork, user: UserAddSchema):
        user_dict = user.model_dump()
        async with uow:
            user_id = await uow.users.add_one(user_dict)
            await uow.commit()
            return user_id

    async def update_user(self, uow: UnitOfWork, user_id: str, user: UserAddSchema):
        user_dict = user.model_dump()
        async with uow:
            user_id = await uow.users.edit_one(user_id, user_dict)
            await uow.commit()
            return user_id

    async def delete_user(self, uow: UnitOfWork, user_id: str):
        async with uow:
            user_id = await uow.users.delete_one(id=user_id)
            await uow.commit()
            return user_id
