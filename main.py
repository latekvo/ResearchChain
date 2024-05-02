import curses
import requests

from colorama import init as colorama_init, Fore, Style
from terminal_gui import user_input, select_input
from core.lookup import web_lookup
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"


colorama_init()

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
