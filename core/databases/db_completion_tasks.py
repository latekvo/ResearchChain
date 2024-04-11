import os

from tinydb import TinyDB, Query

from core.databases import defaults
from core.tools import utils

data_path = "../../store/data/"
if not os.path.exists(data_path):
    os.makedirs(data_path)

db_name = "completion_tasks"
db_path = "../../store/data/{}.json".format(db_name)
db = TinyDB(db_path)


def db_add_completion_task(prompt):
    new_uuid = utils.gen_uuid()
    timestamp = utils.gen_unix_time()

    db.insert(
        {
            "uuid": new_uuid,
            "prompt": prompt,
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

    results = db.get(fields.completed is False)

    return results


"""
def db_add_smart_completion_task(prompt):
    # todo: this functions should automatically check completed crawls 
    #       to see if it's necessary to perform a crawl before doing a summary
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
