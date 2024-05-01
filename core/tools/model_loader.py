from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

from arguments import USE_HUGGING_FACE
from core.models.configurations import load_llm_config

llm_config, embed_config = load_llm_config()


def load_ollama_model():
    llm = Ollama(model=llm_config.model_name)
    embeddings = OllamaEmbeddings(model=embed_config.model_name)
    return llm, embeddings


def load_hugging_face_model():
    # todo: for this to be error-proof, we have to cache returns as singletons, and serve them
    base_model_path = hf_hub_download(
        llm_config.model_file, filename=llm_config.model_name
    )
    # Instantiate model from downloaded file
    llm = Llama(
        model_path=base_model_path,
        n_gpu_layers=-1,
        n_batch=llm_config.model_token_limit,
        verbose=True,
    )
    embedder_model_path = hf_hub_download(
        embed_config.model_file, filename=embed_config.model_name
    )
    # Instantiate model from downloaded file
    embeddings = Llama(
        model_path=embedder_model_path,
        n_gpu_layers=-1,
        n_batch=embed_config.model_token_limit,
        verbose=True,
    )

    return llm, embeddings


def load_model():
    if USE_HUGGING_FACE:
        return load_hugging_face_model()
    else:
        return load_ollama_model()
