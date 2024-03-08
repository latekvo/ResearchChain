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

from os.path import exists

import tiktoken

# todo: replace with puppeteer, this one gets blocked occasionally
from googlesearch import search

model_name = "zephyr:7b-beta-q5_K_M"  # "llama2-uncensored:7b"
model_base_name = '_'.join('_'.join(model_name.split(':')).split('-'))
token_limit = 4096  # depending on VRAM, try 2048, 3072 or 4096. 2048 works great on 4GB VRAM
llm = Ollama(model=model_name)
embeddings = OllamaEmbeddings(model=model_name)
encoder = tiktoken.get_encoding("cl100k_base")
output_parser = StrOutputParser()

if not exists('store/' + model_base_name + '.faiss'):
    tmp_db = FAISS.from_texts(['You are a large language model, intended for research purposes.'], embeddings)
    tmp_db.save_local(folder_path='store', index_name=model_base_name)

db = FAISS.load_local(
    folder_path='store',
    embeddings=embeddings,
    index_name=model_base_name,
    allow_dangerous_deserialization=True)


def _extract_from_quote(text: str):
    if '"' in text:
        return text.split('"')[1]
    else:
        return text


def _rag_chain_function(prompt_text: str):
    return prompt_text


def _web_query_google_lookup(prompt_text: str):
    prompt_text = _extract_from_quote(prompt_text)  # my current llm returns its answer in this format: answer: "prompt"

    print(f"{Fore.CYAN}{Style.BRIGHT}Searching for:{Style.RESET_ALL}", prompt_text)

    url_list = list(search(prompt_text, stop=5, lang='en', safe='off'))

    print(f"{Fore.CYAN}Web search completed.{Fore.RESET}")

    # download and embed all of the documents
    for url in url_list:
        documents = WebBaseLoader(url).load_and_split(RecursiveCharacterTextSplitter())
        db.add_documents(documents, embeddings=embeddings)
    db.save_local(folder_path='store', index_name=model_base_name)

    print(f"{Fore.CYAN}Document vectorization completed.{Fore.RESET}")

    # return the document with the highest prompt similarity score (for now only browsing the first search result)
    embedding_vector = embeddings.embed_query(prompt_text)
    docs_and_scores = db.similarity_search_by_vector(embedding_vector)

    print(f"{Fore.CYAN}Database search completed.{Fore.RESET}")

    context_text = ""
    token_count = 0
    document_index = 0
    while token_count < token_limit:
        token_count += len(encoder.encode(docs_and_scores[document_index].page_content))
        context_text += docs_and_scores[document_index].page_content
        document_index += 1
        if document_index >= len(docs_and_scores):
            return context_text

    # returning top 3 best results
    return context_text


def _web_chain_function(prompt_dict: dict):

    web_query_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are web prompt creator"
                   "Your job is to convert the given input into a very short, concise google search prompt."
                   "The prompt should contain as many keywords describing the prompt as possible."
                   "Do not reply with anything else beside the google prompt."
                   "Do not encase the google search prompt into anything, just output it."
                   "Make sure the google search prompt describes the input with keywords, but is not too large."
                   "DO NOT INCLUDE ANY TEXT BESIDES THE SEARCH PROMPT!"),
        ("user", "{input}")
    ])

    web_interpret_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a search results interpreter. Expand the provided input focusing on the most important parts."
         "Your job is to convert all the search results you were given into a long, comprehensive and clean output."
         "Use provided search results data to answer the user request to the best of your ability."),
        ("user", "Search results data: "
                 "```"
                 "{search_data}"
                 "```"
                 "User request: \"{user_request}\"")
    ])

    def get_user_prompt(_: dict):
        return prompt_dict['input']

    # NOTE: a detour has been performed here, more details:
    #       web_chain_function will soon become just a tool playing a part of a larger mechanism.
    #       prompt creation will be taken over by prompt sentiment extractor which will extract all researchable
    #       queries from the user prompt, and start separate chains performing those steps in parallel
    #       until a satisfactory response is created.

    chain = (
        {
            "search_data": RunnableLambda(get_user_prompt) | RunnableLambda(_web_query_google_lookup),
            "user_request": RunnableLambda(get_user_prompt)  # this has to be a RunnableLambda, it cannot be a string
        } |
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
