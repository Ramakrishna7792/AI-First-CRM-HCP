from fastapi import APIRouter

from app.api.v1.routes import analytics, auth, chat, doctors, interactions, products

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(doctors.router, prefix="/doctors", tags=["doctors"])
api_router.include_router(interactions.router, prefix="/interactions", tags=["interactions"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(chat.router, prefix="/chat", tags=["AI chat"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
