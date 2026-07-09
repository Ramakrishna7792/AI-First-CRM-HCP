from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.domain import models as _models  # noqa: F401  Ensures ORM metadata is registered.


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.create_tables_on_start:
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="AI-assisted CRM for healthcare professional interactions.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"name": settings.app_name, "docs": "/docs"}


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "healthy"}
