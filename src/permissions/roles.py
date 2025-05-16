from enum import Enum

from permissions.user import User


class Role(str, Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    USER = "USER"


ROLE_PERMISSIONS = {
    Role.ADMINISTRATOR: [
        User.CREATE,
        User.READ,
        User.UPDATE,
        User.DELETE,
    ]
}


def get_role_permissions(role: Role):
    return ROLE_PERMISSIONS[role]
