import curses
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
    mode_input = curses.wrapper(select_input)
    text_input = curses.wrapper(user_input)
    print(f'{Fore.GREEN}{Style.BRIGHT}Mode: {Fore.RESET}{mode_input}')
    print(f'{Fore.GREEN}{Style.BRIGHT}Input: {Fore.RESET}{text_input}')
    chain_output = chain.invoke({'input': text_input, 'mode': mode_input})
    print(f'{Fore.GREEN}{Style.BRIGHT}(llm){Fore.RESET} ', end='')
    print(chain_output, end='', flush=True)
    print(end='\n')
except requests.exceptions.ConnectionError:
    print(f'{Fore.RED}{Style.BRIGHT}Connection error, make sure Ollama server is running...{Fore.RESET}{Style.RESET_ALL}')
