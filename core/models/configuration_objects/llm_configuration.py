from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class LlmConfiguration:
    supplier: Literal['ollama', 'hugging_face']
    model_name: str
    model_token_limit: int
    model_file: Optional[str] = None
