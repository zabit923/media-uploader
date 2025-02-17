from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from api.records.schemas import AudioRead
from config import settings
from core.database.models import AudioRecord
from core.utils import save_file


class AudioService:
    @staticmethod
    async def create_audio(
        user_id: int,
        file: UploadFile,
        session: AsyncSession,
    ):
        audio_file = await save_file(file)
        new_audio = AudioRecord(user_id=user_id, audio_file=audio_file)
        session.add(new_audio)
        await session.commit()
        return AudioRead(
            download_url=f"http://{settings.run.host}:{settings.run.port}/record?id={new_audio.id}&user={user_id}"
        )
