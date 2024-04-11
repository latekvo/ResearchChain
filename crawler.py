import datetime
import os
from urllib.error import HTTPError
from typing import List

from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader

from tinydb import TinyDB, Query

from core.classes.traffic_manager import TrafficManager
from core.tools import utils
from core.classes.query import WebQuery
from core.tools.scraper import query_for_urls
from core.tools.utils import hide_prints

# must-haves:
# - live user prompt interaction+injection,
# - dispatching summarizations,
# - link crawling,
# - link database

# todo: we will split crawler into 2 runtimes, one for crawling, one for embedding.
#       the embedding one will look through db_url for any not vectorized articles.
#       this will allow for automatic re-vectorization in case we get a new embed model.

data_path = "store/data/"
if not os.path.exists(data_path):
    os.makedirs(data_path)

# todo: tinydb is a temporary solution, it does not support multithreading, relations or indexing
db_url_path = data_path + "url_store.json"
db_url = TinyDB(db_url_path)

# 100 links max, then put new ones in db
# this does not increase access speed,
# it only encourages a better mix of broadness and deepness of links
url_queue_limit = 100
url_rapid_queue = []

requested_query_queue = [
    WebQuery("news", "llm", priority=1),
    WebQuery("news", "ai", priority=1),
]

# url order:
# 0. use short memory urls
# 1. refill with non-researched db urls
# 2. refill with google search

google_traffic_manager = TrafficManager()


def db_add_url(url: str, parent_id: str = None):
    new_url_id = utils.gen_uuid()
    current_date = datetime.datetime.now().isoformat()

    entry = {
        "uuid": new_url_id,
        "parent_uuid": parent_id,  # will be useful for url crawling analysis & visualization
        "url": url,
        "date_added": current_date,
        "is_downloaded": False,
        "is_rubbish": False,
        "embedded_by": [],
    }

    db_url.insert(entry)
    return new_url_id


def db_get_not_downloaded() -> list:
    db_query = Query()
    db_results = db_url.search(
        db_query.fragment({"is_downloaded": False, "is_rubbish": False})
    )

    return db_results


def db_set_url_embedded(url_id: str, embedding_model: str):
    query = Query()
    record = db_url.get(query.uuid == url_id)
    if record is None:
        return

    embedded_by = record["embedded_by"]
    embedded_by.append(embedding_model)

    db_url.update({"embedded_by": embedded_by}, query.uuid == url_id)


def db_set_url_downloaded(url_id: str):
    query = Query()
    record = db_url.get(query.uuid == url_id)
    if record is None:
        return

    db_url.update({"is_downloaded": True}, query.uuid == url_id)


def db_set_url_rubbish(url_id: str):
    query = Query()
    record = db_url.get(query.uuid == url_id)
    if record is None:
        return

    db_url.update({"is_rubbish": True}, query.uuid == url_id)


def db_is_url_present(url: str):
    # check db_url for presence
    query = Query()
    record = db_url.get(query.url == url)
    return record is not None


def rq_refill(seed_query: WebQuery = None, use_google: bool = True):
    global url_rapid_queue

    # 0. check for space
    space_left = url_queue_limit - len(url_rapid_queue)
    if space_left < 1:
        return

    # 1. get from db
    # todo: currently downloaded = embedded, be careful here when adding separate embedder
    db_url_objects = db_get_not_downloaded()
    space_left = space_left - len(db_url_objects)

    # 2. get from google
    google_url_objects = []
    if use_google and seed_query is not None:
        quit_unexpectedly = False

        if google_traffic_manager.is_timeout_active():
            quit_unexpectedly = True

        google_urls = query_for_urls(seed_query, space_left)

        idx = 0  # using index to avoid converting this generator to list

        if not quit_unexpectedly:
            try:
                for url in google_urls:
                    if db_is_url_present(url):
                        continue
                    new_url_object = db_add_url(url)
                    google_url_objects.append(new_url_object)
                    idx += 1
                google_traffic_manager.report_no_timeout()
            except HTTPError:
                # google requires a long delay after getting timeout
                print("Google timeout")
                quit_unexpectedly = True
                google_traffic_manager.report_timeout()

        # no more new search results are present
        if idx == 0 and not quit_unexpectedly:
            requested_query_queue.remove(seed_query)
            print("removed exhausted query:", seed_query.web_query)

    # 3. fill from db + google
    url_rapid_queue = url_rapid_queue + db_url_objects
    url_rapid_queue = url_rapid_queue + google_url_objects

    print("queue", url_rapid_queue)

    return


def url_save(url: str, parent_id: str = None):
    # 0. check if url was already saved
    if db_is_url_present(url):
        return

    # 1. add to the db
    db_add_url(url, parent_id)

    # 2. place in short-term memory (if there is any space left)
    if len(url_rapid_queue) < url_queue_limit:
        url_rapid_queue.append(url)


def get_document(url: str):
    # we expect the document might not be a pdf from PyPDFLoader
    # and expect that the site might block us from WebBaseLoader
    with hide_prints():
        try:
            document = PyPDFLoader(url).load()
        except Exception:
            try:
                document = WebBaseLoader(url).load()
            except Exception:
                return None

    return document[0]


def url_download(url_object):
    url_uuid = url_object["uuid"]
    url_addr = url_object["url"]
    document = get_document(url_addr)
    if document is None:
        db_set_url_rubbish(url_uuid)
        return None

    document_text = document.page_content

    with open("store/data/" + url_uuid, "w") as f:
        f.write(document_text)

    db_set_url_downloaded(url_uuid)
    return document_text


def process_url(url_object):
    url_uuid = url_object["uuid"]
    url_addr = url_object["url"]

    # 0. download article
    document_text = url_download(url_uuid, url_addr)

    # download failed
    if document_text is None:
        return

    # 1. extract all links
    url_list = utils.extract_links(document_text)

    # 2. save all links
    for link in url_list:
        url_save(link, url_uuid)


def processing_iteration():
    seed_query = None

    if len(requested_query_queue) > 0:
        seed_query = requested_query_queue[0]

    rq_refill(seed_query=seed_query)

    if len(url_rapid_queue) == 0:
        return

    url_object = url_rapid_queue.pop(0)
    process_url(url_object)


processing_iteration()
while len(url_rapid_queue) > 0:
    processing_iteration()

    """ debug, progress tracker
    db_query = Query()
    db_not_downloaded = db_url.search(db_query.fragment({'is_downloaded': False, 'is_rubbish': False}))
    db_rubbish = db_url.search(db_query.fragment({'is_downloaded': False, 'is_rubbish': False}))
    db_total = db_url.all()

    print("urls left to be downloaded:", len(db_not_downloaded))
    print("urls marked rubbish:", len(db_rubbish))
    print("url running total:", len(db_total))
    """
