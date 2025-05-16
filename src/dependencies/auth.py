import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from database.auth.schemas import JWTSchema
from core.config import settings

security = HTTPBearer()


async def decode_jwt(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> JWTSchema:
    token = credentials.credentials
    try:
        data: dict = jwt.decode(token, settings.API_SECRET_TOKEN, algorithms=["HS256"])
        payload = JWTSchema(**data)

    except InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid signature")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")

    return payload
