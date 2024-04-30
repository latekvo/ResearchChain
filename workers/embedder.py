# embedding worker
# url_db -> THIS -> THIS.vector_db
from colorama import Fore
from tinydb import Query
from tinydb.table import Document

from core.databases import db_url_pool, db_embeddings
from core.models.configurations import use_configuration
from core.tools import utils

rapid_queue_limit = 40
rapid_queue: list[Document] = []

# llm will be used - passed to an agentic preprocessor
llm_config, embedder_config = use_configuration()

# important note to remember for later
# we can avoid the ... issue if we just lock the db for every transaction,
# so we lock the db, select 20 or so records, then lock them for ourselves with an update


def processing_iteration():
    embed_model_name = embedder_config.model_name

    embedding_queue = db_url_pool.db_get_not_embedded(embed_model_name)

    for url_object in embedding_queue:
        print("embedding document:", url_object)
        document = url_object["text"]

        db_full_name = utils.gen_vec_db_full_name("embeddings", embed_model_name)
        db_embeddings.db_add_text_batch(document, db_full_name)
        db_url_pool.db_set_url_embedded(url_object["uuid"], embed_model_name)

    print(f"{Fore.CYAN}Document vectorization completed.{Fore.RESET}")


processing_iteration()
while True:
    db_query = Query()
    db_not_embedded = db_url_pool.db_get_not_embedded(embedder_config.model_name)
    db_total = db_url_pool.db.all()

    print("urls left to be embedded:", len(db_not_embedded))
    print("url running total:", len(db_total))

    processing_iteration()
