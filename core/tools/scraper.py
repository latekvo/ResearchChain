import tiktoken
from googlesearch import search
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from colorama import Fore, Style

from configurator import get_runtime_config
from core.classes.query import WebQuery

encoder = tiktoken.get_encoding("cl100k_base")
output_parser = StrOutputParser()

runtime_configuration = get_runtime_config()


def docs_to_context(docs_and_scores: list[Document], token_limit: int) -> str:
    context_text = ""
    token_count = 0
    document_index = 0
    while token_count < token_limit:
        token_count += len(encoder.encode(docs_and_scores[document_index].page_content))
        context_text += docs_and_scores[document_index].page_content
        document_index += 1
        if document_index >= len(docs_and_scores):
            break

    print(
        f"{Fore.CYAN}Used {document_index + 1} snippets with a total of {token_count} tokens as context.{Fore.RESET}"
    )
    print(f"{Fore.CYAN}Context itself: {Fore.RESET}", context_text)
    return context_text


def query_for_urls(query: WebQuery, url_amount=10) -> list[str]:
    print(f"{Fore.CYAN}{Style.BRIGHT}Searching for:{Style.RESET_ALL}", query.web_query)

    url_list = search(
        query=query.web_query,
        stop=url_amount,
        lang="en",
        safe="off",
        tbs=query.web_tbs,
        extra_params=query.web_extra_params,
    )
    print(f"{Fore.CYAN}Web search completed.{Fore.RESET}")
    return url_list
