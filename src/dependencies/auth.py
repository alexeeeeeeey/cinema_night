from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from database.auth.schemas import JWTSchema
from utils.auth import Tokenizer

security = HTTPBearer()


async def decode_jwt(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> JWTSchema:
    token = credentials.credentials

    payload = Tokenizer.validate_token(token)

    return payload
