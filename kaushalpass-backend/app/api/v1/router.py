"""API v1 router — registers all sub-routers."""

from fastapi import APIRouter

from app.api.v1.voice.router import router as voice_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(voice_router)
