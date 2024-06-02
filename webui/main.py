from __future__ import annotations
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.databases.db_crawl_tasks import db_add_crawl_task, db_get_all_crawl_tasks
from core.databases.db_completion_tasks import db_add_completion_task, db_get_completion_tasks_by_uuid
from pydantic import BaseModel
from typing import Literal

class RequestBody(BaseModel):
    prompt: str
    mode: Literal["wiki", "docs", "news"]

app = FastAPI()
app.add_middleware = CORSMiddleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/crawl")
def add_crawl_task(req_body: RequestBody):
    new_uuid = db_add_crawl_task(req_body.prompt, req_body.mode)
    if new_uuid is None:
        raise HTTPException(status_code=500, detail="Something went wrong")
    return {"uuid": new_uuid}


@app.get("/crawl")
def get_crawl_tasks():
    tasks = db_get_all_crawl_tasks()
    return { "tasks": tasks }