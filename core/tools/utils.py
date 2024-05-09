import asyncio
import datetime
import multiprocessing
import re
import uuid
import os, sys

from tinydb import TinyDB

from core.databases import defaults
from core.tools.dbops import get_vec_db_by_name
from core.tools.model_loader import load_model


def purify_name(name):
    return "_".join("_".join(name.split(":")).split("-"))


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


def remove_characters(text: str, wordlist: list[str]):
    for word in wordlist:
        text = "".join(text.split(word))
    return text


def timeout_function(task, timeout=2.0):
    # FIXME: THIS FUNCTION MAY BE BROKEN, TEST THIS

    ctx = multiprocessing.get_context("spawn")
    q = ctx.Queue()

    def wrapper(q):
        task_result = task()
        q.put(task_result)

    thread_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(thread_loop)

    thread = ctx.Process(target=wrapper, args=(q,))

    thread.start()
    thread.join(timeout)  # close thread if work is finished
    if thread.is_alive():
        thread.kill()
        return None

    result = q.get()

    thread_loop.run_until_complete(asyncio.sleep(0))
    thread_loop.close()

    return result


def extract_links(text: str):
    return re.findall(r"(https?://\S+\.\S+/)", text)


def gen_uuid() -> str:
    return uuid.uuid4().hex


def gen_unix_time() -> float:
    return datetime.datetime.utcnow().timestamp()


def use_tinydb(db_name):
    data_path = defaults.DATA_PATH
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    db_path = data_path + "/{}.json".format(db_name)
    db = TinyDB(db_path)

    return db


def gen_vec_db_full_name(db_name, model_name):
    return db_name + "_" + model_name


def use_faiss(db_name, model_name):
    data_path = defaults.DATA_PATH
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    _, embedder = load_model()

    db_full_name = gen_vec_db_full_name(db_name, model_name)
    db = get_vec_db_by_name(db_full_name, embedder)

    return db


class hide_prints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
