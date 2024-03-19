import requests
from langchain_core.output_parsers import StrOutputParser

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from core.lookup import web_lookup

colorama_init()

# llm = Ollama(model=MODEL_NAME) this is not necessary, but without this line the code does not work

output_parser = StrOutputParser()

chain = web_lookup | output_parser

try:
    input_text = input(f"{Fore.GREEN}{Style.BRIGHT}(user){Fore.RESET}{Style.RESET_ALL} ")
    chain_output = chain.invoke({"input": input_text})
    print(f"{Fore.GREEN}{Style.BRIGHT}(llm){Fore.RESET}{Style.RESET_ALL} ", end="")
    print(chain_output, end="", flush=True)
    print(end='\n')
except requests.exceptions.ConnectionError:
    print(f"{Fore.RED}{Style.BRIGHT}Connection error, make sure Ollama server is running...{Fore.RESET}{Style.RESET_ALL}")
