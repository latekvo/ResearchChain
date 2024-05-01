from core.models.configuration_objects.llm_configuration import LlmConfiguration
from core.models.configuration_objects.embedder_configuration import (
    EmbedderConfiguration,
)

from arguments import USE_HUGGING_FACE, MODEL_CHOICE

llm_ollama_default = LlmConfiguration(
    supplier="ollama",
    model_name="zephyr:7b-beta-q5_K_M",
    model_token_limit=4096,
    model_file="",
)

embedder_ollama_default = EmbedderConfiguration(
    supplier="ollama",
    model_name="nomic-embed-text",
    model_token_limit=4096,
    # chunk spliter options
    article_limit=10,
    buffer_stops=["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""],
    chunk_overlap=200,
)

llm_hugging_face_default = LlmConfiguration(
    supplier="hugging_face",
    model_name="mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf",
    model_file="TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF",
    model_token_limit=30720,
)

embedder_hugging_face_default = EmbedderConfiguration(
    supplier="hugging_face",
    model_name="nomic-embed-text-v1.5.Q6_K.gguf",
    model_file="nomic-ai/nomic-embed-text-v1.5-GGUF",
    model_token_limit=4096,
    # chunk spliter options
    article_limit=10,
    buffer_stops=["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""],
    chunk_overlap=200,
)

llm_ollama_small = LlmConfiguration(
    supplier="ollama",
    model_name="zephyr:7b-beta-q3_K_M",
    model_token_limit=4096,
    model_file="",
)

embedder_ollama_small = EmbedderConfiguration(
    supplier="ollama",
    model_name="nomic-embed-text",
    model_token_limit=4096,
    # chunk spliter options
    article_limit=10,
    buffer_stops=["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""],
    chunk_overlap=200,
)

llm_hugging_face_small = LlmConfiguration(
    supplier="hugging_face",
    model_name="mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf",
    model_file="TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF",
    model_token_limit=30720,
)

embedder_hugging_face_small = EmbedderConfiguration(
    supplier="hugging_face",
    model_name="nomic-embed-text-v1.5.Q6_K.gguf",
    model_file="nomic-ai/nomic-embed-text-v1.5-GGUF",
    model_token_limit=4096,
    # chunk spliter options
    article_limit=10,
    buffer_stops=["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""],
    chunk_overlap=200,
)

llm_ollama_large = LlmConfiguration(
    supplier="ollama",
    model_name="mixtral:8x7b-instruct-v0.1-q5_K_M",
    model_token_limit=32768,
    model_file="",
)

embedder_ollama_large = EmbedderConfiguration(
    supplier="ollama",
    model_name="nomic-embed-text",
    model_token_limit=4096,
    # chunk spliter options
    article_limit=10,
    buffer_stops=["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""],
    chunk_overlap=200,
)

llm_hugging_face_large = LlmConfiguration(
    supplier="hugging_face",
    model_name="mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf",
    model_file="TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF",
    model_token_limit=30720,
)

embedder_hugging_face_large = EmbedderConfiguration(
    supplier="hugging_face",
    model_name="nomic-embed-text-v1.5.Q6_K.gguf",
    model_file="nomic-ai/nomic-embed-text-v1.5-GGUF",
    model_token_limit=4096,
    # chunk spliter options
    article_limit=10,
    buffer_stops=["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""],
    chunk_overlap=200,
)

# todo: urgent, move all configs to separate default_hf, default_ollama, large_hf ... files,
#       make them json files, and add fromJson() to LlmConfiguration & EmbedderConfiguration


def get_model_by_choice():
    if MODEL_CHOICE == "default":
        return (
            llm_ollama_default,
            embedder_ollama_default,
            llm_hugging_face_default,
            embedder_hugging_face_default,
        )
    if MODEL_CHOICE == "small":
        return (
            llm_ollama_small,
            embedder_ollama_small,
            llm_hugging_face_small,
            embedder_hugging_face_small,
        )
    if MODEL_CHOICE == "large":
        return (
            llm_ollama_large,
            embedder_ollama_large,
            llm_hugging_face_large,
            embedder_hugging_face_large,
        )


def use_configuration():
    llm_ollama, embedder_ollama, llm_hugging_face, embedder_hugging_face = (
        get_model_by_choice()
    )

    if USE_HUGGING_FACE:
        return llm_hugging_face, embedder_hugging_face
    else:
        return llm_ollama, embedder_ollama
