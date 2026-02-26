# from fastapi import APIRouter
# from app.crud.recommendations import get_mutual_friend_recommendations_for_user,get_posts_recommendations_for_user
# from fastapi import Depends
# from app.deps.auth import get_current_user
# from fastapi import HTTPException

# router = APIRouter()


# @router.get("/", summary="Mutual Friends")
# async def get_posts():  # current_user = Depends(get_current_user)
#     try:
#         user_id = "00000000-0000-0000-0000-000000000001"
#         return get_posts_recommendations_for_user(user_id)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except KeyError:
#         raise HTTPException(status_code=404, detail="User not found")
#     except Exception:
#         raise HTTPException(status_code=500, detail="Internal Server Error")
