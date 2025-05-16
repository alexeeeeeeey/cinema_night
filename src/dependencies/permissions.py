from fastapi import Depends, HTTPException, status

from database.users.schemas import UserSchema
from dependencies.users import get_user
from permissions.base import Permission
from permissions.roles import get_role_permissions


class PermissionChecker:
    def __init__(self, permissions_required: list[Permission]):
        self.permissions_required = permissions_required

    def __call__(self, user: UserSchema = Depends(get_user)):
        perms = get_role_permissions(user.permission)
        for perm in self.permissions_required:
            if perm not in perms:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
                )
        return user
