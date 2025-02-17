from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.database.db import get_async_session

from .schemas import UserCreate, UserRead
from .service import UserService

router = APIRouter(prefix="/users")
user_service = UserService()


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    username_exist = await user_service.get_user_by_username(
        user_data.username, session
    )
    if username_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already taken.",
        )
    new_user = await user_service.create_user(user_data, session)
    return new_user
