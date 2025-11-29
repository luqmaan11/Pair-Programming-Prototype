from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from models.room import Room


@dataclass(slots=True)
class RoomState:
    code: str = ""
    cursor: int = 0


class RoomStore:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession] | None = None) -> None:
        self._session_factory = session_factory
        self._rooms: Dict[str, RoomState] = {}

    def attach_session(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create(self, room_id: str) -> RoomState:
        if not self._session_factory:
            state = RoomState()
            self._rooms[room_id] = state
            return state
        async with self._session_factory() as session:
            room = Room(id=room_id, code="", cursor=0)
            session.add(room)
            await session.commit()
            return RoomState()

    async def ensure(self, room_id: str) -> RoomState:
        if not self._session_factory:
            state = self._rooms.get(room_id)
            if state:
                return state
            state = RoomState()
            self._rooms[room_id] = state
            return state
        async with self._session_factory() as session:
            room = await session.get(Room, room_id)
            if room:
                return RoomState(code=room.code or "", cursor=room.cursor or 0)
            room = Room(id=room_id, code="", cursor=0)
            session.add(room)
            await session.commit()
            return RoomState()

    async def get(self, room_id: str) -> RoomState | None:
        if not self._session_factory:
            return self._rooms.get(room_id)
        async with self._session_factory() as session:
            room = await session.get(Room, room_id)
            if not room:
                return None
            return RoomState(code=room.code or "", cursor=room.cursor or 0)

    async def upsert(self, room_id: str, code: str, cursor: int) -> RoomState:
        if not self._session_factory:
            state = self._rooms.get(room_id) or RoomState()
            state.code = code
            state.cursor = cursor
            self._rooms[room_id] = state
            return state
        async with self._session_factory() as session:
            room = await session.get(Room, room_id)
            if not room:
                room = Room(id=room_id, code=code, cursor=cursor)
                session.add(room)
            else:
                room.code = code
                room.cursor = cursor
            await session.commit()
            await session.refresh(room)
            return RoomState(code=room.code or "", cursor=room.cursor or 0)
