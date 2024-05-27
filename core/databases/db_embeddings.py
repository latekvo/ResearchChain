from langchain_text_splitters import RecursiveCharacterTextSplitter

from configurator import get_runtime_config
from core.tools.utils import use_faiss, is_text_junk

runtime_configuration = get_runtime_config()
llm_config = runtime_configuration.llm_config
embedder_config = runtime_configuration.embedder_config

vector_db, embedder = use_faiss("embeddings")

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
    docs = vector_db.similarity_search(query)
    return docs
