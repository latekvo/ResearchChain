from pydantic import BaseModel
from datetime import date

class CompletionTask(BaseModel):
    uuid: str
    prompt: str
    completed: bool
    timestamp: date

class TaskCreator(BaseModel):
    prompt: str

#the TaskCreator class is going to be more generic class 