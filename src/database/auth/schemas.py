from uuid import UUID

from pydantic import BaseModel


class JWTSchema(BaseModel):
    user_id: UUID
    exp: int


class AccessJWT(BaseModel):
    token_type: str = "bearer"
    access_token: str
