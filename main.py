import requests
import uvicorn

from colorama import init as colorama_init, Fore

from configurator import get_runtime_config, args
from core.databases import db_base
from core.tools import errorlib
from schedulers.deepsearcher import start_deep_searcher
from workers.crawler import start_crawler
from workers.embedder import start_embedder
from workers.summarizer import start_summarizer

colorama_init()
db_base.db_init()

# todo: change deep_searcher into a scheduler instead of worker, -s flag
#       this is because workers use cpu, gpu and memory resources in a distributed way,
#       while a scheduler only does lightweight management without any significant load,
#       and most importantly contrary to worker, doesn't require a config file to run
#       theoretically this makes the crawler a scheduler as well, but for now it is a core part

if args.worker_type == "webui":
    # fixme: this is a workaround, webui should be started from it's folder
    uvicorn.run("webui.main:app", host="0.0.0.0", port=8000)

if args.worker_type == "webui":
    errorlib.pretty_error(
        title=f"No flags were provided",
        advice=f"---",
    )

try:
    runtime_config = get_runtime_config()
    if runtime_config.worker_type == "crawler":
        start_crawler()
    if runtime_config.worker_type == "embedder":
        start_embedder()
    if runtime_config.worker_type == "summarizer":
        start_summarizer()
    if runtime_config.worker_type == "deep_searcher":
        start_deep_searcher()

except requests.exceptions.ConnectionError:
    errorlib.pretty_error(
        title=f"OLLAMA called but not running",
        advice=f"To fix this issue run ollama by running {Fore.CYAN}ollama serve",
    )
