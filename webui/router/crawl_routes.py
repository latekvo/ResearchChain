from fastapi import APIRouter
from core.databases.db_crawl_tasks import (
    db_add_crawl_task,
    db_get_crawl_task,
    db_set_crawl_completed,
)
from core.databases.db_completion_tasks import db_get_incomplete_completion_tasks
from webui.models.crawl_task import CrawlCreator

router = APIRouter()


@router.get("/crawl")
def get_crawl_task():
    crawl_task = db_get_crawl_task()
    return {"crawl_task": crawl_task}


@router.post("/crawl")
def add_crawl_task(crawl_task: CrawlCreator):
    result = db_add_crawl_task(crawl_task.prompt)
    return {"result": result}


@router.put("/crawl/{uuid}")
def set_crawl_completed(uuid):
    result = db_set_crawl_completed(uuid)


@router.get("/crawl/incomplete")
def get_inocmplete_completion_task():
    result = db_get_incomplete_completion_tasks()
    return {"task": result}
