from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

PHP_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "php")

@router.get("/")
async def serve_index():
    file_path = os.path.join(PHP_PATH, "index.html")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Página não encontrada")
    return FileResponse(file_path)
