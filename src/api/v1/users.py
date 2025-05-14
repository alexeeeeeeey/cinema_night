from fastapi import APIRouter

router = APIRouter(prefix="/users")


@router.get("/")
async def get_all_users():
    return "it_works!"
