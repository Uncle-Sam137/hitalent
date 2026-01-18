from fastapi import FastAPI

from app.core.logging import setup_logging
from app.routers.chats import router as chats_router

setup_logging()

app = FastAPI(title="Chats API", version="1.0.0")

app.include_router(chats_router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
