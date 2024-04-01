from core.tools.utils import purify_name
from model_loader import load_base_ollama_model
from model_loader import load_embeddings_ollama_model

# TODO: move hardcoded values from here and from embeddings.py into a standalone configuration file, preferably yaml
MODEL_NAME = "mixtral:8x7b-instruct-v0.1-q5_K_M"  # "llama2-uncensored:7b"
MODEL_SAFE_NAME = purify_name(MODEL_NAME)
MODEL_TOKEN_LIMIT = 30720  # depending on VRAM, try 2048, 3072 or 4096. 2048 works great on 4GB VRAM

# adjust depending on how fast 'database vectorization' runs [3 - 100]
EMBEDDINGS_ARTICLE_LIMIT = 10  # fixme: wikipedia doesn't like high article limit (>5)
EMBEDDINGS_BUFFER_STOPS = ["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""]  # N of elements LTR [4 - 7]
EMBEDDINGS_CHUNK_OVERLAP = 200
EMBEDDINGS_MODEL_TOKEN_LIMIT = 4096
EMBEDDING_MODEL_NAME = "nomic-embed-text"  # this is not a good model, change asap
EMBEDDING_MODEL_SAFE_NAME = purify_name(EMBEDDING_MODEL_NAME)

llm = load_base_ollama_model(MODEL_NAME)
embeddings = load_embeddings_ollama_model(EMBEDDING_MODEL_NAME)
