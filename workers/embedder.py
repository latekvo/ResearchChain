# embedding worker
# url_db -> THIS -> THIS.vector_db
from tinydb import Query

from core.databases import db_url_pool, defaults

PLACEHOLDER_EMBEDDER_NAME = "placeholder"

url_queue_limit = 40
url_rapid_queue = []

# important note to remember for later
# we can avoid the ... issue if we just lock the db for every transaction,
# so we lock the db, select 20 or so records, then lock them for ourselves with an update


def processing_iteration():
    url_queue_remaining_space = url_queue_limit - len(url_rapid_queue)
    if url_queue_remaining_space < url_queue_limit:
        db_url_pool.db_get_not_embedded(PLACEHOLDER_EMBEDDER_NAME)


processing_iteration()
while True:
    db_query = Query()
    db_not_embedded = db_url_pool.db_get_not_embedded(PLACEHOLDER_EMBEDDER_NAME)
    db_total = db_url_pool.db.all()

    print("urls left to be embedded:", len(db_not_embedded))
    print("url running total:", len(db_total))

    processing_iteration()
