import os
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

def cleanup_all_temp_files():
    if os.path.exists(settings.TEMP_AUDIO_DIR):
        for item in os.listdir(settings.TEMP_AUDIO_DIR):
            item_path = os.path.join(settings.TEMP_AUDIO_DIR, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
                
    if os.path.exists(settings.UPLOAD_DIR):
        for item in os.listdir(settings.UPLOAD_DIR):
            if item.endswith(".csv"):
                os.remove(os.path.join(settings.UPLOAD_DIR, item))
