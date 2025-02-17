from fastapi import HTTPException
from sqladmin.authentication import AuthenticationBackend
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from api.users.service import UserService
from core.database.db import async_session_maker
from core.database.models import User

user_service = UserService()


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)

    async def login(self, request: Request) -> bool:
        async with async_session_maker() as session:
            form = await request.form()
            username, access_token = form["username"], form["password"]
            user = await user_service.get_user_by_username(username, session)
            if not user or str(user.access_token) != access_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or access token.",
                )
            request.session.update({"token": str(user.access_token)})
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | User:
        token = request.session.get("token")
        if not token:
            return RedirectResponse(
                request.url_for("admin:login"), status_code=status.HTTP_302_FOUND
            )

        async with async_session_maker() as session:
            user = await user_service.get_user_by_access_token(token, session)
            if not user:
                return RedirectResponse(
                    request.url_for("admin:login"), status_code=status.HTTP_302_FOUND
                )
            return user
