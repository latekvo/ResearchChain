import os

from colorama import Fore, Style

debug = os.environ.get("DEBUG")

# errors meant to be seen by the user


def pretty_error(title: str, advice: str):
    global debug
    err_content = (
        f"\n{Fore.RED}{Style.BRIGHT}{title}{Style.RESET_ALL}\n"
        f"{advice}{Style.RESET_ALL}\n"
        f"Run {Fore.CYAN}main.py -h{Fore.RESET} for more details\n"
    )

    if debug == 1 or debug is True:
        raise ValueError(err_content)

    print(err_content)
    exit(1)
