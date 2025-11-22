# app/services/yt_service.py
import os
from pytubefix import YouTube
from app.config import DOWNLOADS_PATH

class YTService:
    def __init__(self):
        self.videos_dir = os.path.join(DOWNLOADS_PATH, "video")
        self.musics_dir = os.path.join(DOWNLOADS_PATH, "music")
        os.makedirs(self.videos_dir, exist_ok=True)
        os.makedirs(self.musics_dir, exist_ok=True)

    async def download_video(self, url: str):
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()

            if not stream:
                raise ValueError("Nenhuma stream de vídeo disponível")

            out_file = stream.download(output_path=self.videos_dir)

            return {
                "type": "video",
                "title": yt.title,
                "filename": os.path.basename(out_file),
                "path": out_file
            }

        except Exception as e:
            return {
                "type": "video",
                "title": None,
                "filename": None,
                "path": None,
                "error": str(e)
            }

    async def download_music(self, url: str):
        try:
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()

            if not stream:
                raise ValueError("Nenhuma stream de áudio disponível")

            out_file = stream.download(output_path=self.musics_dir)

            base, _ = os.path.splitext(out_file)
            mp3_file = base + ".mp3"

            if os.path.exists(mp3_file):
                os.remove(mp3_file)

            os.rename(out_file, mp3_file)

            return {
                "type": "music",
                "title": yt.title,
                "filename": os.path.basename(mp3_file),
                "path": mp3_file
            }

        except Exception as e:
            return {
                "type": "music",
                "title": None,
                "filename": None,
                "path": None,
                "error": str(e)
            }

# Instância global
yt_service = YTService()
