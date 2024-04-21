from __future__ import annotations

from pydantic import BaseModel


class UrlCreator(BaseModel):
    url: str
    prompt: str
    parent_uuid: str | None = None


class Embedded(BaseModel):
    url_id: str
    embedding_model: str


class Downloaded(BaseModel):
    url_id: str
    text: str
