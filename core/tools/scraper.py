from typing import List

import tiktoken
from colorama import Fore, Style
from googlesearch import search
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from core.models.embeddings import embedding_model_safe_name, embeddings_article_limit, embeddings_buffer_stops, \
    embeddings_chunk_size, embeddings_chunk_overlap, embeddings
from core.tools.dbops import get_db_by_name
from core.tools.query import WebQuery
from core.tools.utils import is_text_junk, remove

encoder = tiktoken.get_encoding("cl100k_base")
output_parser = StrOutputParser()


def docs_to_context(docs_and_scores: List[Document], token_limit: int) -> str:
    context_text = ""
    token_count = 0
    document_index = 0
    while token_count < token_limit:
        token_count += len(encoder.encode(docs_and_scores[document_index].page_content))
        context_text += docs_and_scores[document_index].page_content
        document_index += 1
        if document_index >= len(docs_and_scores):
            break

    print(f"{Fore.CYAN}Used {document_index + 1} snippets with a total of {token_count} tokens as context.{Fore.RESET}")
    print(f"{Fore.CYAN}Context itself: {Fore.RESET}", context_text)
    return context_text


def rag_query_lookup(prompt_text: str) -> str:
    pass


def populate_db_with_google_search(database: FAISS, query: WebQuery):
    print(f"{Fore.CYAN}{Style.BRIGHT}Searching for:{Style.RESET_ALL}", query.web_query)

    url_list = list(
        search(
            query=query.web_query,
            stop=embeddings_article_limit,
            lang='en',
            safe='off',
            tbs=query.web_tbs,
            extra_params=query.web_extra_params))

    print(f"{Fore.CYAN}Web search completed.{Fore.RESET}")

    for url in url_list:
        documents = WebBaseLoader(url).load_and_split(RecursiveCharacterTextSplitter(
            separators=embeddings_buffer_stops,
            chunk_size=embeddings_chunk_size,
            chunk_overlap=embeddings_chunk_overlap,
            keep_separator=False,
            strip_whitespace=True))

        for document in documents:
            if is_text_junk(document.page_content):
                documents.remove(document)
                if len(documents) == 0:
                    continue

            document.page_content = remove(document.page_content, ['\n', '`'])
            document.page_content = (query.db_embedding_prefix +
                                     document.page_content +
                                     query.db_embedding_postfix)

        if len(documents) != 0:
            database.add_documents(documents=documents, embeddings=embeddings)

    db_name = embedding_model_safe_name + query.db_save_file_extension
    database.save_local(folder_path='store', index_name=db_name)

    print(f"{Fore.CYAN}Document vectorization completed.{Fore.RESET}")


def web_query_google_lookup(query: WebQuery, token_limit: int = 2048):
    db_name = embedding_model_safe_name + query.db_save_file_extension
    db = get_db_by_name(db_name, embeddings)

    populate_db_with_google_search(db, query)

    # return the document with the highest prompt similarity score (for now only browsing the first search result)
    embedding_vector = embeddings.embed_query(query.db_embed_query)
    docs_and_scores = db.similarity_search_by_vector(embedding_vector, k=round(token_limit / 64))

    print(f"{Fore.CYAN}Database search completed.{Fore.RESET}")

    return docs_to_context(docs_and_scores, token_limit)


