import datetime

from langchain_community.document_loaders import WebBaseLoader
from tinydb import TinyDB, Query
from core.tools import utils

# must-haves:
# - live user prompt interaction+injection,
# - dispatching summarizations,
# - link crawling,
# - link database

# todo: we will split crawler into 2 runtimes, one for crawling, one for embedding.
#       the embedding one will look through db_url for any not vectorized articles.
#       this will allow for automatic re-vectorization in case we get a new embed model.

# todo: tinydb is a temporary solution, it does not support multithreading, relations or indexing
db_url_path = 'store/data/url_store.json'
db_url = TinyDB(db_url_path)

# 100 links max, then put new ones in db
# this ensures a good balance of broadness and deepness
# todo: add this feature
url_queue_limit = 100
url_rapid_queue = []


# url order:
# 0. use short memory urls
# 1. refill with non-researched db urls
# 2. refill with google search


def db_add_url(url: str, parent_id: str | None):
    new_url_id = utils.gen_uuid()
    current_date = datetime.datetime.now()

    # todo: transition to data classes once a solid protocol is defined
    entry = {
        'uuid': new_url_id,
        'parent_uuid': parent_id,  # will be useful for url crawling analysis & visualization

        'url': url,
        'date_added': current_date,
        'is_downloaded': False,
        'embedded_by': []
    }

    db_url.insert(entry)
    return new_url_id


def db_set_url_embedded(url_id: str, embedding_model: str):
    query = Query()
    record = db_url.get(query.uuid == url_id)
    if record is None:
        return

    embedded_by = record['embedded_by']
    embedded_by.append(embedding_model)

    db_url.update({'embedded_by': embedded_by}, query.uuid == url_id)


def db_set_url_downloaded(url_id: str):
    query = Query()
    record = db_url.get(query.uuid == url_id)
    if record is None:
        return

    db_url.update({'is_downloaded': True}, query.uuid == url_id)


def db_is_url_present(url: str):
    # check db_url for presence
    query = Query()
    record = db_url.get(query.url == url)
    return record is not None


def rq_is_url_present(url: str):
    # todo: add rapid queue
    return False


def rq_push_url(url: str):
    # todo: add rapid queue
    pass


def rq_refill(use_google: bool = True):
    # todo: add rapid queue
    # 0. check for space
    # 1. fill from db
    # 2. fill from google
    return False


def url_save(url: str, parent_id: str | None):
    # 0. check if url was already saved
    if rq_is_url_present(url):
        return

    # 1. add to the db
    if not db_is_url_present(url):
        db_add_url(url, parent_id)

    # 2. place in short-term memory (if there is any space left)
    if len(url_rapid_queue) < url_queue_limit:
        url_rapid_queue.append(url)


def url_download(url_id: str) -> str:
    query = Query()
    record = db_url.get(query.uuid == url_id)
    url = record['url']

    document = WebBaseLoader(url).load()[0]
    document_text = document.page_content

    with open('store/data/' + url_id, 'w') as f:
        f.write(document_text)

    db_set_url_downloaded(url_id)
    return document_text


def process_url(url_id: str):
    # todo: use uuid for input, operate closely with db to only modify records
    # 0. download article
    document_text = url_download(url_id)

    # 1. extract all links
    url_list = utils.extract_links(document_text)

    # 2. save all links
    for link in url_list:
        url_save(link, url_id)

    # 3. update own db record with data
    # ^  uuid (key), url (old), date, file_hash, [embedded_by, ...]
    db_set_url_embedded(url_id, 'placeholder')


def processing_iteration():
    if len(url_rapid_queue) is 0:
        rq_refill()
        return

    url_id = url_rapid_queue.pop(0)
    process_url(url_id)


# repeat for testing
for _ in range(3):
    processing_iteration()
