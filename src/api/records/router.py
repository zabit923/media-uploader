import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import FileResponse

from api.users.service import UserService
from config import media_dir
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


@router.get("", status_code=status.HTTP_201_CREATED)
async def download_audio(
    audio_id: str = Query(...),
    user_id: int = Query(...),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        uuid.UUID(audio_id, version=4)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid audio_id format.")
    user = await user_service.get_user_by_id(user_id, session)
    audio = await audio_service.get_audio(audio_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if not audio:
        raise HTTPException(status_code=404, detail="Audio not found.")
    file_path = os.path.join(media_dir, audio.audio_file)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio not exists.")
    return FileResponse(file_path, filename=audio.audio_file, media_type="audio/mp3")
