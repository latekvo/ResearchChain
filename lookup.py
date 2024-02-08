from colorama import Fore
from colorama import Style

from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
llm = Ollama(model="llama2-uncensored:7b")
output_parser = StrOutputParser()



"""
docs = loader.load()
embeddings = OllamaEmbeddings()

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)
"""


def _rag_chain_function(prompt_text: str):
    return prompt_text


def _web_query_google_lookup(prompt_text: str):
    return prompt_text


def _web_chain_function(prompt_dict: dict):
    web_query_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are web prompt creator"
                   "Your job is to convert the given input into a very short, concise google search prompt."
                   "The prompt should contain as many keywords describing the prompt as possible."
                   "Do not reply with anything else beside the google prompt."
                   "Do not encase the google search prompt into anything, just output it."
                   "Make sure the google search prompt describes the input, but is not too large."),
        ("user", "{input}")
    ])
    web_interpret_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a search results interpreter. Summarize the provided input focusing on the most important parts."
         "Your job is to summarize the search results you were given."),
        ("user", "Search results: "
                 "```"
                 "{input}"
                 "```")
    ])

    chain = (
        web_query_prompt |
        llm |
        output_parser |
        RunnableLambda(_web_query_google_lookup) |
        web_interpret_prompt |
        llm |
        output_parser
    )

    return chain.invoke(prompt_dict)


rag_lookup = RunnableLambda(_rag_chain_function)
web_lookup = RunnableLambda(_web_chain_function)


def _lookup_determining_proxy(prompt_dict: dict[str, str]):
    web_chain = web_lookup
    if 'google' in prompt_dict['input'].lower():
        web_chain.invoke(prompt_dict)
    return prompt_dict


proxy_parser = RunnableLambda(_lookup_determining_proxy)
