import curses
import requests
import uvicorn
from colorama import init as colorama_init, Fore, Style

from configurator import get_runtime_config
from terminal_gui import user_input, select_input
from core.lookup import web_lookup
from workers.crawler import start_crawler
from workers.embedder import start_embedder
from workers.summarizer import start_summarizer

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
    try:
        mode_input = curses.wrapper(select_input)
        text_input = curses.wrapper(user_input)
        print(f"{Fore.GREEN}{Style.BRIGHT}Mode: {Fore.RESET}{mode_input}")
        print(f"{Fore.GREEN}{Style.BRIGHT}Input: {Fore.RESET}{text_input}")
    except curses.error:
        # terminal is not present,
        # user likely tries running through IDE
        print(
            f"{Fore.YELLOW}Terminal not detected, full functionality may not be available.{Fore.RESET}"
        )
        mode_input = "Wiki"
        text_input = input(f"{Fore.GREEN}{Style.BRIGHT}(user){Fore.RESET} ")

    chain_output = web_lookup.invoke({"input": text_input, "mode": mode_input})
    print(f"{Fore.GREEN}{Style.BRIGHT}(llm){Fore.RESET} ", end="")
    print(chain_output, end="", flush=True)
    print(end="\n")
except requests.exceptions.ConnectionError:
    print(
        f"{Fore.RED}{Style.BRIGHT}Connection error, make sure Ollama server is running...{Fore.RESET}{Style.RESET_ALL}"
    )
