from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostCreate(BaseModel):
    content: str
    image_path: Optional[str] = None


class PostOut(BaseModel):
    id: str
    user_id: str
    content: str
    image_path: Optional[str]
    created_at: datetime
