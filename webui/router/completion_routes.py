from fastapi import APIRouter
from core.databases.db_completion_tasks import db_add_completion_task, db_get_completion_tasks_by_page, db_get_incomplete_completion_task
from webui.models.completion_task import TaskCreator

router = APIRouter()


@router.get('/task')
def get_tasks_by_page():
    result = db_get_completion_tasks_by_page()
    return {
        "tasks": result
    }


@router.get('/task/incomplete')
def get_incomplete_task():
    result = db_get_incomplete_completion_task()
    return {
        "tasks": result
    }


@router.post('/task')
def add_completion_task(completion_task: TaskCreator):
    uuid = db_add_completion_task(completion_task.prompt, completion_task.mode)
    return {
        "task_uuid": uuid,
    }
