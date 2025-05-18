from database.movies.models import Movie, Rate
from utils.repository import SQLAlchemyRepository


class MovieRepository(SQLAlchemyRepository):
    model = Movie


class RateRepository(SQLAlchemyRepository):
    model = Rate
