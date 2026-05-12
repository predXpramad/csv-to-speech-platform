import os
import asyncio
import edge_tts
import pandas as pd
from app.websocket.manager import ws_manager
from app.utils.zip_manager import create_zip
from app.storage.file_manager import save_metadata, delete_temp_audio
from app.core.config import settings
from datetime import datetime, timedelta

cancellation_tokens = set()

def cancel_job(job_id: str):
    cancellation_tokens.add(job_id)

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

async def process_conversion(job_id: str, file_path: str, text_col: str, voice: str, start_row: int = None, end_row: int = None):
    try:
        df = pd.read_csv(file_path)
    except:
        return
        
    original_len = len(df)
    start_idx = 0
    end_idx = original_len
    
    if start_row is not None and end_row is not None:
        start_idx = max(0, start_row - 1)
        end_idx = min(original_len, end_row)
        df = df.iloc[start_idx:end_idx]
        
    actual_start = start_idx + 1
    actual_end = end_idx
    
    # e.g., "en-US-AriaNeural" -> lang_short="en", voice_short="AriaNeural"
    voice_parts = voice.split("-")
    if len(voice_parts) >= 3:
        lang_short = voice_parts[0]
        voice_short = "-".join(voice_parts[2:])
    else:
        lang_short = "Unknown"
        voice_short = voice
        
    download_filename = f"{actual_start}-{actual_end}-{lang_short}-{voice_short}.zip"
        
    total_rows = len(df)
    if total_rows == 0:
        total_rows = 1
        
    temp_dir = os.path.join(settings.TEMP_AUDIO_DIR, job_id)
    os.makedirs(temp_dir, exist_ok=True)
    
    success_count = 0
    failure_count = 0
    failed_rows = []
    
    if job_id in cancellation_tokens:
        cancellation_tokens.remove(job_id)
    
    await ws_manager.broadcast(job_id, {
        "status": "processing",
        "progress": 0,
        "processedRows": 0,
        "totalRows": total_rows,
        "failedRows": []
    })

    # High Concurrency Semaphore
    sem = asyncio.Semaphore(35)
    
    async def process_row(idx, row):
        if job_id in cancellation_tokens:
            return (idx, False, "Cancelled")
            
        text = str(row.get(text_col, ""))
        if not text.strip():
            return (idx, False, "Empty text")
            
        audio_path = os.path.join(temp_dir, f"{idx + 1}.mp3")
        
        async with sem:
            try:
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(audio_path)
                return (idx, True, None)
            except Exception as e:
                return (idx, False, str(e))

    tasks = [asyncio.create_task(process_row(idx, row)) for idx, row in df.iterrows()]

    for coro in asyncio.as_completed(tasks):
        if job_id in cancellation_tokens:
            break
            
        idx, success, error = await coro
        
        if success:
            success_count += 1
        else:
            failure_count += 1
            if error != "Cancelled":
                failed_rows.append({"row": idx + 1, "error": error})
                
        processed = success_count + failure_count
        progress = int((processed / total_rows) * 100)
        
        if processed % 5 == 0 or processed == total_rows:
            await ws_manager.broadcast(job_id, {
                "job_id": job_id,
                "status": "processing",
                "progress": progress,
                "processedRows": processed,
                "totalRows": total_rows,
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
        "expires_at": expires_at.isoformat(),
        "download_filename": download_filename
    })
    
    if job_id in cancellation_tokens:
        cancellation_tokens.remove(job_id)
    
    await ws_manager.broadcast(job_id, {
        "status": "completed",
        "progress": 100,
        "processedRows": success_count + failure_count,
        "totalRows": total_rows,
        "zip_url": f"/api/download/{job_id}",
        "expires_in_hours": settings.ZIP_EXPIRATION_HOURS
    })
