from pydantic import BaseModel


class CompletionTask(BaseModel):
    uuid: str
    prompt: str
    completed: bool
    timestamp: float


class TaskCreator(BaseModel):
    prompt: str
    mode: str


# TaskCreator will is more generic
