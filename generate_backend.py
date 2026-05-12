import os

base_dir = r"d:\02 Projects\TTS ML Model"
backend_dir = os.path.join(base_dir, "backend")

files = {}

files["requirements.txt"] = """fastapi
uvicorn
edge-tts
pandas
aiofiles
APScheduler
pydantic
python-multipart
"""

files["Dockerfile"] = """FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

files[".env"] = """
# Environment configuration
"""

files["app/main.py"] = """import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .api.v1.api import api_router
from .api.v1.endpoints.ws import ws_router
from .core.config import settings
from .utils.scheduler import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.TEMP_AUDIO_DIR, exist_ok=True)
    os.makedirs(settings.ZIP_EXPORTS_DIR, exist_ok=True)
    os.makedirs(settings.METADATA_DIR, exist_ok=True)
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
"""

files["app/core/config.py"] = """import os

class Settings:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    STORAGE_DIR = os.path.join(BASE_DIR, "storage")
    UPLOAD_DIR = os.path.join(STORAGE_DIR, "uploads")
    TEMP_AUDIO_DIR = os.path.join(STORAGE_DIR, "temp_audio")
    ZIP_EXPORTS_DIR = os.path.join(STORAGE_DIR, "zip_exports")
    METADATA_DIR = os.path.join(STORAGE_DIR, "metadata")
    ZIP_EXPIRATION_HOURS = 72

settings = Settings()
"""

files["app/api/v1/api.py"] = """from fastapi import APIRouter
from .endpoints import tts

api_router = APIRouter()
api_router.include_router(tts.router, tags=["tts"])
"""

files["app/api/v1/endpoints/tts.py"] = """import os
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
    
    background_tasks.add_task(process_conversion, job_id, file_path, req.textCol, req.voice)
    
    return {
        "job_id": job_id,
        "websocket_url": f"/ws/progress/{job_id}"
    }

@router.get("/download/{job_id}")
async def download_zip(job_id: str):
    zip_path = os.path.join(settings.ZIP_EXPORTS_DIR, f"{job_id}.zip")
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="ZIP file not found or expired")
    return FileResponse(zip_path, media_type="application/zip", filename=f"{job_id}.zip")

@router.delete("/download/{job_id}")
async def delete_zip(job_id: str):
    delete_job_files(job_id)
    return {"status": "deleted"}
"""

files["app/api/v1/endpoints/ws.py"] = """from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import ws_manager

ws_router = APIRouter()

@ws_router.websocket("/progress/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await ws_manager.connect(websocket, job_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, job_id)
"""

files["app/websocket/manager.py"] = """import json
from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, job_id: str):
        await websocket.accept()
        if job_id not in self.active_connections:
            self.active_connections[job_id] = []
        self.active_connections[job_id].append(websocket)

    def disconnect(self, websocket: WebSocket, job_id: str):
        if job_id in self.active_connections:
            if websocket in self.active_connections[job_id]:
                self.active_connections[job_id].remove(websocket)
            if not self.active_connections[job_id]:
                del self.active_connections[job_id]

    async def broadcast(self, job_id: str, message: dict):
        if job_id in self.active_connections:
            for connection in self.active_connections[job_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    pass

ws_manager = ConnectionManager()
"""

files["app/services/edge_tts_service.py"] = """import os
import edge_tts
import pandas as pd
from app.websocket.manager import ws_manager
from app.utils.zip_manager import create_zip
from app.storage.file_manager import save_metadata, delete_temp_audio
from app.core.config import settings
from datetime import datetime, timedelta

async def get_all_voices():
    voices = await edge_tts.list_voices()
    languages_map = {}
    for v in voices:
        locale = v["Locale"]
        lang_code = locale.split("-")[0]
        if locale not in languages_map:
            languages_map[locale] = {
                "language": lang_code,
                "locale": locale,
                "voices": []
            }
        languages_map[locale]["voices"].append({
            "voice_name": v["Name"],
            "display_name": v["FriendlyName"],
            "gender": v["Gender"]
        })
    return {"languages": list(languages_map.values())}

async def process_conversion(job_id: str, file_path: str, text_col: str, voice: str):
    try:
        df = pd.read_csv(file_path)
    except:
        return
        
    total_rows = len(df)
    temp_dir = os.path.join(settings.TEMP_AUDIO_DIR, job_id)
    os.makedirs(temp_dir, exist_ok=True)
    
    success_count = 0
    failure_count = 0
    failed_rows = []
    
    await ws_manager.broadcast(job_id, {
        "status": "processing",
        "progress": 0,
        "processedRows": 0,
        "totalRows": total_rows,
        "failedRows": []
    })

    for index, row in df.iterrows():
        text = str(row.get(text_col, ""))
        if not text.strip():
            failure_count += 1
            failed_rows.append({"row": index + 1, "error": "Empty text"})
            continue
            
        audio_path = os.path.join(temp_dir, f"{index + 1}.mp3")
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(audio_path)
            success_count += 1
        except Exception as e:
            failure_count += 1
            failed_rows.append({"row": index + 1, "error": str(e)})
            
        processed = success_count + failure_count
        progress = int((processed / total_rows) * 100)
        
        await ws_manager.broadcast(job_id, {
            "job_id": job_id,
            "row_id": str(index + 1),
            "status": "processing",
            "progress": progress,
            "processedRows": processed,
            "success_count": success_count,
            "failure_count": failure_count,
            "failedRows": failed_rows
        })

    zip_path = os.path.join(settings.ZIP_EXPORTS_DIR, f"{job_id}.zip")
    create_zip(temp_dir, zip_path)
    delete_temp_audio(job_id)
    
    expires_at = datetime.utcnow() + timedelta(hours=settings.ZIP_EXPIRATION_HOURS)
    save_metadata(job_id, {
        "job_id": job_id,
        "status": "completed",
        "success_count": success_count,
        "failure_count": failure_count,
        "expires_at": expires_at.isoformat()
    })
    
    await ws_manager.broadcast(job_id, {
        "status": "completed",
        "progress": 100,
        "processedRows": total_rows,
        "zip_url": f"/api/download/{job_id}",
        "expires_in_hours": settings.ZIP_EXPIRATION_HOURS
    })
"""

files["app/utils/zip_manager.py"] = """import os
import zipfile

def create_zip(source_dir: str, output_path: str):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
"""

files["app/storage/file_manager.py"] = """import os
import json
import shutil
from app.core.config import settings

def save_metadata(job_id: str, data: dict):
    path = os.path.join(settings.METADATA_DIR, f"{job_id}.json")
    with open(path, "w") as f:
        json.dump(data, f)

def get_metadata(job_id: str) -> dict:
    path = os.path.join(settings.METADATA_DIR, f"{job_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def delete_temp_audio(job_id: str):
    temp_dir = os.path.join(settings.TEMP_AUDIO_DIR, job_id)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

def delete_job_files(job_id: str):
    zip_path = os.path.join(settings.ZIP_EXPORTS_DIR, f"{job_id}.zip")
    meta_path = os.path.join(settings.METADATA_DIR, f"{job_id}.json")
    upload_path = os.path.join(settings.UPLOAD_DIR, f"{job_id}.csv")
    
    if os.path.exists(zip_path): os.remove(zip_path)
    if os.path.exists(meta_path): os.remove(meta_path)
    if os.path.exists(upload_path): os.remove(upload_path)
    delete_temp_audio(job_id)
"""

files["app/utils/scheduler.py"] = """import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.core.config import settings
from app.storage.file_manager import get_metadata, delete_job_files

scheduler = BackgroundScheduler()

def cleanup_expired_zips():
    if not os.path.exists(settings.METADATA_DIR):
        return
    for filename in os.listdir(settings.METADATA_DIR):
        if not filename.endswith(".json"):
            continue
        job_id = filename.replace(".json", "")
        meta = get_metadata(job_id)
        if "expires_at" in meta:
            try:
                expires_at = datetime.fromisoformat(meta["expires_at"])
                if datetime.utcnow() > expires_at:
                    delete_job_files(job_id)
            except:
                pass

def start_scheduler():
    scheduler.add_job(cleanup_expired_zips, 'interval', hours=1)
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()
"""

for rel_path, content in files.items():
    full_path = os.path.join(backend_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Backend files generated successfully.")

# Frontend patches
frontend_files = {}

frontend_files["vite.config.ts"] = """import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true
      },
      "/ws": {
        target: "ws://127.0.0.1:8000",
        ws: true
      }
    }
  }
})
"""

frontend_files["src/services/api.ts"] = """import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

export const getVoices = async () => {
  const res = await api.get('/voices');
  const data = res.data;
  const flatVoices: any[] = [];
  if (data.languages) {
    data.languages.forEach((lang: any) => {
      lang.voices.forEach((voice: any) => {
        flatVoices.push({
          Name: voice.display_name,
          ShortName: voice.voice_name,
          Gender: voice.gender,
          Locale: lang.locale
        });
      });
    });
  } else {
    return data;
  }
  return flatVoices;
};

export const uploadCsv = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await api.post('/upload', formData);
  return res.data;
};

export const startConversion = async (jobId: string, textCol: string, voice: string) => {
  const res = await api.post('/convert', { jobId, textCol, voice });
  return res.data;
};

export const deleteJob = async (jobId: string) => {
  const res = await api.delete(`/download/${jobId}`);
  return res.data;
};
"""

frontend_files["src/pages/Dashboard.tsx"] = """import React, { useEffect } from 'react';
import { UploadZone } from '@/components/features/tts/UploadZone';
import { ConversionForm } from '@/components/features/tts/ConversionForm';
import { ProgressDashboard } from '@/components/features/tts/ProgressDashboard';
import { DownloadCard } from '@/components/features/tts/DownloadCard';
import { useAppStore } from '@/store/useAppStore';
import { getVoices } from '@/services/api';

export const Dashboard = () => {
  const { file, job, setVoices } = useAppStore();

  useEffect(() => {
    getVoices().then(setVoices).catch(console.error);
  }, []);

  return (
    <div className="space-y-8 pb-12 animate-in fade-in duration-500">
      <div className="text-center space-y-2 mt-8">
        <h2 className="text-3xl font-bold tracking-tight">Batch Convert CSV to Audio</h2>
        <p className="text-muted-foreground max-w-xl mx-auto">
          Upload your dataset, select your target column and preferred voice, and we'll generate speech audio for every row instantly.
        </p>
      </div>

      {!file && !job && <UploadZone />}
      
      {file && job?.status === 'pending' && <ConversionForm />}
      
      {(job?.status === 'processing' || job?.status === 'completed') && (
        <ProgressDashboard />
      )}
      
      {job?.status === 'completed' && <DownloadCard />}
    </div>
  );
};
"""

frontend_files["src/components/features/tts/UploadZone.tsx"] = """import React, { useState } from 'react';
import { UploadCloud } from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';
import { uploadCsv } from '@/services/api';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export const UploadZone = () => {
  const { setFile, setHeaders, setJob } = useAppStore();
  const [isLoading, setIsLoading] = useState(false);

  const handleUpload = async (file: File) => {
    if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
      alert('Please upload a valid CSV file.');
      return;
    }
    
    setIsLoading(true);
    try {
      const data = await uploadCsv(file);
      setFile(file);
      setHeaders(data.headers);
      setJob({
        jobId: data.jobId || data.file_id,
        status: 'pending',
        progress: 0,
        totalRows: data.totalRows || data.row_count,
        processedRows: 0,
        failedRows: []
      });
    } catch (err) {
      console.error(err);
      alert('Upload failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto mt-8 border-dashed border-2 bg-muted/20">
      <CardContent className="p-12 flex flex-col items-center justify-center text-center">
        <UploadCloud className="w-12 h-12 text-muted-foreground mb-4" />
        <h3 className="text-xl font-semibold mb-2">Upload your CSV</h3>
        <p className="text-muted-foreground mb-6">Drag and drop your file here, or click to browse.</p>
        <div className="relative">
          <Button disabled={isLoading}>{isLoading ? 'Uploading...' : 'Select File'}</Button>
          <input 
            type="file" 
            accept=".csv"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            onChange={(e) => e.target.files && handleUpload(e.target.files[0])}
            disabled={isLoading}
          />
        </div>
      </CardContent>
    </Card>
  );
};
"""

frontend_files["src/components/features/tts/ConversionForm.tsx"] = """import React from 'react';
import { useAppStore } from '@/store/useAppStore';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { startConversion } from '@/services/api';
import { connectWebSocket } from '@/services/websocket';

export const ConversionForm = () => {
  const { headers, voices, selectedTextCol, setSelectedTextCol, selectedVoice, setSelectedVoice, job } = useAppStore();

  const handleStart = async () => {
    if (!job || !selectedTextCol || !selectedVoice) return;
    
    try {
      await startConversion(job.jobId, selectedTextCol, selectedVoice);
      connectWebSocket(job.jobId);
    } catch (err) {
      console.error(err);
      alert('Failed to start conversion');
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto mt-8">
      <CardHeader>
        <CardTitle>Configuration</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-2">
          <label className="text-sm font-medium">Text Column</label>
          <select 
            className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
            value={selectedTextCol} 
            onChange={(e) => setSelectedTextCol(e.target.value)}
          >
            <option value="">Select column...</option>
            {headers.map(h => <option key={h} value={h}>{h}</option>)}
          </select>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium">Voice</label>
          <select 
            className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
            value={selectedVoice} 
            onChange={(e) => setSelectedVoice(e.target.value)}
          >
            <option value="">Select voice...</option>
            {voices.map(v => <option key={v.ShortName} value={v.ShortName}>{v.Name} ({v.Locale})</option>)}
          </select>
        </div>

        <Button 
          className="w-full" 
          disabled={!selectedTextCol || !selectedVoice}
          onClick={handleStart}
        >
          Start Conversion
        </Button>
      </CardContent>
    </Card>
  );
};
"""

frontend_dir = os.path.join(base_dir, "frontend")
for rel_path, content in frontend_files.items():
    full_path = os.path.join(frontend_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Frontend files patched successfully.")
