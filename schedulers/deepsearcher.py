# The first automatic scheduler.
# When launched, looks at the available data, picks interesting topics and requests deeper searches about them.
from langchain_core.output_parsers import StrOutputParser

from core.databases.db_completion_tasks import CompletionTask
from core.tools.model_loader import load_functional_llm
from core.tools.utils import sleep_noisy


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

llm = load_functional_llm()

output_parser = StrOutputParser()


def are_workers_free():
    # check if there are tasks scheduled waiting for execution
    return True


def get_random_completion() -> CompletionTask:
    pass


def extract_interesting_topics(text: str) -> list[str]:
    # todo: perform semantic grouping of subjects + their context
    pass


def schedule_new_completion(query: str) -> str:
    pass


def start_deepsearch():
    while True:
        # fixme: replace False with free worker checking
        if not are_workers_free():
            continue

        completion = get_random_completion()
        completion_text = completion.completion_result
        topics = extract_interesting_topics(completion_text)

        for topic in topics:
            schedule_new_completion(topic)

        sleep_noisy(6)
