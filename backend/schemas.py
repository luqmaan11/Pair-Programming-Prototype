from __future__ import annotations

from pydantic import BaseModel, Field


class RoomCreateResponse(BaseModel):
    roomId: str = Field(..., description="Public room identifier")


class AutocompleteRequest(BaseModel):
    code: str
    cursorPosition: int
    language: str


class AutocompleteResponse(BaseModel):
    suggestion: str
