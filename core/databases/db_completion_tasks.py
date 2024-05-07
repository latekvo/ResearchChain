from tinydb import Query

from core.databases import defaults
from core.tools import utils
from core.tools.utils import use_tinydb, gen_unix_time

db = use_tinydb("completion_tasks")


def db_add_completion_task(prompt, mode):
    new_uuid = utils.gen_uuid()
    timestamp = utils.gen_unix_time()

    db.insert(
        {
            "uuid": new_uuid,
            "prompt": prompt,
            "mode": mode,
            "completed": False,
            "completion_result": None,
            "executing": False,
            "completion_date": 0,
            "execution_date": 0,
            "timestamp": timestamp,
        }
    )

    return new_uuid


def db_get_completion_tasks_by_page(page: int, per_page: int = defaults.ITEMS_PER_PAGE):

    # returns all as TinyDB does not support pagination
    # we'll be moving to SQLite or Cassandra soon enough
    results = db.all()

    return results


def db_set_incomplete_completion_task_executing(uuid: str):
    fields = Query()
    db.update(
        {"executing": True, "execution_date": gen_unix_time()}, fields.uuid == uuid
    )


def db_get_incomplete_completion_task():
    fields = Query()

    results = db.get(fields.completed == False and fields.executing == False)
    if results is not None:
        db_set_incomplete_completion_task_executing(results["uuid"])

    return results


def db_update_completion_task_after_summarizing(summary: str, uuid: str):
    fields = Query()
    db.update({"completed": True, "completion_result": summary, "completion_date": gen_unix_time()}, fields.uuid == uuid)


"""
def db_add_smart_completion_task(prompt):
    # todo: this functions should automatically dispatch crawl tasks if they are needed 
    new_uuid = utils.gen_uuid()
    timestamp = utils.gen_unix_time()

    db.insert(
        {
            "uuid": new_uuid,
            "prompt": prompt,
            "complete": False,
            "timestamp": timestamp,
        }
    )

    return new_uuid
"""
