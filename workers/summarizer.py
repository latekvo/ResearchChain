from core.databases.db_embeddings import db_search_for_similar_queries
from core.databases.db_completion_tasks import (
    db_get_incomplete_completion_task,
    db_update_completion_task_after_summarizing,
)
from langchain_core.runnables import RunnableLambda
from core.classes.query import WebQuery
from core.chainables.web import (
    web_docs_lookup_prompt,
    web_news_lookup_prompt,
    web_wiki_lookup_prompt,
)
from core.tools.model_loader import load_model
from langchain_core.output_parsers import StrOutputParser

from tinydb import Query
from core.tools.utils import use_tinydb
from colorama import Fore

output_parser = StrOutputParser()

llm, embeddings = load_model()


def summarize():

    task = db_get_incomplete_completion_task()

    if task is not None:

        def get_query():
            return WebQuery(task["mode"].lower(), prompt_core=task["prompt"])

        context = db_search_for_similar_queries(get_query())

        def interpret_prompt_mode():
            if task["mode"] == "News":
                return web_news_lookup_prompt()
            elif task["mode"] == "Docs":
                return web_docs_lookup_prompt()
            elif task["mode"] == "Wiki":
                return web_wiki_lookup_prompt()

        def get_user_prompt(_: dict):
            return task["prompt"]

        def get_context(_: dict):
            return context[0].page_content

        web_interpret_prompt_mode = interpret_prompt_mode()

        print("Summarizing task with uuid: ", task["uuid"])
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
        summary = chain.invoke(task)
        db_update_completion_task_after_summarizing(summary, task["uuid"])

        print(f"{Fore.CYAN}Completed task with uuid: {Fore.RESET}", task["uuid"])


previous_total_tasks = None

while True:
    db = use_tinydb("completion_tasks")
    db_query = Query()
    total_tasks = len(
        db.search(db_query.completed == False and db_query.executing == False)
    )
    if total_tasks is not previous_total_tasks:
        print("Number of uncompleted tasks: ", total_tasks)
    previous_total_tasks = total_tasks

    summarize()
