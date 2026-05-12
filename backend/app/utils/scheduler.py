import os
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
