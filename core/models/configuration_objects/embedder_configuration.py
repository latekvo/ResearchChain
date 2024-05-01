from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from core.models.configuration_objects.utils import load_json


@dataclass
class EmbedderConfiguration:
    supplier: Literal["ollama", "hugging_face"]
    model_name: str
    model_token_limit: int
    article_limit: int
    buffer_stops: list[str]
    chunk_overlap: int
    model_file: str | None = None

    def __init__(self, filename: str):
        raw_config = load_json(filename)
        self.supplier = raw_config["supplier"]
        self.model_name = raw_config["model_name"]
        self.model_token_limit = raw_config["model_token_limit"]
        self.article_limit = raw_config["article_limit"]
        self.buffer_stops = raw_config["buffer_stops"]
        self.chunk_overlap = raw_config["chunk_overlap"]
        self.model_file = raw_config.get("model_file")
