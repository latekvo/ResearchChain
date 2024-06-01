from __future__ import annotations
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.databases.db_crawl_tasks import db_add_crawl_task
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



@app.post("/crawl/add")
def add_crawl_task(requset_body: RequestBody):
    new_uuid = db_add_crawl_task(requset_body.prompt, requset_body.mode)
    if new_uuid is None:
        raise HTTPException(status_code=500, detail="Something went wrong")
    return {"uuid": new_uuid}
