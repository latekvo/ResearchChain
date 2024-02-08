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

from googlesearch import search

model = "llama2-uncensored:7b"
model_base_name = model.split(':')[0]
llm = Ollama(model=model)
embeddings = OllamaEmbeddings(model=model)
db = FAISS.load_local(folder_path='store', embeddings=embeddings, index_name=model_base_name)
output_parser = StrOutputParser()


def _rag_chain_function(prompt_text: str):
    return prompt_text


def _web_query_google_lookup(prompt_text: str):
    print(f"{Fore.CYAN}{Style.BRIGHT}Searching for:{Style.RESET_ALL}", prompt_text)

    url_list = list(search(prompt_text, stop=20, lang='en', safe='off'))

    print(f"{Fore.CYAN}Web search completed.{Fore.RESET}")

    # download and embed all of the documents
    for url in url_list:
        documents = WebBaseLoader(url).load_and_split(RecursiveCharacterTextSplitter())
        db.add_documents(documents)
    db.save_local(folder_path='store', index_name=model_base_name)

    print(f"{Fore.CYAN}Document vectorization completed.{Fore.RESET}")

    # return the document with the highest prompt similarity score (for now only browsing the first search result)
    embedding_vector = embeddings.embed_query(prompt_text)
    docs_and_scores = db.similarity_search_by_vector(embedding_vector)

    print(f"{Fore.CYAN}{Style.BRIGHT}Top search results:{Style.RESET_ALL}", docs_and_scores)

    return docs_and_scores[0].page_content  # returning the best scoring document.


def _web_chain_function(prompt_dict: dict):
    web_query_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are web prompt creator"
                   "Your job is to convert the given input into a very short, concise google search prompt."
                   "The prompt should contain as many keywords describing the prompt as possible."
                   "Do not reply with anything else beside the google prompt."
                   "Do not encase the google search prompt into anything, just output it."
                   "Make sure the google search prompt describes the input, but is not too large."
                   "DO NOT INCLUDE ANY TEXT BESIDES THE SEARCH PROMPT!"),
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
        {"input": web_query_prompt | llm | RunnableLambda(_web_query_google_lookup)} |
        web_interpret_prompt |
        llm |
        output_parser
    )

    return chain.invoke(prompt_dict)


rag_lookup = RunnableLambda(_rag_chain_function)
web_lookup = RunnableLambda(_web_chain_function)


def _lookup_determining_proxy(prompt_input: str):
    web_chain = web_lookup
    if 'google' in prompt_input.lower():
        web_chain.invoke({'input': prompt_input})
    return prompt_input


lookup_parser = RunnableLambda(_lookup_determining_proxy)
