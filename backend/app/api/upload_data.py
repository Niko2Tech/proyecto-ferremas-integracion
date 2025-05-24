from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from uuid import uuid4

router = APIRouter(prefix="/upload", tags=["Subidas"])

UPLOAD_DIR = "static/images"

@router.post("/imagen/")
def subir_imagen(file: UploadFile = File(...)):
    # Validaciones opcionales
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos de imagen")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid4().hex}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    url = f"/static/images/{file_name}"
    return {"imagen_url": url}
