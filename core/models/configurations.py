from core.models.configuration_objects.llm_configuration import LlmConfiguration
from core.models.configuration_objects.embedder_configuration import (
    EmbedderConfiguration,
)
from terminal_gui import USE_HUGGING_FACE

llm_ollama_heavy = LlmConfiguration(
    supplier="ollama",
    model_name="zephyr:7b-beta-q5_K_M",
    model_token_limit=4096,
    model_file="",
)

embedder_ollama_heavy = EmbedderConfiguration(
    supplier="ollama",
    model_name="nomic-embed-text",
    model_token_limit=4096,
    # chunk spliter options
    article_limit=10,
    buffer_stops=["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""],
    chunk_overlap=200,
)

llm_hugging_face_heavy = LlmConfiguration(
    supplier="hugging_face",
    model_name="mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf",
    model_file="TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF",
    model_token_limit=30720,
)

embedder_hugging_face_heavy = EmbedderConfiguration(
    supplier="hugging_face",
    model_name="nomic-embed-text-v1.5.Q6_K.gguf",
    model_file="nomic-ai/nomic-embed-text-v1.5-GGUF",
    model_token_limit=4096,
    # chunk spliter options
    article_limit=10,
    buffer_stops=["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""],
    chunk_overlap=200,
)


def use_configuration():
    if USE_HUGGING_FACE:
        return llm_hugging_face_heavy, embedder_hugging_face_heavy
    else:
        return llm_ollama_heavy, embedder_ollama_heavy
