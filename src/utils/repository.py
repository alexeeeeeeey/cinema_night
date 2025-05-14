from typing import TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, select, update

T = TypeVar("T", bound=BaseModel)

class SQLAlchemyRepository():
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_one(self, schema: type[T], **filter_by) -> T:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one().to_read_model(schema)
        return res

    async def find_all(self, schema: type[T], **filter_by) -> list[T]:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model(schema) for row in res.all()]
        return res

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def add_many(
        self, data: list[dict]
    ) -> list[int]:
        stmt = insert(self.model).values(data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def edit_one(self, id: int, data: dict) -> int:
        stmt = (
            update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete_one(self, data: dict) -> None:
        stmt = delete(self.model).filter_by(**data)
        await self.session.execute(stmt)
