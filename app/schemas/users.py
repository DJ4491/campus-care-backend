from pydantic import BaseModel


class UserPublic(BaseModel):
    id: str
    display_name: str | None
    username: str | None
    avatar_url: str | None


class UserCreate(BaseModel):
    email: str
    username: str
