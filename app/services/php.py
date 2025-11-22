# app/services/http_service.py
import httpx

class HTTPService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get(self, path: str, params: dict = None):
        resp = await self.client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    async def post(self, path: str, data: dict = None):
        resp = await self.client.post(path, json=data)
        resp.raise_for_status()
        return resp.json()

http_service = HTTPService("http://localhost:8000")
