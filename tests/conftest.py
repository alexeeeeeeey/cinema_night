import os
import sys

sys.path.append(os.path.abspath("./src"))


import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from api import main_router
from core.config import settings
from core.init_api import app
from database import Base
from database.users.schemas import UserAddSchema, UserSchema
from dependencies.unit_of_work import UnitOfWork, get_uow
from services.users import UsersService
from utils.auth import Hasher, Tokenizer

engine_test = create_async_engine(settings.TEST_DATABASE_URL)
async_session_test = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="function", autouse=True)
async def setup_test_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine_test.dispose()


@pytest.fixture()
async def test_uow():
    uow = UnitOfWork()
    uow.session_factory = async_session_test
    yield uow


@pytest.fixture()
async def override_uow(test_uow):
    app.dependency_overrides[get_uow] = lambda: test_uow
    yield
    app.dependency_overrides.clear()


@pytest.fixture()
async def user(test_uow: UnitOfWork):
    new_user = UserAddSchema(
        username="aboba",
        password=Hasher.get_password_hash("123"),
        fullname="aboba",
        permission="ADMIN",
    )
    id = await UsersService.add_user(test_uow, new_user)
    yield UserSchema(id=id, **new_user.model_dump())


@pytest.fixture()
async def token(user: UserSchema):
    return Tokenizer.create_access_token(user.id)


@pytest.fixture()
async def client(override_uow):
    app.include_router(main_router)
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test/"
    ) as c:
        yield c
