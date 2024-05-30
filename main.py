import requests
import uvicorn
from colorama import init as colorama_init, Fore, Style

<<<<<<< HEAD
from configurator import get_runtime_config
from terminal_gui import user_input, select_input
from core.lookup import web_lookup
from workers.crawler import start_crawler
from workers.embedder import start_embedder
from workers.summarizer import start_summarizer
=======
>>>>>>> main

colorama_init()
runtime_config = get_runtime_config()

if runtime_config.worker_type == "crawler":
    start_crawler()
if runtime_config.worker_type == "embedder":
    start_embedder()
if runtime_config.worker_type == "summarizer":
    start_summarizer()

uvicorn.run("webui.main:app")  # Workaround for launching backend service

try:
    pass
except requests.exceptions.ConnectionError:
    print(
        f"{Fore.RED}{Style.BRIGHT}Connection error, make sure Ollama server is running...{Fore.RESET}{Style.RESET_ALL}"
    )
