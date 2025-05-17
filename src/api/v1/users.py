from uuid import UUID

from fastapi import APIRouter, Depends, status

from database.users.schemas import UserAddSchema, UserSchema
from dependencies.permissions import PermissionChecker
from dependencies.unit_of_work import get_uow
from permissions.users import User
from services.users import UsersService
from utils.unit_of_work import UnitOfWork

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", dependencies=[Depends(PermissionChecker([User.READ]))])
async def get_all_users(uow: UnitOfWork = Depends(get_uow)) -> list[UserSchema]:
    return await UsersService.get_users(uow)


@router.get(
    "/{user_id}", dependencies=[Depends(PermissionChecker([User.READ], [User.is_user]))]
)
async def get_user_by_id(user_id: UUID, uow=Depends(get_uow)) -> UserSchema:
    return await UsersService.get_user_by_id(uow, user_id)


@router.put(
    "/{user_id}",
    dependencies=[Depends(PermissionChecker([User.UPDATE], [User.is_user]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_user(user_id: UUID, user: UserAddSchema, uow=Depends(get_uow)) -> None:
    return await UsersService.update_user(uow, user_id, user)


@router.post(
    "/",
    dependencies=[Depends(PermissionChecker([User.CREATE]))],
    status_code=status.HTTP_201_CREATED,
)
async def add_user(user: UserAddSchema, uow=Depends(get_uow)) -> UUID:
    return await UsersService.add_user(uow, user)


@router.delete(
    "/{user_id}",
    dependencies=[Depends(PermissionChecker([User.DELETE], [User.is_user]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(user_id: UUID, uow=Depends(get_uow)) -> None:
    return await UsersService.delete_user(uow, user_id)
