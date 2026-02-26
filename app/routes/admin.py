from fastapi import APIRouter, Depends, HTTPException, status
from app.deps.auth import get_current_user
from app.core.config import settings

router = APIRouter()


@router.post("/cleanup")
async def admin_cleanup(current_user=Depends(get_current_user)):
    # For now, we simply disallow unless the user is an admin by claim
    claims = current_user.get("claims", {})
    if not claims.get("role") == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin required"
        )
    # TODO: perform admin cleanup using service_supabase
    return {"status": "ok", "message": "cleanup queued"}
