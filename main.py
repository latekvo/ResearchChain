import requests

from colorama import init as colorama_init, Fore, Style

from configurator import get_runtime_config
from workers.crawler import start_crawler
from workers.embedder import start_embedder
from workers.summarizer import start_summarizer

colorama_init()
runtime_config = get_runtime_config()

if runtime_config.worker_type == "crawler":
    print("starting crawler")
    start_crawler()
if runtime_config.worker_type == "embedder":
    print("starting embedder")

    start_embedder()
if runtime_config.worker_type == "summarizer":
    print("starting summarizer")

    start_summarizer()

print("going through")

try:
    pass
except requests.exceptions.ConnectionError:
    print(
        f"{Fore.RED}{Style.BRIGHT}Connection error, make sure Ollama server is running...{Fore.RESET}{Style.RESET_ALL}"
    )
