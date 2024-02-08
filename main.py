from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from lookup import proxy_parser

colorama_init()

llm = Ollama(model="llama2-uncensored:7b")

prompt = ChatPromptTemplate.from_messages([
    ("system", "It is currently 2024. You don't have knowledge from before 2022. All your knowledge is outdated."
               "You are a researching assistant. Answer very precisely and shortly." 
               "Your job is very simple, it's to evaluate if user prompt requires usage of the internet, or not."
               "You don't have any recent knowledge, so you may need to use GOOGLE"
               "Any queries asking about innovations, latest news, etc. require GOOGLE"
               "If the user asks about some specific product or event, that requires GOOGLE, so respond with 'GOOGLE'"
               "If query requires google, respond with only a single word: 'GOOGLE'."
               "If query requires web access, do not type ANYTHING besides only the word 'GOOGLE'."
               "Otherwise, reply with an answer."),
    ("user", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | llm | proxy_parser | output_parser

while True:
    try:
        input_text = input(f"{Fore.GREEN}{Style.BRIGHT}(user){Fore.RESET}{Style.RESET_ALL} ")
        for output_chunk in chain.stream({"input": input_text}):
            print(output_chunk, end="", flush=True)
        print(end='\n')
    except ConnectionError:
        print(f"{Fore.RED}{Style.BRIGHT}Connection error, make sure Ollama server is running...{Fore.RESET}{Style.RESET_ALL}")
