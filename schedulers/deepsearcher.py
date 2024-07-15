# The first automatic scheduler.
# When launched, looks at the available data, picks interesting topics and requests deeper searches about them.
from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser

from core.chainables.web import structured_extraction_prompt
from core.databases.db_completion_tasks import (
    CompletionTask,
    db_get_complete_completion_tasks,
    db_add_completion_task,
)
from core.tools.model_loader import load_llm
from core.tools.utils import sleep_noisy, remove_characters

# get finished tasks
# extract interesting talking points
# repeat until a unique one has been found
# create new tasks out of it

# we can also make a great use of embedding here
# use very broad embeddings to see which topics align the most with others
# to see how well certain topic is developed so far

# poc: just get a random summary and dispatch a new one from it
# then: grab a random topic from one of the summaries, and focus on it,
#       continuously condensing summaries and requesting them on deeper topics

# TODO: move all LLM load to summarizer, local for now

llm = load_llm()
output_parser = StrOutputParser()

extraction_chain = structured_extraction_prompt() | llm | output_parser


def are_workers_free():
    # todo: check if there are non-busy workers available
    return True


def get_random_completion() -> CompletionTask | None:
    completions_list = db_get_complete_completion_tasks()
    if len(completions_list) > 0:
        return completions_list[0]
    else:
        return None


def extract_interesting_topics(text: str) -> list[str]:
    # todo: separate function for extracting topics and getting one,
    #       run the extraction one only when lacking topics
    # todo: perform semantic grouping of subjects + their context
    # fixme: instead of TODO, extracting a single topic as a POC for now
    extraction_request = "Find exactly one topic from this text, it must be interesting. Reply in 3 words at most."

    result = extraction_chain.invoke({"data": text, "user_request": extraction_request})

    return [result]


def schedule_new_completion(query: str) -> str:
    # fixme: regex remove anything not a-zA-Z
    pure_query = remove_characters(query, ['"', "'", ':', '?', '!'])
    return db_add_completion_task(pure_query, "info")


def start_deep_searcher():
    while True:
        # fixme: replace False with free worker checking
        if not are_workers_free():
            sleep_noisy(6)
            continue

        completion = get_random_completion()

        if not completion:
            sleep_noisy(6)
            continue

        completion_text = completion.completion_result
        topics = extract_interesting_topics(completion_text)

        for topic in topics:
            print('dispatching new summaries:', topic)
            schedule_new_completion(topic)

        sleep_noisy(6)
        print("DBG: shutting down deep_searcher - only 1 loop scheduled")
        return
