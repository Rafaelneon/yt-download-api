from fastapi import APIRouter
from app.services.ai_manager import AIManager

router = APIRouter()
ai_manager = AIManager()

@router.post("/organize")
async def organize_downloads():
    result = await ai_manager.organize_downloads()
    return result
