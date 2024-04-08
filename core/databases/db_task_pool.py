from tinydb import TinyDB

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
            "timestamp": timestamp,
        }
    )

    return new_uuid
