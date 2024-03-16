from langchain_community.llms.ollama import Ollama

from core.tools.utils import purify_name

model_name = "zephyr:7b-beta-q5_K_M"  # "llama2-uncensored:7b"
model_safe_name = purify_name(model_name)
token_limit = 2048  # depending on VRAM, try 2048, 3072 or 4096. 2048 works great on 4GB VRAM

llm = Ollama(model=model_name)
