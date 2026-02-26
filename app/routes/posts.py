# app/routes/posts.py
from fastapi import APIRouter
from app.crud.posts import create_post_db
from app.deps.pagination import pagination_params
from fastapi import Depends
router = APIRouter()


@router.get("/", summary="Posts")
async def get_posts(pagination: dict = Depends(pagination_params)):
    # create_post_db is sync; calling it directly is fine.
    # If create_post_db becomes async you can await it instead.
    return create_post_db(
        limit = pagination["limit"],
        cursor = pagination["cursor"]
    )
