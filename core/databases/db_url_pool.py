from tinydb import TinyDB, Query

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

    new_url_object = {
        "uuid": new_uuid,
        "parent_uuid": parent_uuid,
        "prompt": prompt,
        "url": url,
        "is_downloaded": False,
        "is_rubbish": False,
        "embedded_by": [],
        "timestamp": timestamp,
    }

    db.insert(new_url_object)

    return new_url_object


def db_get_not_downloaded() -> list:
    db_query = Query()
    db_results = db.search(
        db_query.fragment({"is_downloaded": False, "is_rubbish": False})
    )

    return db_results


def db_get_not_embedded(model: str) -> list:
    fields = Query()
    db_results = db.search(fields.embedded_by.contains(model) is not True)

    return db_results


def db_set_url_embedded(url_id: str, embedding_model: str):
    query = Query()
    record = db.get(query.uuid == url_id)
    if record is None:
        return

    embedded_by = record["embedded_by"]
    embedded_by.append(embedding_model)

    db.update({"embedded_by": embedded_by}, query.uuid == url_id)


def db_set_url_downloaded(url_id: str):
    query = Query()
    record = db.get(query.uuid == url_id)
    if record is None:
        return

    db.update({"is_downloaded": True}, query.uuid == url_id)


def db_set_url_rubbish(url_id: str):
    query = Query()
    record = db.get(query.uuid == url_id)
    if record is None:
        return

    db.update({"is_rubbish": True}, query.uuid == url_id)


def db_is_url_present(url: str):
    query = Query()
    record = db.get(query.url == url)
    return record is not None
