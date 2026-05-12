from fastapi import APIRouter
from .endpoints import tts

api_router = APIRouter()
api_router.include_router(tts.router, tags=["tts"])
