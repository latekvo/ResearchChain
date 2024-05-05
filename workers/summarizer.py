from core.databases.db_embeddings import db_search_for_similar_queries
from core.databases.db_completion_tasks import db_get_incomplete_completion_task
from langchain_core.runnables import RunnableLambda
from core.classes.query import WebQuery
from core.chainables.web import (
    web_docs_lookup_prompt,
    web_news_lookup_prompt,
    web_wiki_lookup_prompt,
)
from core.tools.model_loader import load_model
from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()

llm = load_model()


def summarize():

    #task = db_get_incomplete_completion_task()
    task = {"prompt": "Elon Musk", "mode": "Wiki"}
    print(task["prompt"])

    def get_query():
        if task["mode"] == "News":
            return WebQuery("news", prompt_core=task["prompt"])
        elif task["mode"] == "Docs":
            return WebQuery("docs", prompt_core=task["prompt"])
        elif task["mode"] == "Wiki":
            return WebQuery("wiki", prompt_core=task["prompt"])

    context = db_search_for_similar_queries(get_query())
    print(context[0].page_content)

    def interpret_prompt_mode():
        if task["mode"] == "News":
            return web_news_lookup_prompt()
        elif task["mode"] == "Docs":
            return web_docs_lookup_prompt()
        elif task["mode"] == "Wiki":
            return web_wiki_lookup_prompt()

    def get_user_prompt(_: dict):
        print(task["prompt"])
        return task["prompt"]

    def get_context(_: dict):
        print(context[0].page_content)
        return context[0].page_content

    web_interpret_prompt_mode = interpret_prompt_mode()

    chain = (
            {
                "search_data": RunnableLambda(get_user_prompt)
                | RunnableLambda(get_context),
                # this has to be a RunnableLambda, it cannot be a string
                "user_request": RunnableLambda(get_user_prompt),
            }
            | web_interpret_prompt_mode
            | llm
            | output_parser
    )
    return chain.invoke(task)


print(summarize())
