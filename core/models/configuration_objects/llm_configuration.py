from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class LlmConfiguration:
    supplier: Literal["ollama", "hugging_face"]
    model_name: str
    model_token_limit: int
    model_file: str | None = None
