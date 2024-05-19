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
            "required_crawl_tasks": [],  # uuid list that has to be completed first
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


def db_set_completion_task_executing(uuid: str):
    fields = Query()
    db.update(
        {"executing": True, "execution_date": gen_unix_time()}, fields.uuid == uuid
    )


def db_get_incomplete_completion_tasks(amount: int = 1):
    fields = Query()

    results = db.search(fields.completed == False and fields.executing == False)
    results = results[:amount]

    for task in results:
        db_set_completion_task_executing(task["uuid"])

    return results


def db_release_executing_tasks(uuid_list: list[str]):
    fields = Query()
    db.update({"executing": False}, fields.uuid in uuid_list)


def db_update_completion_task_after_summarizing(summary: str, uuid: str):
    fields = Query()
    db.update(
        {
            "completed": True,
            "completion_result": summary,
            "completion_date": gen_unix_time(),
        },
        fields.uuid == uuid,
    )
