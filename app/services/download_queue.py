# app/services/download_queue.py
from enum import Enum
import asyncio

class Status(str, Enum):
    PENDING = "pendente"
    IN_PROGRESS = "em andamento"
    COMPLETED = "concluído"
    FAILED = "falhou"

class DownloadQueue:
    def __init__(self):
        self.queue = []
        self.lock = asyncio.Lock()

    async def add(self, url: str, type_: str):
        """
        Adiciona item à fila de downloads.
        """
        item = {
            "url": url,
            "type": type_,
            "status": Status.PENDING,
            "result": None
        }
        async with self.lock:
            self.queue.append(item)
        return item

    async def set_status(self, item, status: Status, result=None):
        """
        Atualiza status do item e armazena resultado ou erro.
        """
        async with self.lock:
            item["status"] = status
            if result:
                item["result"] = result

    async def get_all(self):
        """
        Retorna toda a fila com status atualizado.
        """
        async with self.lock:
            # retorna cópia da fila para evitar problemas de concorrência
            return [dict(i) for i in self.queue]

# Instância global
download_queue = DownloadQueue()
