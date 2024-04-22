from tinydb import Query

from core.databases import defaults
from core.tools import utils
from core.tools.utils import use_tinydb

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
            "timestamp": timestamp,
        }
    )

    return new_uuid


def db_get_completion_tasks_by_page(page: int, per_page: int = defaults.ITEMS_PER_PAGE):

    # returns all as TinyDB does not support pagination
    # we'll be moving to SQLite or Cassandra soon enough
    results = db.all()

    return results


def db_get_incomplete_completion_task():
    fields = Query()

    results = db.get(fields.completed == False)

    return results


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
