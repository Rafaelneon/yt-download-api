from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.yt_service import YTService
from app.services.download_queue import download_queue, Status

router = APIRouter()

# instância global correta
yt_service = YTService()

async def process_download(item):
    await download_queue.set_status(item, Status.IN_PROGRESS)

    if item["type"] == "video":
        result = await yt_service.download_video(item["url"])

    elif item["type"] == "music":
        result = await yt_service.download_music(item["url"])

    else:
        result = {"error": "Tipo inválido"}
        await download_queue.set_status(item, Status.FAILED, result)
        return

    if "error" in result:
        await download_queue.set_status(item, Status.FAILED, result)
    else:
        await download_queue.set_status(item, Status.COMPLETED, result)

@router.post("/download")
async def add_download(url: str, type_: str, background_tasks: BackgroundTasks):
    item = await download_queue.add(url, type_)
    background_tasks.add_task(process_download, item)
    return {"message": "Download adicionado à fila", "url": url, "type": type_}

@router.get("/queue")
async def get_queue():
    return await download_queue.get_all()

@router.get("/status")
async def get_status(url: str):
    items = await download_queue.get_all()
    for i in items:
        if i.get("url") == url:
            return i
    raise HTTPException(status_code=404, detail="URL não encontrada na fila")
