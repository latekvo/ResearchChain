from tinydb import TinyDB

db_name = "crawl_history"
db_path = "../../store/data/{}.json".format(db_name)
db = TinyDB(db_path)

# this db is completely optional, only used by the UI, and so it's development can be delayed
