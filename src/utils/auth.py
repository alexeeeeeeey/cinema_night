from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from fastapi import HTTPException, status
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from passlib.context import CryptContext

from core.config import settings
from database.auth.schemas import JWTSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Tokenizer:
    @staticmethod
    def create_refresh_token(user_id: UUID, exp: int | None = None) -> str:
        if exp is None:
            exp = int((datetime.now(UTC) + timedelta(days=30)).timestamp())

        payload = JWTSchema(
            user_id=user_id,
            exp=exp,
        )
        return jwt.encode(
            payload.model_dump(mode="json"),
            settings.API_SECRET_TOKEN,
            algorithm="HS256",
        )

    @staticmethod
    def create_access_token(user_id: UUID, exp: int | None = None) -> str:
        if exp is None:
            exp = int((datetime.now(UTC) + timedelta(minutes=5)).timestamp())

        payload = JWTSchema(
            user_id=user_id,
            exp=exp,
        )
        return jwt.encode(
            payload.model_dump(mode="json"),
            settings.API_SECRET_TOKEN,
            algorithm="HS256",
        )

    @staticmethod
    def validate_token(token: str) -> JWTSchema:
        try:
            data: dict = jwt.decode(
                token, settings.API_SECRET_TOKEN, algorithms=["HS256"]
            )
            payload = JWTSchema(**data)

        except InvalidSignatureError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature"
            ) from e
        except ExpiredSignatureError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature has expired"
            ) from e

        return payload


class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)
