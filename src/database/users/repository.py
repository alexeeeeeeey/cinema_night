from database.users.models import User
from utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
