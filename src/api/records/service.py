from fastapi import UploadFile
from sqlalchemy import select
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
    ) -> AudioRead:
        audio_file = await save_file(file)
        new_audio = AudioRecord(user_id=user_id, audio_file=audio_file)
        session.add(new_audio)
        await session.commit()
        return AudioRead(
            download_url=f"http://{settings.run.host}:{settings.run.port}/record?audio_id={new_audio.id}&user_id={user_id}"
        )

    @staticmethod
    async def get_audio(
        audio_id: str,
        session: AsyncSession,
    ) -> AudioRecord:
        statement = select(AudioRecord).where(AudioRecord.id == audio_id)
        result = await session.execute(statement)
        audio = result.scalars().first()
        return audio
