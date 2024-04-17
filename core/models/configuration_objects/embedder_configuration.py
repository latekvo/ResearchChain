from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class EmbedderConfiguration:
    supplier: Literal["ollama", "hugging_face"]
    model_name: str
    model_token_limit: int
    article_limit: int
    buffer_stops: list[str]
    chunk_overlap: int
    model_file: str | None = None
