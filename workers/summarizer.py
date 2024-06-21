from core.databases.db_crawl_tasks import (
    db_are_crawl_tasks_fully_embedded,
)
from core.databases.db_embeddings import (
    db_search_for_similar_queries,
    db_get_currently_used_vector_model,
)
from core.databases.db_completion_tasks import (
    db_get_incomplete_completion_tasks,
    db_update_completion_task_after_summarizing,
    db_release_executing_tasks,
    db_required_crawl_tasks_for_uuid,
)
from langchain_core.runnables import RunnableLambda
from core.classes.query import WebQuery
from core.chainables.web import (
    web_docs_lookup_prompt,
    web_news_lookup_prompt,
    web_wiki_lookup_prompt,
)
from core.tools.model_loader import load_llm
from langchain_core.output_parsers import StrOutputParser
from core.tools import utils

from core.tools.utils import sleep_noisy
from colorama import Fore, Style

output_parser = StrOutputParser()

llm = None

# even though a single task takes a long time to complete,
# as soon as one task is started, all elements of the queue are released
task_queue = []
task_queue_limit = 10


def extract_uuid(task):
    return task.uuid


def summarize():
    global task_queue, llm

    if llm is None:
        llm = load_llm()

    queue_space = task_queue_limit - len(task_queue)
    task_queue += db_get_incomplete_completion_tasks(queue_space)

    current_task = None

    current_vec_db_model = db_get_currently_used_vector_model()

    # find the first task ready for execution, dismiss the others
    for task in task_queue:
        # check all dependencies for completeness
        dep_list = db_required_crawl_tasks_for_uuid(task.uuid)

        if db_are_crawl_tasks_fully_embedded(dep_list, current_vec_db_model):
            current_task = task
            task_queue.remove(task)
            task_uuid_list = list(map(extract_uuid, task_queue))
            db_release_executing_tasks(task_uuid_list)
            utils.send_update_to_api(
                current_task.uuid, "embedding completed", "update_status", ""
            )

    if current_task is None:
        return

    task_query = WebQuery(
        prompt_core=current_task.prompt, query_type=current_task.mode.lower()
    )

    context = db_search_for_similar_queries(task_query)

    if context is None:
        return

    def interpret_prompt_mode():
        if current_task.mode == "news":
            return web_news_lookup_prompt()
        elif current_task.mode == "docs":
            return web_docs_lookup_prompt()
        elif current_task.mode == "wiki":
            return web_wiki_lookup_prompt()

    def get_user_prompt(_: dict):
        return current_task.prompt

    def get_context(_: dict):
        return context[0].page_content

    web_interpret_prompt_mode = interpret_prompt_mode()

    print("Summarizing task with uuid: ", current_task.uuid)
    chain = (
        {
            "search_data": RunnableLambda(get_context),
            # this has to be a RunnableLambda, it cannot be a string
            "user_request": RunnableLambda(get_user_prompt),
        }
        | web_interpret_prompt_mode
        | llm
        | output_parser
    )
    summary = chain.invoke(current_task)
    db_update_completion_task_after_summarizing(summary, current_task.uuid)

    print(f"{Fore.CYAN}Completed task with uuid: {Fore.RESET}", current_task.uuid)
    print(f"{Fore.CYAN}Completed task with uuid: {Fore.RESET}", current_task.uuid)
    utils.send_update_to_api(current_task.uuid, "summary completed", "update_status", summary)


previous_queued_tasks = 0

# 1. get a list of available tasks, in the backend they'll be automatically set as executing
# 2. parse through all of them, until one that has all it's dependencies resolved appears
# 3. once one is found to be ready, release all the other tasks (reset 'executing')
# 4. proceed with normal execution

# todo: implement class-based task management system


def start_summarizer():
    global previous_queued_tasks

    while True:
        queue_length = len(task_queue)
        if queue_length > previous_queued_tasks:
            print(f"{Fore.CYAN}{Style.BRIGHT}--- SUMMARIZER ---")
            print(f"RECEIVED NEW TASKS")
            print(f"currently executing:", task_queue[0])

        if queue_length != previous_queued_tasks:
            print(f"{Fore.CYAN}tasks left:", queue_length, f"{Style.RESET_ALL}")
            previous_tasks_queued = queue_length

        summarize()
        sleep_noisy(5)
