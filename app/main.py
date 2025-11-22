from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import youtube, status, ai

app = FastAPI(
    title="RafaelNeon API",
    description="API de download e organização automática via IA",
    version="2.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["0.0.0.0","127.0.0.1","192.168.15.10"],  # você pode restringir depois
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Routers
app.include_router(youtube.router, prefix="/youtube", tags=["YouTube"])
app.include_router(ai.router, prefix="/ai", tags=["AI"])
app.include_router(status.router, prefix="/status", tags=["Status"])

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Rota raiz -> dashboard
@app.get("/")
async def root():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/index.html")
