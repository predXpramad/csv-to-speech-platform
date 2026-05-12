import os
import uuid
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.core.config import settings
from app.services.edge_tts_service import process_conversion, get_all_voices
from app.storage.file_manager import delete_job_files, save_metadata
from pydantic import BaseModel

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV is allowed.")
    
    file_id = str(uuid.uuid4())
    file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.csv")
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
        
    headers = df.columns.tolist()
    row_count = len(df)
    
    return {
        "file_id": file_id,
        "jobId": file_id,
        "headers": headers,
        "row_count": row_count,
        "totalRows": row_count
    }

@router.get("/voices")
async def fetch_voices():
    return await get_all_voices()

class ConvertRequest(BaseModel):
    jobId: str
    textCol: str
    voice: str
    startRow: int = None
    endRow: int = None

@router.post("/convert")
async def start_conversion(req: ConvertRequest, background_tasks: BackgroundTasks):
    job_id = req.jobId
    file_path = os.path.join(settings.UPLOAD_DIR, f"{job_id}.csv")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    save_metadata(job_id, {
        "job_id": job_id,
        "status": "pending"
    })
    
    background_tasks.add_task(process_conversion, job_id, file_path, req.textCol, req.voice, req.startRow, req.endRow)
    
    return {
        "job_id": job_id,
        "websocket_url": f"/ws/progress/{job_id}"
    }

from app.services.edge_tts_service import cancel_job

@router.post("/stop/{job_id}")
async def stop_conversion(job_id: str):
    cancel_job(job_id)
    return {"status": "stopping"}

@router.get("/download/{job_id}")
async def download_zip(job_id: str):
    zip_path = os.path.join(settings.ZIP_EXPORTS_DIR, f"{job_id}.zip")
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="ZIP file not found or expired")
        
    from app.storage.file_manager import get_metadata
    meta = get_metadata(job_id)
    download_filename = meta.get("download_filename", f"{job_id}.zip")
    
    return FileResponse(zip_path, media_type="application/zip", filename=download_filename)

@router.delete("/download/{job_id}")
async def delete_zip(job_id: str):
    delete_job_files(job_id)
    return {"status": "deleted"}
