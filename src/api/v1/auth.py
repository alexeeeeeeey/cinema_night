
from fastapi import APIRouter, Cookie, Depends, Response, status
from fastapi.exceptions import HTTPException

from database.auth.schemas import AccessJWT
from database.users.schemas import UserIDSchema, UserLoginSchema, UserRegisterSchema
from dependencies.unit_of_work import get_uow
from services.auth import AuthService
from utils.auth import Tokenizer
from utils.unit_of_work import UnitOfWork

router = APIRouter(tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user: UserRegisterSchema, uow: UnitOfWork = Depends(get_uow)
) -> UserIDSchema:
    user_id = await AuthService.register_user(user, uow)
    return UserIDSchema(id=user_id)


@router.post("/login")
async def login(
    user: UserLoginSchema, response: Response, uow: UnitOfWork = Depends(get_uow)
) -> AccessJWT:
    user_db = await AuthService.login_user(uow, user)

    refresh_token = Tokenizer.create_refresh_token(user_db.id)
    access_token = Tokenizer.create_access_token(user_db.id)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
    )

    return AccessJWT(access_token=access_token)


@router.post("/refresh")
async def refresh(refresh_token: str | None = Cookie(default=None)) -> AccessJWT:
    if not refresh_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "No refresh token")

    user = Tokenizer.validate_token(refresh_token)
    access_token = Tokenizer.create_access_token(user.user_id)

    return AccessJWT(access_token=access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(key="refresh_token")
