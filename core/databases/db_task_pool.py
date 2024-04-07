from tinydb import TinyDB

db_name = "task_pool"
db_path = "../../store/data/{}.json".format(db_name)
db = TinyDB(db_path)

# we have to heartbeat our workers once we run out of tasks, websocks should suffice
