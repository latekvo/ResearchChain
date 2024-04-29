# embedding worker
# url_db -> THIS -> THIS.vector_db
from colorama import Fore
from tinydb import Query
from tinydb.table import Document

from core.databases import db_url_pool, db_embeddings
from core.models.configurations import use_configuration

rapid_queue_limit = 40
rapid_queue: list[Document] = []

# llm will be used - passed to an agentic preprocessor
llm_config, embedder_config = use_configuration()

# important note to remember for later
# we can avoid the ... issue if we just lock the db for every transaction,
# so we lock the db, select 20 or so records, then lock them for ourselves with an update


def processing_iteration():
    global rapid_queue

    url_queue_remaining_space = rapid_queue_limit - len(rapid_queue)
    if url_queue_remaining_space < rapid_queue_limit:
        rapid_queue += db_url_pool.db_get_not_embedded(embedder_config.model_name)

    for url_object in rapid_queue:
        print(url_object.values)
        document = url_object.text
        document_uuid = url_object.parent_uuid

        db_embeddings.db_add_text_batch(document, document_uuid)

    print(f"{Fore.CYAN}Document vectorization completed.{Fore.RESET}")


processing_iteration()
while True:
    db_query = Query()
    db_not_embedded = db_url_pool.db_get_not_embedded(embedder_config.model_name)
    db_total = db_url_pool.db.all()

    print("urls left to be embedded:", len(db_not_embedded))
    print("url running total:", len(db_total))

    processing_iteration()
