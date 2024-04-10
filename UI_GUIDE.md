## Guide for UI developers, no matter the platform.
To interact with the rest of the system, exclusively utilize functions from `core/database/db_xxx`

For a simple applications which only requests summaries and reads the results,<br>
You have to use:
* `db_add_completion_task` to create a task
* `db_get_completions_by_page` to get the results

<br>
Here is an example of how that would look like with `FastAPI`:

```py
@app.post("/add_completion_task")
def add_completion_task(prompt):
    db_add_completion_task(prompt)
    return {
        "status": "OK"
    }


@app.get("/get_completions")
def get_completions(page: int):
    completions = db_get_completions_by_page(page)
    return {
        "completions": completions
    }
```

For a more complicated web page, which can also schedule crawls,
you'll also make use of:
* `db_add_crawl_task` to schedule a new crawl
* `db_get_crawl_history_by_page` to see the crawls you scheduled, and their status

#### Important notes
* Currently, there is no system present which would automatically populate
the embeddings database after scheduling a completion task.
This means, that the UI has to ensure all the databases are appropriately populated.
As a result, before requesting a summary, it's necessary to perform crawls
to give our summaries enough context to work with.

* All db calls return lists of entire objects, unless it's specified otherwise.
This is the default since we're prioritizing speed and minimal latency over 
security.