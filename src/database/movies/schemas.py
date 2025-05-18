from uuid import UUID

from pydantic import BaseModel


class MovieIDSchema(BaseModel):
    id: UUID


class MovieAddSchema(BaseModel):
    hall_id: UUID
    name: str
    description: str
    genres: str


class MovieGetSchema(BaseModel):
    hall_id: UUID
    name: str
    description: str
    genres: str


class MovieSchema(MovieAddSchema, MovieIDSchema):
    pass
