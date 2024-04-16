from core.models.configuration_objects.llm_configuration import LlmConfiguration
from core.models.configuration_objects.embedder_configuration import (
    EmbedderConfiguration,
)
from terminal_gui import USE_HUGGING_FACE, PICK_MODEL


def pick_model():
    if PICK_MODEL == "default":
        llm_ollama = LlmConfiguration(
            supplier="ollama",
            model_name="zephyr:7b-beta-q5_K_M",
            model_token_limit=4096,
            model_file="",
        )

        embedder_ollama = EmbedderConfiguration(
            supplier="ollama",
            model_name="nomic-embed-text",
            model_token_limit=4096,
            # chunk spliter options
            article_limit=10,
            buffer_stops=["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""],
            chunk_overlap=200,
        )

        llm_hugging_face = LlmConfiguration(
            supplier="hugging_face",
            model_name="mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf",
            model_file="TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF",
            model_token_limit=30720,
        )

        embedder_hugging_face = EmbedderConfiguration(
            supplier="hugging_face",
            model_name="nomic-embed-text-v1.5.Q6_K.gguf",
            model_file="nomic-ai/nomic-embed-text-v1.5-GGUF",
            model_token_limit=4096,
            # chunk spliter options
            article_limit=10,
            buffer_stops=["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""],
            chunk_overlap=200,
        )
    if PICK_MODEL == "small":
        llm_ollama = LlmConfiguration(
            supplier="ollama",
            model_name="zephyr:7b-beta-q3_K_M",
            model_token_limit=4096,
            model_file="",
        )

        embedder_ollama = EmbedderConfiguration(
            supplier="ollama",
            model_name="nomic-embed-text",
            model_token_limit=4096,
            # chunk spliter options
            article_limit=10,
            buffer_stops=["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""],
            chunk_overlap=200,
        )

        llm_hugging_face = LlmConfiguration(
            supplier="hugging_face",
            model_name="mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf",
            model_file="TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF",
            model_token_limit=30720,
        )

        embedder_hugging_face = EmbedderConfiguration(
            supplier="hugging_face",
            model_name="nomic-embed-text-v1.5.Q6_K.gguf",
            model_file="nomic-ai/nomic-embed-text-v1.5-GGUF",
            model_token_limit=4096,
            # chunk spliter options
            article_limit=10,
            buffer_stops=["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""],
            chunk_overlap=200,
        )
    if PICK_MODEL == "large":
        llm_ollama = LlmConfiguration(
            supplier="ollama",
            model_name="mixtral:8x7b-instruct-v0.1-q5_K_M",
            model_token_limit=32768,
            model_file="",
        )

        embedder_ollama = EmbedderConfiguration(
            supplier="ollama",
            model_name="nomic-embed-text",
            model_token_limit=4096,
            # chunk spliter options
            article_limit=10,
            buffer_stops=["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""],
            chunk_overlap=200,
        )

        llm_hugging_face = LlmConfiguration(
            supplier="hugging_face",
            model_name="mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf",
            model_file="TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF",
            model_token_limit=30720,
        )

        embedder_hugging_face = EmbedderConfiguration(
            supplier="hugging_face",
            model_name="nomic-embed-text-v1.5.Q6_K.gguf",
            model_file="nomic-ai/nomic-embed-text-v1.5-GGUF",
            model_token_limit=4096,
            # chunk spliter options
            article_limit=10,
            buffer_stops=["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""],
            chunk_overlap=200,
        )
    return llm_ollama, embedder_ollama, llm_hugging_face, embedder_hugging_face


def use_configuration():
    llm_ollama, embedder_ollama, llm_hugging_face, embedder_hugging_face = pick_model()
    if USE_HUGGING_FACE:
        return llm_hugging_face, embedder_hugging_face
    else:
        return llm_ollama, embedder_ollama
