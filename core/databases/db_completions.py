from tinydb import Query

from core.databases import defaults
from core.tools import utils
from core.tools.utils import use_tinydb

db = use_tinydb("completions")

# we have to use a document database with this one,
# as completions will be large chunks of data of variable size


def db_add_completion(text, prompt="N/A"):
    new_uuid = utils.gen_uuid()
    timestamp = utils.gen_unix_time()

    db.insert(
        {
            "uuid": new_uuid,
            "prompt": prompt,
            "response": text,
            "timestamp": timestamp,
        }
    )

    return new_uuid


def db_get_completions_by_date(start_date: int, end_date: int) -> list:
    fields = Query()

    results = db.search(start_date < fields.timestamp < end_date)
    return results


def db_get_completions_by_page(
    page: int, per_page: int = defaults.ITEMS_PER_PAGE
) -> list:
    splice_start = page * per_page
    splice_end = splice_start + per_page

    # current db doesn't support ranges, return all
    results = db.all()
    return results
