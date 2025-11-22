import os
import shutil
from pathlib import Path
from app.config import DOWNLOADS_PATH, MUSIC_DIR, VIDEO_DIR

class FileService:
    def __init__(self):
        # Cria pastas se não existirem
        for folder in [DOWNLOADS_PATH, MUSIC_DIR, VIDEO_DIR]:
            Path(folder).mkdir(parents=True, exist_ok=True)

    def list_recent(self, limit=10):
        files = []
        for root, _, filenames in os.walk(DOWNLOADS_PATH):
            for f in filenames:
                path = Path(root) / f
                files.append({"name": f, "path": str(path), "timestamp": path.stat().st_mtime})
        files.sort(key=lambda x: x["timestamp"], reverse=True)
        return files[:limit]

    def move_file(self, src_path: str, target: str):
        src = Path(src_path)
        if not src.exists():
            return {"error": "Arquivo não encontrado"}

        if target == "music":
            dest = Path(MUSIC_DIR) / src.name
        elif target == "video":
            dest = Path(VIDEO_DIR) / src.name
        else:
            return {"error": "Destino inválido"}

        shutil.move(str(src), str(dest))
        return {"from": str(src), "to": str(dest)}
