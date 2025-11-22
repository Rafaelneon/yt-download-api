# app/services/ai_manager.py
import os
import shutil
from app.config import DOWNLOADS_PATH

class AIManager:
    def __init__(self):
        self.download_dir = DOWNLOADS_PATH
        self.video_dir = os.path.join(DOWNLOADS_PATH, "video")
        self.music_dir = os.path.join(DOWNLOADS_PATH, "music")

        os.makedirs(self.video_dir, exist_ok=True)
        os.makedirs(self.music_dir, exist_ok=True)

    async def organize_file(self, filepath: str):
        ext = filepath.lower().split(".")[-1]

        if ext in ["mp4", "mkv", "mov"]:
            shutil.move(filepath, os.path.join(self.video_dir, os.path.basename(filepath)))
        elif ext in ["mp3", "wav", "flac"]:
            shutil.move(filepath, os.path.join(self.music_dir, os.path.basename(filepath)))

# instância global
ai_manager = AIManager()
