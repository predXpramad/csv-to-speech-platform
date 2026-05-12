import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .api.v1.api import api_router
from .api.v1.endpoints.ws import ws_router
from .core.config import settings
from .utils.scheduler import start_scheduler, stop_scheduler
from .storage.file_manager import cleanup_all_temp_files

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.TEMP_AUDIO_DIR, exist_ok=True)
    os.makedirs(settings.ZIP_EXPORTS_DIR, exist_ok=True)
    os.makedirs(settings.METADATA_DIR, exist_ok=True)
    
    # Cleanup on startup
    cleanup_all_temp_files()
    
    start_scheduler()
    yield
    stop_scheduler()

app = FastAPI(title="CSV-to-Speech Platform", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
app.include_router(ws_router, prefix="/ws")
