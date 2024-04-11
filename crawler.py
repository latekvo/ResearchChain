import os
from urllib.error import HTTPError

from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from tinydb import Query

from core.classes.traffic_manager import TrafficManager
from core.databases import db_url_pool
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


def rq_refill(seed_query: WebQuery = None, use_google: bool = True):
    global url_rapid_queue

    # 0. check for space
    space_left = url_queue_limit - len(url_rapid_queue)
    if space_left < 1:
        return

    # 1. get from db
    # todo: currently downloaded = embedded, be careful here when adding separate embedder
    db_url_objects = db_url_pool.db_get_not_downloaded()
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
                    if db_url_pool.db_is_url_present(url):
                        continue
                    prompt = seed_query.web_query
                    new_url_object = db_url_pool.db_add_url(url, prompt, None)
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
    if db_url_pool.db_is_url_present(url):
        return

    # 1. add to the db
    db_url_pool.db_add_url(url, parent_id)


def url_download_text(url: str):
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
    document = url_download_text(url_addr)
    if document is None:
        db_url_pool.db_set_url_rubbish(url_uuid)
        return None

    document_text = document.page_content

    db_url_pool.db_set_url_downloaded(url_uuid, document_text)
    return document_text


def process_url(url_object):
    url_uuid = url_object["uuid"]

    # 0. download article
    document_text = url_download(url_object)

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
    db_query = Query()
    db_not_downloaded = db_url_pool.db.search(
        db_query.fragment({"is_downloaded": False, "is_rubbish": False})
    )
    db_rubbish = db_url_pool.db.search(db_query.fragment({"is_rubbish": True}))
    db_total = db_url_pool.db.all()

    print("urls left to be downloaded:", len(db_not_downloaded))
    print("urls marked rubbish:", len(db_rubbish))
    print("url running total:", len(db_total))

    processing_iteration()
