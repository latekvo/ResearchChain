from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.models.configurations import use_configuration
from core.tools.model_loader import load_model
from core.tools.utils import use_faiss, is_text_junk, remove_characters

llm_config, embedder_config = use_configuration()
_, embedder = load_model()

vector_db = use_faiss("embeddings", embedder_config.model_name)

text_splitter = RecursiveCharacterTextSplitter(
    separators=embedder_config.buffer_stops,
    chunk_size=embedder_config.model_token_limit,
    chunk_overlap=embedder_config.chunk_overlap,
    keep_separator=False,
    strip_whitespace=True,
)


def db_add_text_batch(text: str, source_uuid: str):
    # automatically splits text before embedding it
    chunks = text_splitter.split_text(text)

    for chunk in chunks:
        if is_text_junk(chunk.page_content):
            chunks.remove(chunk)
            continue

        chunk.page_content = remove_characters(chunk.page_content, ["\n", "`"])
        chunk.page_content = chunk.page_content

    if len(chunks) != 0:
        vector_db.add_texts(documents=chunks, embeddings=embedder)

    pass
