from langchain_community.embeddings import OllamaEmbeddings

from core.tools.utils import purify_name

# it is not recommended to play with this value, [100 - 600]
EMBEDDINGS_CHUNK_SIZE = 600
# adjust depending on how fast 'database vectorization' runs [3 - 100]
EMBEDDINGS_ARTICLE_LIMIT = 50
EMBEDDINGS_BUFFER_STOPS = ["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""]  # N of elements LTR [4 - 7]
EMBEDDINGS_CHUNK_OVERLAP = 200
EMBEDDINGS_MODEL_TOKEN_LIMIT = 4096
EMBEDDING_MODEL_NAME = "nomic-embed-text"  # this is not a good model, change asap
EMBEDDING_MODEL_SAFE_NAME = purify_name(EMBEDDING_MODEL_NAME)
embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
