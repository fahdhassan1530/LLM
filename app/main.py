from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.routers import health, website


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Validate settings once at startup (fails fast if OPENAI_API_KEY is missing).
    get_settings()
    yield


app = FastAPI(
    title="FastAPI + RAG Starter",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(website.router)
