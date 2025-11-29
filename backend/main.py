from __future__ import annotations

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import autocomplete as autocomplete_router
from routers import rooms as rooms_router
from services.autocomplete import AutocompleteService
from services.room_state import RoomStore
from services.collaboration import CollaborationHub
from services.database import init_db, shutdown_db

load_dotenv()

app = FastAPI(title="Pair Programming Prototype")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
store = RoomStore()
autocomplete_service = AutocompleteService()
router_rooms = rooms_router.init_router(store)
router_autocomplete = autocomplete_router.init_router(autocomplete_service)
app.include_router(router_rooms)
app.include_router(router_autocomplete)
hub = CollaborationHub(store)


@app.on_event("startup")
async def on_startup() -> None:
    session_factory = await init_db()
    if session_factory:
        store.attach_session(session_factory)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await shutdown_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.websocket("/ws/{room_id}")
async def websocket_room(room_id: str, socket: WebSocket) -> None:
    await hub.connect(room_id, socket)
    try:
        while True:
            payload = await socket.receive_json()
            code = str(payload.get("code", ""))
            cursor = int(payload.get("cursor", 0))
            state = await store.upsert(room_id, code, cursor)
            message = {"code": state.code, "cursor": state.cursor}
            await hub.broadcast(room_id, message, source=socket)
    except WebSocketDisconnect:
        hub.disconnect(room_id, socket)
