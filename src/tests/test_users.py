import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import User
from core.factories import UserFactory


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient, test_session: AsyncSession):
    response = await client.post(
        "/users/register",
        json={"username": "testuser"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"

    user = await test_session.get(User, data["id"])
    assert user is not None
    assert user.username == "testuser"


@pytest.mark.asyncio
async def test_register_user_duplicate_username(
    client: AsyncClient, test_session: AsyncSession
):
    user = UserFactory(username="testuser")
    test_session.add(user)
    await test_session.commit()
    response = await client.post(
        "/users/register",
        json={"username": "testuser"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "This username is already taken."


@pytest.mark.asyncio
async def test_register_user_invalid_data(client: AsyncClient):
    response = await client.post(
        "/users/register",
        json={"usernameee": "testuser"},
    )
    assert response.status_code == 422
