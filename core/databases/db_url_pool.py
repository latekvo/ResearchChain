from tinydb import TinyDB

db_name = "url_pool"
db_path = "../../store/data/{}.json".format(db_name)
db = TinyDB(db_path)

# we have to heartbeat the workers once we run out of urls
# i believe this db should remain local permanently
# instead, we should have a separate global file db for embedder to use,
# and a tiny global kv cache just to prevent duplicate urls
