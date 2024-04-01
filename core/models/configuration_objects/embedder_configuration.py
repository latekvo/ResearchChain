from dataclasses import dataclass
from typing import Literal, Optional
@dataclass
class EmbedderConfiguration:
    supplier: Literal['ollama', 'hugging_face']
    model_name: str
    model_token_limit: int
    model_file: Optional[str] = None
    article_limit: int
    buffer_stops: list
    chunk_overlap: int
