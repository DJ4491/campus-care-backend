from typing import Optional
from fastapi import Query

def pagination_params(limit: int = Query(5, ge=1, le=100), cursor: Optional[str] = Query(None)):
    return {"limit": limit, "cursor": cursor}
