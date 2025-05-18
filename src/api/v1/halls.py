from uuid import UUID

from fastapi import APIRouter, Depends, status

from database.halls.schemas import (
    HallAddSchema,
    HallGetSchema,
    HallIDSchema,
    HallSchema,
)
from dependencies.permissions import PermissionChecker
from dependencies.unit_of_work import get_uow
from permissions.halls import Hall
from services.halls import HallsService
from utils.unit_of_work import UnitOfWork

router = APIRouter(prefix="/halls", tags=["Halls"])


@router.get("/")
async def get_all_halls(uow: UnitOfWork = Depends(get_uow)) -> list[HallSchema]:
    return await HallsService.get_halls(uow)


@router.get("/{hall_id}")
async def get_hall_by_id(hall_id: UUID, uow=Depends(get_uow)) -> HallGetSchema:
    return await HallsService.get_hall_by_id(uow, hall_id)


@router.put(
    "/{hall_id}",
    dependencies=[Depends(PermissionChecker([Hall.UPDATE]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_hall(hall_id: UUID, hall: HallAddSchema, uow=Depends(get_uow)) -> None:
    return await HallsService.update_hall(uow, hall_id, hall)


@router.post(
    "/",
    dependencies=[Depends(PermissionChecker([Hall.CREATE]))],
    status_code=status.HTTP_201_CREATED,
)
async def add_hall(hall: HallAddSchema, uow=Depends(get_uow)) -> HallIDSchema:
    hall_id = await HallsService.add_hall(uow, hall)
    return HallIDSchema(id=hall_id)


@router.delete(
    "/{hall_id}",
    dependencies=[Depends(PermissionChecker([Hall.DELETE]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_hall(hall_id: UUID, uow=Depends(get_uow)) -> None:
    return await HallsService.delete_hall(uow, hall_id)
