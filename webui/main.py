from __future__ import annotations
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.databases.db_crawl_tasks import db_add_crawl_task
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

@app.post("/summarize")
def add_summarize_task(req_body: RequestBody):
    uuid = db_add_completion_task(req_body.prompt, req_body.mode)
    result = db_get_completion_tasks_by_uuid(uuid)
    while result is None or result["completion_result"] is None:
        result = db_get_completion_tasks_by_uuid(uuid)
    return {
        "summary": result["completion_result"]
    }


@app.post("/crawl/add")
def add_crawl_task(req_body: RequestBody):
    new_uuid = db_add_crawl_task(req_body.prompt, req_body.mode)
    if new_uuid is None:
        raise HTTPException(status_code=500, detail="Something went wrong")
    return {"uuid": new_uuid}
