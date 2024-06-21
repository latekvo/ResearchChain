import datetime
import math
import os
import random
import re
import sys
import time
import uuid

from configurator import get_runtime_config
from core.databases import defaults
from core.tools.dbops import get_vec_db_by_name
from core.tools.model_loader import load_embedder

import pika
import json


def is_text_junk(text: str):
    # checks if text contains any of junky keywords eg: privacy policy, subscribe, cookies etc.
    # do not expand this list, it has to be small to be efficient, and these words are grouped either way.
    trigger_list = [
        "sign in",
        "privacy policy",
        "skip to",
        "newsletter",
        "subscribe",
        "related tags",
        "share price",
    ]
    low_text = text.lower()
    for trigger in trigger_list:
        if trigger in low_text:
            return True
    return False


def extract_from_quote(text: str):
    if '"' in text:
        return text.split('"')[1]
    else:
        return text


def reduce(text: str, goal: str, match: str):
    if match in text:
        text = goal.join(text.split(match))
        return reduce(text, goal, match)
    return goal.join(text.split(match))


def remove_characters(text: str, wordlist: list[str], replace_with: str = "") -> str:
    for word in wordlist:
        text = "{}".format(replace_with).join(text.split(word))
    return text


def purify_name(name):
    return remove_characters(name, ["_", "+", ":", "-"], "_")


def extract_links(text: str):
    return re.findall(r"(https?://\S+\.\S+/)", text)


def gen_uuid() -> str:
    return uuid.uuid4().hex


def gen_unix_time() -> int:
    return math.floor(datetime.datetime.utcnow().timestamp())


def page_to_range(page: int, per_page: int) -> (int, int):
    start = page * per_page
    stop = start + per_page

    return start, stop


def gen_vec_db_full_name(db_name, model_name):
    return db_name + "_" + model_name


def use_faiss(db_name):
    data_path = defaults.DATA_PATH
    config = get_runtime_config()
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    embedder = load_embedder()
    model_name = config.embedder_config.model_name

    db_full_name = gen_vec_db_full_name(db_name, model_name)
    db = get_vec_db_by_name(db_full_name, embedder)

    return db, embedder


def sleep_forever():
    while True:
        time.sleep(60)


def send_update_to_api(task_uuid: str, status: str, routing_key: str, payload: str):
    connection_params = pika.ConnectionParameters(host="rabbitmq", port=5672)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.exchange_declare(exchange="status", exchange_type="direct")
    message = json.dumps({"task_uuid": task_uuid, "status": status, "payload": payload})
    channel.basic_publish(exchange="", routing_key=routing_key, body=message)
    print("status sent")
    channel.close()
    connection.close()


# deviation [0.0 -> 1.0]
def sleep_noisy(duration: int, deviation=0.10):
    rng = random.Random()
    from_duration = duration - duration * deviation
    to_duration = duration + duration * deviation
    random_coefficient = rng.uniform(from_duration, to_duration)
    time.sleep(duration * random_coefficient)


class hide_prints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
