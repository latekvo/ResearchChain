import requests
import uvicorn

from colorama import init as colorama_init, Fore

from configurator import get_runtime_config, args
from core.databases import db_base
from core.tools import errorlib
from workers.crawler import start_crawler
from workers.embedder import start_embedder
from workers.summarizer import start_summarizer

colorama_init()
db_base.db_init()

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
except requests.exceptions.ConnectionError:
    errorlib.pretty_error(
        title=f"OLLAMA called but not running",
        advice=f"To fix this issue run ollama by running {Fore.CYAN}ollama serve",
    )
