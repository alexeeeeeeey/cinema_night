import jwt
from datetime import datetime, timedelta
from core.config import settings
from datetime import datetime, timedelta, timezone
from database.auth.schemas import JWTSchema


async def create_jwt(user_id: int, exp: int | None = None) -> str:
    if exp is None:
        exp = int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp())

    payload = JWTSchema(
        user_id=user_id,
        exp=exp,
    )
    return jwt.encode(payload.model_dump(), settings.API_SECRET_TOKEN, algorithm="HS256")
