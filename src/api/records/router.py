from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.users.service import UserService
from core.database.db import get_async_session

from .schemas import AudioRead
from .service import AudioService

router = APIRouter(prefix="/record")
user_service = UserService()
audio_service = AudioService()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=AudioRead)
async def upload_audio(
    user_id: int = File(...),
    access_token: str = File(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
):
    user = await user_service.get_user_by_id(user_id, session)
    if not user or str(user.access_token) != access_token:
        raise HTTPException(status_code=401, detail="Invalid user or token")
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only .wav files are allowed")

    new_audio = await audio_service.create_audio(user_id, file, session)
    return new_audio
