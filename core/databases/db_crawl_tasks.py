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
            "base_amount_scheduled": 100,  # todo: replace with dynamically adjusted value
            "embedding_progression": {},  # {model_name: count} | progress tracking
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


def db_get_incomplete_crawl_task():
    fields = Query()
    task = db.get(fields.completed == False and fields.executing == False)
    db.update({"executing": True}, fields.uuid == task.uuid)

    return task


def db_is_crawl_task_fully_embedded(uuid: str, model_name: str):
    fields = Query()
    task = db.get(fields.uuid == uuid)

    baseline_count = task.base_amount_scheduled
    current_count = task.embedding_progression[model_name]

    return current_count >= baseline_count


def db_increment_task_embedding_progression(uuid: str, model_name: str):
    fields = Query()
    task = db.get(fields.uuid == uuid)

    current_progression = task.embedding_progression
    current_count = current_progression[model_name]

    if current_count is not None:
        current_count += 1
    else:
        current_count = 1

    current_progression[model_name] = current_count

    db.update({"embedding_progression": current_progression}, fields.uuid == task.uuid)
