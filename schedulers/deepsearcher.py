# The first automatic scheduler.
# When launched, looks at the available data, picks interesting topics and requests deeper searches about them.
from core.databases.db_completion_tasks import CompletionTask
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

def get_random_completion() -> CompletionTask:
    pass


def extract_interesting_topics() -> list[str]:
    pass


def schedule_new_search() -> str:
    pass


def start_deepsearch():
    while True:
        sleep_noisy(6)
