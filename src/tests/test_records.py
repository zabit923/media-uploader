import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.factories import UserFactory


@pytest.mark.asyncio
async def test_upload_audio_success(
    client: AsyncClient, test_session: AsyncSession, tmp_path
):
    user = UserFactory()
    test_session.add(user)
    await test_session.commit()

    temp_audio = tmp_path / "test_audio.wav"
    temp_audio.write_bytes(b"Fake WAV data")

    with temp_audio.open("rb") as file:
        response = await client.post(
            "/record",
            files={
                "user_id": (None, str(user.id)),
                "access_token": (None, str(user.access_token)),
                "file": ("test_audio.wav", file, "audio/wav"),
            },
        )

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_upload_audio_invalid_token(
    client: AsyncClient, test_session: AsyncSession, tmp_path
):
    user = UserFactory()
    test_session.add(user)
    await test_session.commit()

    temp_audio = tmp_path / "test_audio.wav"
    temp_audio.write_bytes(b"Fake WAV data")

    with temp_audio.open("rb") as file:
        response = await client.post(
            "/record",
            files={
                "user_id": (None, str(user.id)),
                "access_token": (None, "invalid_token"),
                "file": ("test_audio.wav", file, "audio/wav"),
            },
        )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid user or token"


@pytest.mark.asyncio
async def test_upload_audio_invalid_format(
    client: AsyncClient, test_session: AsyncSession, tmp_path
):
    user = UserFactory()
    test_session.add(user)
    await test_session.commit()

    temp_audio = tmp_path / "test_audio.mp3"
    temp_audio.write_bytes(b"Fake MP3 data")

    with temp_audio.open("rb") as file:
        response = await client.post(
            "/record",
            files={
                "user_id": (None, str(user.id)),
                "access_token": (None, str(user.access_token)),
                "file": ("test_audio.mp3", file, "audio/mp3"),
            },
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only .wav files are allowed"
