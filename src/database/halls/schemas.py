from uuid import UUID

from pydantic import BaseModel


class HallIDSchema(BaseModel):
    id: UUID


class HallAddSchema(BaseModel):
    hall_name: str


class HallGetSchema(BaseModel):
    hall_name: str


class HallSchema(HallAddSchema, HallIDSchema):
    pass
