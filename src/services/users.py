from database.users.schemas import UserSchemaAdd
from utils.repository import SQLAlchemyRepository
from utils.unit_of_work import UnitOfWork


class UsersService:
    async def add_user(self, uow: UnitOfWork, user: UserSchemaAdd):
        user_dict = user.model_dump()
        async with uow:
            user_id = await uow.users.add_one(user_dict)
            await uow.commit()
            return user_id
