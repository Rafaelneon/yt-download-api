from fastapi import APIRouter
from app.services.file_service import FileService

router = APIRouter()
fs = FileService()

@router.get("/recent")
async def recent_downloads(limit: int = 10):
    return {"recent_files": fs.list_recent(limit=limit)}
