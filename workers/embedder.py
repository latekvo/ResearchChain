# embedding worker
# url_db -> THIS -> THIS.vector_db
from colorama import Fore, Style
from tinydb.table import Document

from configurator import get_runtime_config
from core.databases import db_url_pool, db_embeddings, db_crawl_tasks
from core.tools import utils
from core.tools.utils import sleep_noisy

rapid_queue_limit = 40
rapid_queue: list[Document] = []

# llm will be used - passed to an agentic preprocessor
runtime_configuration = get_runtime_config()
llm_config = runtime_configuration.llm_config
embedder_config = runtime_configuration.embedder_config

# important note to remember for later
# we can avoid the ... issue if we just lock the db for every transaction,
# so we lock the db, select 20 or so records, then lock them for ourselves with an update


def processing_iteration():
    embed_model_name = embedder_config.model_name

    embedding_queue = db_url_pool.db_get_not_embedded(embed_model_name)

    for url_object in embedding_queue:
        document = url_object.text
        task_uuid = url_object.task_uuid

        db_full_name = utils.gen_vec_db_full_name("embeddings", embed_model_name)

        db_embeddings.db_add_text_batch(document, db_full_name)
        db_url_pool.db_set_url_embedded(url_object.uuid, embed_model_name)
        db_crawl_tasks.db_increment_task_embedding_progression(
            task_uuid, embed_model_name
        )
    utils.send_update_to_api(embedding_queue[0].task_uuid, "embedding completed", "update_status")


previous_tasks_queued = 0


def start_embedder():
    global previous_tasks_queued
    while True:
        queue_length = len(rapid_queue)
        if queue_length > previous_tasks_queued:
            print(f"{Fore.CYAN}{Style.BRIGHT}--- EMBEDDER ---")
            print(f"RECEIVED NEW TASKS")
            print(f"currently executing:", rapid_queue[0])

        if queue_length != previous_tasks_queued:
            print(f"{Fore.CYAN}tasks left:", queue_length)
            previous_tasks_queued = queue_length

        processing_iteration()

        sleep_noisy(6)
