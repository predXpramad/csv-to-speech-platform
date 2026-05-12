import os

class Settings:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    STORAGE_DIR = os.path.join(BASE_DIR, "storage")
    UPLOAD_DIR = os.path.join(STORAGE_DIR, "uploads")
    TEMP_AUDIO_DIR = os.path.join(STORAGE_DIR, "temp_audio")
    ZIP_EXPORTS_DIR = os.path.join(STORAGE_DIR, "zip_exports")
    METADATA_DIR = os.path.join(STORAGE_DIR, "metadata")
    ZIP_EXPIRATION_HOURS = 72

settings = Settings()
