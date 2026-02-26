from fastapi import APIRouter, Depends
from app.deps.auth import get_current_user

router = APIRouter()


@router.get("/people-you-may-know")
async def people_you_may_know(current_user=Depends(get_current_user)):
    # TODO: implement rec_engine logic; for now return empty list with user id for tests
    return {"user_id": current_user["user_id"], "recommendations": []}
