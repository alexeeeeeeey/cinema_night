from utils.unit_of_work import UnitOfWork


async def get_uow():
    return UnitOfWork()
