from uuid import UUID

from database.movies.schemas import MovieAddSchema, MovieSchema
from utils.unit_of_work import UnitOfWork


class MoviesService:
    @staticmethod
    async def get_movies(uow: UnitOfWork, hall_id: UUID | None = None):
        filters = {}
        if hall_id:
            filters["hall_id"] = hall_id

        async with uow:
            movies = await uow.movies.find_all(MovieSchema, **filters)
            return movies

    @staticmethod
    async def get_movie_by_id(uow: UnitOfWork, movie_id: UUID):
        async with uow:
            movies = await uow.movies.find_one(MovieSchema, id=movie_id)
            return movies

    @staticmethod
    async def add_movie(uow: UnitOfWork, movie: MovieAddSchema):
        movie_dict = movie.model_dump()
        async with uow:
            movie_id = await uow.movies.add_one(movie_dict)
            await uow.commit()
            return movie_id

    @staticmethod
    async def update_movie(uow: UnitOfWork, movie_id: UUID, movie: MovieAddSchema):
        movie_dict = movie.model_dump()
        async with uow:
            movie_id = await uow.movies.edit_one(movie_id, movie_dict)
            await uow.commit()
            return movie_id

    @staticmethod
    async def delete_movie(uow: UnitOfWork, movie_id: UUID):
        async with uow:
            movie_id = await uow.movies.delete_one(id=movie_id)
            await uow.commit()
            return movie_id
