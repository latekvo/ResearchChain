from urllib.error import HTTPError

from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from tinydb import Query

from core.classes.traffic_manager import TrafficManager
from core.databases import db_url_pool, db_crawl_tasks
from core.tools import utils
from core.classes.query import WebQuery
from core.tools.scraper import query_for_urls
from core.tools.utils import hide_prints

# 100 links max, then put new ones in db
# this does not increase access speed,
# it only encourages a better mix of broadness and deepness of links
url_queue_limit = 80
url_rapid_queue = []

# populated by db_crawl_tasks database
requested_tasks_limit = 1  # each takes up to several minutes, no need in caching
requested_crawl_tasks = []

# url order:
# 0. use short memory urls
# 1. refill with non-researched db urls
# 2. refill with google search

google_traffic_manager = TrafficManager()


def rq_refill(seed_task, use_google: bool = True):
    global url_rapid_queue

    print("loaded task:", seed_task)

    # adapt crawl_task to web_query
    seed_query = None

    if seed_task is not None:
        seed_query = WebQuery(query_type=seed_task.type, prompt_core=seed_task.prompt)

    # 0. check for space
    url_space_left = url_queue_limit - len(url_rapid_queue)
    if url_space_left < 1:
        return

    # 1. get from db
    db_url_objects = db_url_pool.db_get_not_downloaded()
    url_space_left = url_space_left - len(db_url_objects)

    # 2. get from google
    google_url_objects = []
    if use_google and seed_query is not None:
        quit_unexpectedly = False

        if google_traffic_manager.is_timeout_active():
            quit_unexpectedly = True

        google_urls = query_for_urls(seed_query, url_space_left)

        idx = 0  # using index to avoid converting this generator to list

        if not quit_unexpectedly:
            try:
                for url in google_urls:

                    if db_url_pool.db_is_url_present(url):
                        continue

                    prompt = seed_query.web_query
                    new_url_object = db_url_pool.db_add_url(
                        url=url,
                        prompt=prompt,
                        parent_uuid=None,
                        task_uuid=seed_task.uuid,
                    )

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
            requested_crawl_tasks.remove(seed_task)
            db_crawl_tasks.db_set_crawl_completed(seed_task.uuid)
            print("removed exhausted query:", seed_query.web_query)

    # 3. fill from db + google
    url_rapid_queue = url_rapid_queue + db_url_objects
    url_rapid_queue = url_rapid_queue + google_url_objects

    return


def url_save(url: str, parent_uuid: str = None, task_uuid: str = None):
    # 0. check if url was already saved
    if db_url_pool.db_is_url_present(url):
        return

    # 1. add to the db
    db_url_pool.db_add_url(
        url=url, prompt="N/A", parent_uuid=parent_uuid, task_uuid=task_uuid
    )


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
    url_task_uuid = url_object["task_uuid"]

    # 0. download article
    document_text = url_download(url_object)

    # download failed
    if document_text is None:
        return

    # 1. extract all links
    url_list = utils.extract_links(document_text)

    # 2. save all links
    for link in url_list:
        url_save(url=link, parent_uuid=url_uuid, task_uuid=url_task_uuid)


def processing_iteration():
    global requested_crawl_tasks

    task_space_left = requested_tasks_limit - len(requested_crawl_tasks)
    if task_space_left > 0:
        new_tasks = db_crawl_tasks.db_get_crawl_task()
        requested_crawl_tasks.append(new_tasks)

    seed_task = None

    if len(requested_crawl_tasks) > 0:
        seed_task = requested_crawl_tasks[0]

    rq_refill(seed_task=seed_task)

    if len(url_rapid_queue) == 0:
        return

    url_object = url_rapid_queue.pop(0)
    process_url(url_object)


previous_db_not_downloaded = None


def start_crawler():
    global previous_db_not_downloaded
    while True:
        db_query = Query()
        db_not_downloaded = db_url_pool.db.search(
            db_query.fragment({"is_downloaded": False, "is_rubbish": False})
        )
        db_rubbish = db_url_pool.db.search(db_query.fragment({"is_rubbish": True}))
        db_total = db_url_pool.db.all()

        if db_not_downloaded != previous_db_not_downloaded:
            print("urls left to be downloaded:", len(db_not_downloaded))
            print("urls marked rubbish:", len(db_rubbish))
            print("url running total:", len(db_total))
            previous_db_not_downloaded = db_not_downloaded

        processing_iteration()
