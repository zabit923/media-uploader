from datetime import datetime

from pydantic import UUID4, BaseModel


class UserCreate(BaseModel):
    username: str


class UserRead(BaseModel):
    id: int
    username: str
    access_token: UUID4
    created_at: datetime
