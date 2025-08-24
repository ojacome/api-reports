from typing import Dict, Set
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self) -> None:
        self._by_number: Dict[str, Set[WebSocket]] = {}

    async def register(self, phone_number: str, ws: WebSocket) -> None:
        self._by_number.setdefault(phone_number, set()).add(ws)

    def unregister(self, phone_number: str, ws: WebSocket) -> None:
        conns = self._by_number.get(phone_number)
        if not conns:
            return
        conns.discard(ws)
        if not conns:
            self._by_number.pop(phone_number, None)

    async def broadcast(self, phone_number: str, payload: dict) -> None:
        for ws in list(self._by_number.get(phone_number, set())):
            try:
                await ws.send_json(payload)
            except Exception:
                # si falla, lo sacamos silenciosamente
                self.unregister(phone_number, ws)

manager = ConnectionManager()
