
import pytest
from httpx import AsyncClient

from database.users.schemas import UserLoginSchema, UserSchema


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, user: UserSchema):
    response = await client.post(
        "/api/v1/login",
        json=UserLoginSchema(username=user.username, password="123").model_dump(),
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, token: str, user: UserSchema):
    response = await client.get(
        f"/api/v1/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["fullname"] == "aboba"
