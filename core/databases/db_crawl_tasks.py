from tinydb import Query

from core.tools import utils
from core.tools.utils import use_tinydb, gen_unix_time

db = use_tinydb("crawl_tasks")

# we have to heartbeat our workers once we run out of tasks, websocks should suffice


def db_add_crawl_task(prompt):
    new_uuid = utils.gen_uuid()
    timestamp = utils.gen_unix_time()

    db.insert(
        {
            "uuid": new_uuid,
            "prompt": prompt,
            "type": None,  # todo: choose 'news', 'wiki', 'docs', use WebQuery
            "completed": False,
            "executing": False,
            "completion_date": 0,  # time completed
            "execution_date": 0,  # time started completion
            "timestamp": timestamp,  # time added
        }
    )

    return new_uuid


def db_set_crawl_executing(uuid: str):
    fields = Query()
    db.update(
        {"executing": True, "execution_date": gen_unix_time()}, fields.uuid == uuid
    )


def db_set_crawl_completed(uuid: str):
    fields = Query()
    db.update(
        {"completed": True, "completion_date": gen_unix_time()}, fields.uuid == uuid
    )


def db_get_crawl_task():
    fields = Query()
    crawl_task = db.get(fields.completed == False)

    if crawl_task is not None:
        db_set_crawl_executing(crawl_task.uuid)

    return crawl_task


def db_get_incomplete_completion_task():
    fields = Query()
    task = db.get(fields.completed == False and fields.executing == False)
    db.update({"executing": True}, fields.uuid == task.uuid)

    return task
