from typing import Union
from app.routes import health, mutual_friend, recommendations, admin,posts_you_may_like,posts
from fastapi import FastAPI
import os
import logging
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO, # Set this to INFO to see our info messages
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="Campus Social Backend", version="0.1.0")
origins = ["http://localhost:8081"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok"}

if __name__ == '__main__':
    port = int(os.getenv("PORT",8080))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0",port=port)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
# app.include_router(
#     recommendations.router, prefix="/recommendations", tags=["recommendations"]
# )
app.include_router(admin.router, prefix="/admin", tags=["admin"])
# app.include_router(mutual_friend.router, prefix="/api/mutual_friends", tags=["Mutual Friend"])
# app.include_router(posts_you_may_like.router, prefix="/api/posts_you_may_like", tags=["Posts Recommendation"])
