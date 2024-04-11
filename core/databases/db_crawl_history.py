import os

from tinydb import TinyDB

from core.databases import defaults
from core.tools import utils

data_path = defaults.DATA_PATH
if not os.path.exists(data_path):
    os.makedirs(data_path)

db_name = "crawl_history"
db_path = data_path + "{}.json".format(db_name)
db = TinyDB(db_path)


# this db is completely optional, only used by the UI, and so it's development can be delayed
# most sensible solution here is to make items of the url_database point to entries of this database
# even better, let's add a prompt field to each entry of the url_database, and count them here
# this db will still be used to store the prompts, and their embeddings, so that the UI
# will have an easy time comparing new prompts to historical ones


def db_add_crawl_history(prompt: str) -> str:
    new_uuid = utils.gen_uuid()
    return new_uuid


def db_add_url_to_crawl_history(url: str, prompt: str) -> str:
    new_uuid = utils.gen_uuid()
    return new_uuid


def db_get_similar_prompts(prompt: str) -> list:
    return []


def db_get_crawl_history_by_page(page: int, per_page=defaults.ITEMS_PER_PAGE) -> list:
    return []
