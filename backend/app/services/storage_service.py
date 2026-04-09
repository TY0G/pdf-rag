import os
import shutil
import uuid

from fastapi import UploadFile

from app.core.config import settings


class StorageService:
    def __init__(self) -> None:
        os.makedirs(settings.upload_dir, exist_ok=True)
        os.makedirs(settings.preview_dir, exist_ok=True)

    def save_upload(self, file: UploadFile) -> tuple[str, int]:
        ext = os.path.splitext(file.filename or "")[1].lower() or ".pdf"
        unique_name = f"{uuid.uuid4().hex}{ext}"
        dest_path = os.path.join(settings.upload_dir, unique_name)

        with open(dest_path, "wb") as out:
            shutil.copyfileobj(file.file, out)

        size = os.path.getsize(dest_path)
        return dest_path, size
