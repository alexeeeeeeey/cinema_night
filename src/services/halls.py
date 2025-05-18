from uuid import UUID

from database.halls.schemas import HallAddSchema, HallSchema
from utils.unit_of_work import UnitOfWork


class HallsService:
    @staticmethod
    async def get_halls(uow: UnitOfWork):
        async with uow:
            halls = await uow.halls.find_all(HallSchema)
            return halls

    @staticmethod
    async def get_hall_by_id(uow: UnitOfWork, hall_id: UUID):
        async with uow:
            halls = await uow.halls.find_one(HallSchema, id=hall_id)
            return halls

    @staticmethod
    async def add_hall(uow: UnitOfWork, hall: HallAddSchema):
        hall_dict = hall.model_dump()
        async with uow:
            hall_id = await uow.halls.add_one(hall_dict)
            await uow.commit()
            return hall_id

    @staticmethod
    async def update_hall(uow: UnitOfWork, hall_id: UUID, hall: HallAddSchema):
        hall_dict = hall.model_dump()
        async with uow:
            hall_id = await uow.halls.edit_one(hall_id, hall_dict)
            await uow.commit()
            return hall_id

    @staticmethod
    async def delete_hall(uow: UnitOfWork, hall_id: UUID):
        async with uow:
            hall_id = await uow.halls.delete_one(id=hall_id)
            await uow.commit()
            return hall_id
