from langchain_community.llms.ollama import Ollama

from core.tools.utils import purify_name

# TODO: move hardcoded values from here and from embeddings.py into a standalone configuration file, preferably yaml
MODEL_NAME = "mixtral:8x7b-instruct-v0.1-q5_K_M"  # "llama2-uncensored:7b"
MODEL_SAFE_NAME = purify_name(MODEL_NAME)
MODEL_TOKEN_LIMIT = 30720  # depending on VRAM, try 2048, 3072 or 4096. 2048 works great on 4GB VRAM

llm = Ollama(model=MODEL_NAME)
