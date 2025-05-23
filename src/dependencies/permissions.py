import asyncio
from collections.abc import Awaitable, Callable

from fastapi import Depends, HTTPException, Request, status

from database.users.schemas import UserSchema
from dependencies.unit_of_work import get_uow
from dependencies.users import get_user
from permissions.base import Permission
from permissions.roles import get_role_permissions
from utils.unit_of_work import UnitOfWork

OwnershipCheck = Callable[[Request, UserSchema, UnitOfWork], Awaitable[bool]]


class PermissionChecker:
    def __init__(
        self,
        permissions_required: list[Permission] = None,
        ownership_required: list[OwnershipCheck] = None,
    ):
        self.permissions_required = permissions_required or []
        self.ownership_required = ownership_required or []

    async def __call__(
        self,
        request: Request,
        user: UserSchema = Depends(get_user),
        uow: UnitOfWork = Depends(get_uow),
    ):
        perms = get_role_permissions(user.permission)

        if all(perm in perms for perm in self.permissions_required):
            return

        if self.ownership_required and all(
            await asyncio.gather(
                *(
                    ownership(request, user, uow)
                    for ownership in self.ownership_required
                )
            )
        ):
            return

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
