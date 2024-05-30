import os

from colorama import Fore, Style

debug = os.environ.get("DEBUG")

# errors meant to be seen by the user


def pretty_error(title: str, advice: str):
    err_content = (
        f"\n{Fore.RED}{Style.BRIGHT}{title}{Style.RESET_ALL}\n"
        f"{advice}{Style.RESET_ALL}\n"
        f"Run {Fore.CYAN}main.py -h{Fore.RESET} for more details\n"
    )

    debug = 1
    if debug == 1:
        raise ValueError(err_content)

    print(err_content)
    exit(1)
