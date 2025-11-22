# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # carrega variáveis do .env

# Caminho base de downloads
DOWNLOADS_PATH = os.getenv("DOWNLOADS_PATH")
VIDEO_DIR = os.path.join(DOWNLOADS_PATH, "video")
MUSIC_DIR = os.path.join(DOWNLOADS_PATH, "music")

# Cria pastas se não existirem
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

# Ambiente da aplicação
ENV = os.getenv("ENV", "development")  # default é 'development'
