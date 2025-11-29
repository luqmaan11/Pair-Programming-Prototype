from __future__ import annotations

from typing import Dict, Set

from fastapi import WebSocket, WebSocketDisconnect

from services.room_state import RoomStore


class CollaborationHub:
    def __init__(self, store: RoomStore) -> None:
        self.store = store
        self.connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, room_id: str, socket: WebSocket) -> None:
        await socket.accept()
        await self.store.ensure(room_id)
        sockets = self.connections.setdefault(room_id, set())
        sockets.add(socket)
        snapshot = await self.store.get(room_id)
        if snapshot:
            await socket.send_json({"code": snapshot.code, "cursor": snapshot.cursor})

    def disconnect(self, room_id: str, socket: WebSocket) -> None:
        sockets = self.connections.get(room_id)
        if not sockets:
            return
        sockets.discard(socket)
        if not sockets:
            self.connections.pop(room_id, None)

    async def broadcast(self, room_id: str, payload: dict, source: WebSocket | None = None) -> None:
        sockets = list(self.connections.get(room_id, set()))
        for socket in sockets:
            if socket == source:
                continue
            try:
                await socket.send_json(payload)
            except WebSocketDisconnect:
                self.disconnect(room_id, socket)
