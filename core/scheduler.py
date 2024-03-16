"""
Thread scheduling algorithms:
(with both of these, i assume 1: search can be interrupted, 2: there will be either recursion or total limit)
DFS: would use up the least memory, but could potentially go too deep into one topic
BFS: it really only has to schedule 1 layer ahead so memory wouldn't really be that bad,
     and it could pain a really broad picture, which would allow for better control, as this broad picture
     is already a very specific topic, giving us a very balanced response

So general architecture for now:

short_research() -> string:
    # quick research thread, within context, dispatches other complex operations
    # TODO: at context overflow, we can either stop, reduce and continue, or fork into # smaller threads

each thread can be either a stub, or a node.
- stub: returns with a string, as short as possible, with some key info. Ex:
    - none: basic model response
    - google: just return a summarized google query
    - project-rag: highly specific data set about this project,
                   rag population will be running in background, or with each node.
                   Embeddings on this amount of text are relatively cheap, fast, efficient.
    - response: basic model response
- node: a thread which schedules one of the following:
    - node: recursive thread creation, can be interpreted as a loop with limited iterations
    - stub: one of the stubs listed above

problems:
- error-tolerating function calling has to be implemented, each response HAS to be a function,
  otherwise it has to be either:
  - treated as a basic response
  - redone
  - ignored, discarded, to avoid wasting resources 'Response error' will be returned
- how does the LLM actually determine if the task is complex enough to be split / just googled
- how does the LLM know whether to google, rag, or just respond?
  - divide data into EXTERNAL, INTERNAL, BASIC
  - response may be either INFORMATIVE (lookup), or an OPINION (basic response)
(we have to remember every little evaluation wastes a lot of time)

A generally good approach to this is to provide sample code to these models, and then ask them to use it.
For example:
```
You can use one of these functions:
def function_call(): ...
```
or
```
You are tasked with picking the best function for this task.
Go through your thought process step by step.
Only use one function. (this line will not really work with any small models, we have to be more creative)
options:
- function_call() - this function will let you...
- other_call() - this one will ...
- another_call()

It's just important to be very descriptive, often because of how tokenization works,
models will not recognize the name of the function itself.
For function-calling reference see OpenBMB/ChatDev
"""
import queue
from dataclasses import dataclass


@dataclass
class ThreadObject:
    pass


@dataclass(order=True)
class ThreadTask:
    priority: int
    item: ThreadObject
    pass


thread_queue: queue.PriorityQueue


def new_research_thread(prompt: str, remaining_depth: int) -> str:
    if remaining_depth <= 0:
        return 'SYSTEM ERROR cannot perform operation maximum search depth reached'



def research_loop() -> str:
    pass
