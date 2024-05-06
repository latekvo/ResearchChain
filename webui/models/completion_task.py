from pydantic import BaseModel


class TaskCreator(BaseModel):
    prompt: str
    mode: str
