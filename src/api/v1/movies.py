from uuid import UUID

from fastapi import APIRouter, Depends, status

from database.movies.schemas import (
    MovieAddSchema,
    MovieGetSchema,
    MovieIDSchema,
    MovieSchema,
)
from dependencies.permissions import PermissionChecker
from dependencies.unit_of_work import get_uow
from permissions.movies import Movie
from services.movies import MoviesService
from utils.unit_of_work import UnitOfWork

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/")
async def get_all_movies(
    hall_id: UUID | None = None, uow: UnitOfWork = Depends(get_uow)
) -> list[MovieSchema]:
    return await MoviesService.get_movies(uow, hall_id)


@router.get("/{movie_id}")
async def get_movie_by_id(movie_id: UUID, uow=Depends(get_uow)) -> MovieGetSchema:
    return await MoviesService.get_movie_by_id(uow, movie_id)


@router.put(
    "/{movie_id}",
    dependencies=[Depends(PermissionChecker([Movie.UPDATE]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_movie(
    movie_id: UUID, movie: MovieAddSchema, uow=Depends(get_uow)
) -> None:
    return await MoviesService.update_movie(uow, movie_id, movie)


@router.post(
    "/",
    dependencies=[Depends(PermissionChecker([Movie.CREATE]))],
    status_code=status.HTTP_201_CREATED,
)
async def add_movie(movie: MovieAddSchema, uow=Depends(get_uow)) -> MovieIDSchema:
    movie_id = await MoviesService.add_movie(uow, movie)
    return MovieIDSchema(id=movie_id)


@router.delete(
    "/{movie_id}",
    dependencies=[Depends(PermissionChecker([Movie.DELETE]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_movie(movie_id: UUID, uow=Depends(get_uow)) -> None:
    return await MoviesService.delete_movie(uow, movie_id)
