import curses
import _curses
import requests

from colorama import init as colorama_init, Fore, Style
from core.lookup import web_lookup
from langchain_core.output_parsers import StrOutputParser
from terminal_gui import user_input, select_input

colorama_init()

# llm = Ollama(model=MODEL_NAME) this is not necessary, but without this line the code does not work
output_parser = StrOutputParser()

chain = web_lookup | output_parser

try:
    try:
        mode_input = curses.wrapper(select_input)
        text_input = curses.wrapper(user_input)
        print(f'{Fore.GREEN}{Style.BRIGHT}Mode: {Fore.RESET}{mode_input}')
        print(f'{Fore.GREEN}{Style.BRIGHT}Input: {Fore.RESET}{text_input}')
    except _curses.error:
        # terminal is not present,
        # user likely tries running through IDE
        print(f'{Fore.YELLOW}Terminal not detected, full functionality may not be available.{Fore.RESET}')
        mode_input = 'Wiki'
        text_input = input(f"{Fore.GREEN}{Style.BRIGHT}(user){Fore.RESET} ")

    chain_output = chain.invoke({'input': text_input, 'mode': mode_input})
    print(f'{Fore.GREEN}{Style.BRIGHT}(llm){Fore.RESET} ', end='')
    print(chain_output, end='', flush=True)
    print(end='\n')
except requests.exceptions.ConnectionError:
    print(f'{Fore.RED}{Style.BRIGHT}Connection error, make sure Ollama server is running...{Fore.RESET}{Style.RESET_ALL}')
