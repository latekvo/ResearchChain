from pydantic import BaseModel
from typing import Optional

class UrlCreator(BaseModel):
    url: str
    prompt: str
    parent_uuid: Optional[str] = None

class Embedded(BaseModel):
    url_id: str
    embeddeding_model: str

class Downloaded(BaseModel): 
    url_id: str
    text: str