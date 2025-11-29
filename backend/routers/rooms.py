from __future__ import annotations

from fastapi import APIRouter
from uuid import uuid4

from schemas import RoomCreateResponse
from services.room_state import RoomStore

router = APIRouter(prefix="/rooms", tags=["rooms"])


def init_router(store: RoomStore) -> APIRouter:
    @router.post("", response_model=RoomCreateResponse)
    async def create_room() -> RoomCreateResponse:
        room_id = uuid4().hex[:8]
        await store.create(room_id)
        return RoomCreateResponse(roomId=room_id)

    return router
