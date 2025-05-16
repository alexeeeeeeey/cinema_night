import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from core.config import settings
from database.auth.schemas import JWTSchema

security = HTTPBearer()


async def decode_jwt(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> JWTSchema:
    token = credentials.credentials
    try:
        data: dict = jwt.decode(token, settings.API_SECRET_TOKEN, algorithms=["HS256"])
        payload = JWTSchema(**data)

    except InvalidSignatureError as e:
        raise HTTPException(status_code=401, detail="Invalid signature") from e
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail="Signature has expired") from e

    return payload
