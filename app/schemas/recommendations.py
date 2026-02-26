from pydantic import BaseModel
from typing import List


class RecItem(BaseModel):
    user_id: str
    score: float


class RecList(BaseModel):
    recs: List[RecItem]
