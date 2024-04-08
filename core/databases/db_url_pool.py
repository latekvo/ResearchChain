from tinydb import TinyDB

from core.tools import utils

db_name = "url_pool"
db_path = "../../store/data/{}.json".format(db_name)
db = TinyDB(db_path)

# we have to heartbeat the workers once we run out of urls
# i believe this db should remain local permanently
# instead, we should have a separate global file db for embedder to use,
# and a tiny global kv cache just to prevent duplicate urls


def db_add_url(url, prompt, parent_uuid=None):
    new_uuid = utils.gen_uuid()
    timestamp = utils.gen_unix_time()

    db.insert(
        {
            "uuid": new_uuid,
            "parent_uuid": parent_uuid,
            "prompt": prompt,
            "url": url,
            "is_downloaded": False,
            "is_rubbish": False,
            "embedded_by": [],
            "timestamp": timestamp,
        }
    )

    return new_uuid
