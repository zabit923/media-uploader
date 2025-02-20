from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database.models import User

from .schemas import UserCreate


class UserService:
    @staticmethod
    async def create_user(
        user_data: UserCreate,
        session: AsyncSession,
    ) -> User:
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @staticmethod
    async def get_user_by_access_token(
        access_token: str, session: AsyncSession
    ) -> User:
        statement = select(User).where(User.access_token == access_token)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user

    @staticmethod
    async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user

    @staticmethod
    async def get_user_by_username(username: str, session: AsyncSession) -> User:
        statement = select(User).where(User.username == username)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user

    async def user_exists(self, username: str, session: AsyncSession) -> True | False:
        user = await self.get_user_by_username(username, session)
        return True if user else False
