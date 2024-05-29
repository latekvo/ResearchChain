import requests

from colorama import init as colorama_init, Fore, Style


colorama_init()

try:
    pass
except requests.exceptions.ConnectionError:
    print(
        f"{Fore.RED}{Style.BRIGHT}Connection error, make sure Ollama server is running...{Fore.RESET}{Style.RESET_ALL}"
    )
