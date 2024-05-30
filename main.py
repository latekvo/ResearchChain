import requests
import uvicorn

from colorama import init as colorama_init, Fore

from configurator import get_runtime_config
from core.tools import errorlib
from workers.crawler import start_crawler
from workers.embedder import start_embedder
from workers.summarizer import start_summarizer

colorama_init()
runtime_config = get_runtime_config()

if runtime_config.worker_type == "none":
    errorlib.pretty_error(
        title=f"No flags were provided",
        advice=f"---",
    )

try:
    if runtime_config.worker_type == "webui":
        # this is a workaround :P
        uvicorn.run("webui.main:app")
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
