from database.halls.models import Hall, Seat
from utils.repository import SQLAlchemyRepository


class HallRepository(SQLAlchemyRepository):
    model = Hall


class SeatRepository(SQLAlchemyRepository):
    model = Seat
