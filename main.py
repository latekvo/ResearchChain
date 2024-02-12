from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from lookup import web_lookup, model_name

colorama_init()

llm = Ollama(model=model_name)

output_parser = StrOutputParser()

chain = web_lookup | output_parser

try:
    input_text = input(f"{Fore.GREEN}{Style.BRIGHT}(user){Fore.RESET}{Style.RESET_ALL} ")
    for output_chunk in chain.stream({"input": input_text}):
        print(output_chunk, end="", flush=True)
    print(end='\n')
except ConnectionError:
    print(f"{Fore.RED}{Style.BRIGHT}Connection error, make sure Ollama server is running...{Fore.RESET}{Style.RESET_ALL}")
