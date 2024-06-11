from __future__ import annotations

from typing import Union

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llama_cpp import Llama

from configurator import get_runtime_config
from core.tools.utils import use_faiss, is_text_junk

runtime_configuration = get_runtime_config()
llm_config = runtime_configuration.llm_config
embedder_config = runtime_configuration.embedder_config

# fixme: these cause linter errors, i don't like this code overall,
#        but i had to quickly find a solution to file-scope execution
vector_db: FAISS | None = None
embedder: Union[OllamaEmbeddings, Llama] | None = None
text_splitter: RecursiveCharacterTextSplitter | None = None

# todo: we've changed every other db to Postgres, but here, we'll have to use 'FAISS server'


def first_use_init():
    global vector_db, embedder, text_splitter
    if vector_db is None:
        vector_db, embedder = use_faiss("embeddings")

    if text_splitter is None:
        text_splitter = RecursiveCharacterTextSplitter(
            separators=embedder_config.buffer_stops,
            chunk_size=embedder_config.model_token_limit,
            chunk_overlap=embedder_config.chunk_overlap,
            keep_separator=False,
            strip_whitespace=True,
        )


def db_get_currently_used_vector_model():
    return embedder_config.model_name


def db_add_text_batch(text: str, db_full_name: str):
    first_use_init()

    # automatically splits text before embedding it
    chunks = text_splitter.split_text(text)

    for chunk in chunks:
        if is_text_junk(chunk):
            chunks.remove(chunk)
            continue

    if len(chunks) != 0:
        vector_db.add_texts(texts=chunks, embeddings=embedder)

    vector_db.save_local(folder_path="store/vector", index_name=db_full_name)

    pass


def db_search_for_similar_queries(query):
    first_use_init()

    docs = vector_db.similarity_search(query)
    return docs
