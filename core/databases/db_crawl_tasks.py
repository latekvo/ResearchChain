from tinydb import TinyDB, Query

from core.tools import utils

db_name = "crawl_tasks"
db_path = "../../store/data/{}.json".format(db_name)
db = TinyDB(db_path)

# we have to heartbeat our workers once we run out of tasks, websocks should suffice


def db_add_crawl_task(prompt):
    new_uuid = utils.gen_uuid()
    timestamp = utils.gen_unix_time()

    db.insert(
        {
            "uuid": new_uuid,
            "prompt": prompt,
            "completed": False,
            "executing": False,
            "completion_date": 0,  # time completed
            "execution_date": 0,  # time started completion
            "timestamp": timestamp,  # time added
        }
    )

    return new_uuid


def db_set_crawl_completed(uuid: str):
    fields = Query()
    db.update({"completed": True}, fields.uuid == uuid)


def db_get_crawl_task():
    fields = Query()
    crawl_task = db.get(fields.completed is False)

    return crawl_task


def db_get_incomplete_completion_task():
    fields = Query()
    task = db.get(fields.completed is False and fields.executing is False)

    task_uuid = task
    db.update({"executing": True}, fields.uuid == task_uuid)

    return task
