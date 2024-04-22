from pydantic import BaseModel


class CrawlCreator(BaseModel):
    prompt: str


class CrawlTask(BaseModel):
    uuid: str
    prompt: str
    completed: bool
    executing: bool
    completion_date: float
    execution_date: float
    timestamp: float
