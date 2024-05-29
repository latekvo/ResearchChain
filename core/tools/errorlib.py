from colorama import Fore, Style


def assert_error(title: str, advice: str):
    print(
        f"\n{Fore.RED}{Style.BRIGHT}{title}{Style.RESET_ALL}\n"
        f"{advice}{Style.RESET_ALL}\n"
        f"Run {Fore.CYAN}main.py -h{Fore.RESET} for more details"
    )
    exit(1)
