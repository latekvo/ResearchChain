from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

from lookup import web_lookup, model_name

from datetime import date

colorama_init()

today = date.today()

llm = Ollama(model=model_name)  # this is not necessary, but without this line the code does not work

output_parser = StrOutputParser()

chain = web_lookup | output_parser

# Please find significant events from the past 7 days, emphasizing natural disasters, geopolitical updates, and technological advancements curent date: { str(date)

try:
    Topic = input(f"{Fore.GREEN}{Style.BRIGHT}(Imsert Topic){Fore.RESET}{Style.RESET_ALL} ")
    input_text = f"The Latest {Topic} News: A Comprehensive Overview"
    for output_chunk in chain.stream({"input": input_text}):
        print(output_chunk, end="", flush=True)
    print(end='\n')
except ConnectionError:
    print(f"{Fore.RED}{Style.BRIGHT}Connection error, make sure Ollama server is running...{Fore.RESET}{Style.RESET_ALL}")
