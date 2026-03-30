from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ExtractRequest(BaseModel):
    text: str
    save_note: Optional[bool] = False


class ActionItemOut(BaseModel):
    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: datetime


class ExtractResponse(BaseModel):
    note_id: Optional[int]
    items: List[ActionItemOut]


class MarkDoneRequest(BaseModel):
    done: Optional[bool] = True