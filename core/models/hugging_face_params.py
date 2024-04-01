from core.tools.utils import purify_name
from model_loader import load_huging_face_model

# TODO: move hardcoded values from here and from embeddings.py into a standalone configuration file, preferably yaml
MODEL_NAME = "TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF"
MODEL_FILE = "mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf"
MODEL_SAFE_NAME = purify_name(MODEL_NAME)
MODEL_TOKEN_LIMIT = 30720  # depending on VRAM, try 2048, 3072 or 4096. 2048 works great on 4GB VRAM

llm = load_huging_face_model(MODEL_NAME, MODEL_FILE)
