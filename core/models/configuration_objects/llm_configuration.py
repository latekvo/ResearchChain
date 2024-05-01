from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from core.models.configuration_objects.utils import load_json


@dataclass
class LlmConfiguration:
    supplier: Literal["ollama", "hugging_face"]
    model_name: str
    model_token_limit: int
    model_file: str | None = None

    def __init__(self, filename: str):
        raw_config = load_json(filename)
        self.supplier = raw_config["supplier"]
        self.model_name = raw_config["model_name"]
        self.model_token_limit = raw_config["model_token_limit"]
        self.model_file = raw_config["model_file"]
