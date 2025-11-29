from __future__ import annotations

from fastapi import APIRouter

from schemas import AutocompleteRequest, AutocompleteResponse
from services.autocomplete import AutocompleteService

router = APIRouter(prefix="/autocomplete", tags=["autocomplete"])


def init_router(service: AutocompleteService) -> APIRouter:
    @router.post("", response_model=AutocompleteResponse)
    def autocomplete(payload: AutocompleteRequest) -> AutocompleteResponse:
        return AutocompleteResponse(suggestion=service.suggest(payload.code))

    return router
