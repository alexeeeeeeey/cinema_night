from database.users.schemas import PermissionEnum
from permissions.halls import Hall
from permissions.movies import Movie
from permissions.users import User

ROLE_PERMISSIONS = {
    PermissionEnum.USER: [],
    PermissionEnum.ADMIN: [
        User.CREATE,
        User.READ,
        User.UPDATE,
        User.DELETE,
        Movie.CREATE,
        Movie.READ,
        Movie.UPDATE,
        Movie.DELETE,
        Hall.CREATE,
        Hall.READ,
        Hall.UPDATE,
        Hall.DELETE,
    ],
}


def get_role_permissions(role: PermissionEnum):
    return ROLE_PERMISSIONS[role]
