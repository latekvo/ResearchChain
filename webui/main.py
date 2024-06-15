from __future__ import annotations
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from core.databases.db_completion_tasks import (
    db_add_completion_task,
    db_get_completion_tasks_by_page,
    db_get_incomplete_completion_tasks,
)
from core.databases.db_crawl_tasks import (
    db_add_crawl_task,
    db_get_crawl_task,
    db_set_crawl_completed,
)
from core.databases.db_url_pool import (
    db_add_url,
    db_get_not_downloaded,
    db_get_not_embedded,
    db_is_url_present,
    db_set_url_downloaded,
    db_set_url_embedded,
    db_set_url_rubbish,
)
from pydantic import BaseModel
import pika
import threading
import json
import asyncio
import functools


class TaskCreator(BaseModel):
    prompt: str
    mode: str


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


class UrlCreator(BaseModel):
    url: str
    prompt: str
    parent_uuid: str = None


class Embedded(BaseModel):
    url_id: str
    embedding_model: str


class Downloaded(BaseModel):
    url_id: str
    text: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/task")
def get_tasks_by_page():
    result = db_get_completion_tasks_by_page(0)
    return {"tasks": result}


@app.get("/task/incomplete")
def get_incomplete_task():
    result = db_get_incomplete_completion_tasks()
    return {"tasks": result}


@app.post("/task")
def add_completion_task(completion_task: TaskCreator):
    uuid = db_add_completion_task(completion_task.prompt, completion_task.mode)
    return {"uuid": uuid}


@app.get("/crawl")
def get_crawl_task():
    crawl_task = db_get_crawl_task()
    return {"crawl_task": crawl_task}


@app.post("/crawl")
def add_crawl_task(crawl_task: CrawlCreator):
    result = db_add_crawl_task(crawl_task.prompt)
    return {"result": result}


@app.put("/crawl/{uuid}")
def set_crawl_completed(uuid):
    result = db_set_crawl_completed(uuid)


@app.get("/crawl/incomplete")
def get_incomplete_completion_task():
    result = db_get_incomplete_completion_tasks()
    return {"task": result}


@app.post("/url")
def add_url(url: UrlCreator):
    uuid, result = db_add_url(url.url, url.prompt, url.parent_uuid)
    return {"uuid": uuid, "url_object": result}


@app.get("/url/downloaded")
def get_not_downloaded():
    result = db_get_not_downloaded()
    return {"result": result}


@app.get("/url/embedded")
def get_not_embedded(model: str = None):
    result = db_get_not_embedded(model)
    return {"result": result}


@app.get("/url/present")
def get_present_urls(url: str = None):
    result = db_is_url_present(url)
    return {"url": result}


@app.put("/url/embedded")
def set_embedded_url(body: Embedded):
    db_set_url_embedded(body.url_id, body.embeddeding_model)


@app.put("/url/downloaded")
def set_downloaded_url(body: Downloaded):
    db_set_url_downloaded(body.url_id, body.text)


@app.put("/url/rubbish/{url_id}")
def set_url_rubbish(url_id: str):
    db_set_url_rubbish(url_id)


active_connections = {}


@app.websocket("/ws")
async def on_connection(websocket: WebSocket):
    await websocket.accept()
    active_connections[websocket] = []
    print(active_connections)
    while True:
        data = await websocket.receive_text()
        data_dict = json.loads(data)
        active_connections[websocket].append(data_dict["message"])
        print(active_connections)


def sync(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(f(*args, **kwargs))

    return wrapper


@sync
async def callback(ch, method, properties, body):
    data = json.loads(body)
    print("getting data from: ", data)
    uuid = data["task_uuid"]
    status = data["status"]
    for websocket, uuid_list in active_connections.items():
        if uuid in uuid_list:
            await websocket.send_text("current status: " + status)


def consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="status", exchange_type="direct")

    channel.queue_declare(queue="update_status", durable=True)

    channel.queue_bind(
        exchange="status", queue="update_status", routing_key="update_status"
    )

    channel.basic_consume(
        queue="update_status", on_message_callback=callback, auto_ack=True
    )

    channel.start_consuming()


consumer_thread = threading.Thread(target=consumer)
consumer_thread.start()
