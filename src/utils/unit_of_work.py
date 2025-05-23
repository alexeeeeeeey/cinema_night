from database.base import async_session_maker
from database.halls.repository import HallRepository, SeatRepository
from database.movies.repository import MovieRepository, RateRepository
from database.users.repository import UserRepository


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.movies = MovieRepository(self.session)
        self.halls = HallRepository(self.session)
        self.seats = SeatRepository(self.session)
        self.rates = RateRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
