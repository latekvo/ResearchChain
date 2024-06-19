from __future__ import annotations
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.databases.db_crawl_tasks import db_add_crawl_task, db_get_crawl_tasks_by_page
from core.databases.db_completion_tasks import (
    db_add_completion_task,
    db_get_completion_tasks_by_page,
)
from pydantic import BaseModel
import pika
import threading
import json
import asyncio
import functools

from typing import Literal


class RequestBody(BaseModel):
    prompt: str
    mode: Literal["wiki", "docs", "news"]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
def get_crawl_tasks(page: int = 0):
    crawl_tasks = db_get_crawl_tasks_by_page(page)
    return {"tasks": crawl_tasks}


@app.post("/completion")
def add_completion_task(req_body: RequestBody):
    new_uuid = db_add_completion_task(req_body.prompt, req_body.mode)
    if new_uuid is None:
        raise HTTPException(status_code=500, detail="Something went wrong")
    return {"uuid": new_uuid}


@app.get("/completion")
def get_completion_tasks(page: int = 0):
    completion_tasks = db_get_completion_tasks_by_page(page)
    return {"tasks": completion_tasks}


active_connections = {}


@app.websocket("/ws")
async def on_connection(websocket: WebSocket):
    await websocket.accept()
    active_connections[websocket] = []
    print(active_connections)
    try:
        while True:
            try:
                data = await websocket.receive_text()
                data_dict = json.loads(data)
                if isinstance(data_dict["message"], list):
                    active_connections[websocket].extend(data_dict["message"])
                else:
                    active_connections[websocket].append(data_dict["message"])
                print(active_connections)
            except WebSocketDisconnect:
                break
    finally:
        if websocket in active_connections:
            del active_connections[websocket]


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
            try:
                await websocket.send_text("current status: " + status)
            except WebSocketDisconnect:
                del active_connections[websocket]


def consumer():
    connection_params = pika.ConnectionParameters(host="rabbitmq", port=5672)
    connection = pika.BlockingConnection(connection_params)
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
