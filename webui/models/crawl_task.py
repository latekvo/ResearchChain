from pydantic import BaseModel 
from datetime import date

class CrawlTask(BaseModel):
    uuid: str
    prompt: str
    completed: bool
    executing: bool
    completion_date: float
    execution_date: float
    timestamp: date


