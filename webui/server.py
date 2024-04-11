from fastapi import FastAPI
from pydantic import List
from core.databases.db_completion_tasks import db_add_completion_task, db_get_completion_tasks_by_page, db_get_incomplete_completion_task


app = FastAPI()

@app.get('/task')
def get_tasks_by_page():
    result = db_get_completion_tasks_by_page()
    return {
        "tasks": result
    }

@app.get('/task/incomplete')
def get_incomplete_task():
    result = db_get_incomplete_completion_task()
    return {
        "tasks": result
    }

@app.post('/task/add')
def add_completion_task(prompt: str) -> str:
    uuid = db_add_completion_task(prompt)
    return {
        "task_uuid": uuid,
    }

