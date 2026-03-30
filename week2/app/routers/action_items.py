from __future__ import annotations

from typing import List, Optional
from ..services.extract import extract_action_items_llm
from fastapi import APIRouter, HTTPException

from .. import db
from ..services.extract import extract_action_items
from ..schemas import (
    ExtractRequest,
    ExtractResponse,
    ActionItemOut,
    MarkDoneRequest,
)

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="text is required")

    try:
        note_id: Optional[int] = None

        if payload.save_note:
            note_id = db.insert_note(payload.text)

        items = extract_action_items(payload.text)
        ids = db.insert_action_items(items, note_id=note_id)

        result_items = [
            ActionItemOut(
                id=i,
                note_id=note_id,
                text=t,
                done=False,
                created_at=None,  # adjust if DB returns timestamp
            )
            for i, t in zip(ids, items)
        ]

        return ExtractResponse(note_id=note_id, items=result_items)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[ActionItemOut])
def list_all(note_id: Optional[int] = None):
    try:
        rows = db.list_action_items(note_id=note_id)

        return [
            ActionItemOut(
                id=r["id"],
                note_id=r["note_id"],
                text=r["text"],
                done=bool(r["done"]),
                created_at=r["created_at"],
            )
            for r in rows
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{action_item_id}/done")
def mark_done(action_item_id: int, payload: MarkDoneRequest):
    try:
        db.mark_action_item_done(action_item_id, payload.done)
        return {"id": action_item_id, "done": payload.done}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(payload: ExtractRequest) -> ExtractResponse:
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="text is required")

    try:
        note_id: Optional[int] = None

        if payload.save_note:
            note_id = db.insert_note(payload.text)

        items = extract_action_items_llm(payload.text)
        ids = db.insert_action_items(items, note_id=note_id)

        result_items = [
            ActionItemOut(
                id=i,
                note_id=note_id,
                text=t,
                done=False,
                created_at=None,
            )
            for i, t in zip(ids, items)
        ]

        return ExtractResponse(note_id=note_id, items=result_items)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/notes")
def list_notes():
    try:
        rows = db.list_notes()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))