from database.users.schemas import PermissionEnum
from permissions.user import User

ROLE_PERMISSIONS = {
    PermissionEnum.USER: [],
    PermissionEnum.ADMIN: [
        User.CREATE,
        User.READ,
        User.UPDATE,
        User.DELETE,
    ],
}


def get_role_permissions(role: PermissionEnum):
    return ROLE_PERMISSIONS[role]
