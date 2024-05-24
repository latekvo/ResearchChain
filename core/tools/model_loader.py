from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

from arguments import get_runtime_config

runtime_configuration = get_runtime_config()
llm_config = runtime_configuration.llm_config
embedder_config = runtime_configuration.embedder_config

# todo: for this to be memory efficient,
#       we have to cache returns as singletons, and serve them
# problem with the caching requests above: we have to share those singletons across instances

# fixme: n_gpu_layers=-1 is a poor approach, it can and will cause crashes.
#        with llama.cpp we have to manually calculate and set this number


def load_ollama_llm():
    return Ollama(model=llm_config.model_name)


def load_ollama_embedder():
    return OllamaEmbeddings(model=embedder_config.model_name)


def load_ollama_model():
    return load_ollama_llm(), load_ollama_embedder()


def load_hf_llm():
    base_model_path = hf_hub_download(
        llm_config.model_file, filename=llm_config.model_name
    )
    return Llama(
        model_path=base_model_path,
        n_gpu_layers=-1,
        n_batch=llm_config.model_token_limit,
        verbose=True,
    )


def load_hf_embedder():
    embedder_model_path = hf_hub_download(
        embedder_config.model_file, filename=embedder_config.model_name
    )
    return Llama(
        model_path=embedder_model_path,
        n_gpu_layers=-1,
        n_batch=embedder_config.model_token_limit,
        verbose=True,
    )


def load_hugging_face_model():
    return load_hf_llm(), load_hf_embedder()


def load_model():
    # todo: split up into separate llm and embedder functions
    if llm_config.supplier == "hugging_face":
        return load_hugging_face_model()
    else:
        return load_ollama_model()


def load_llm():
    if llm_config.supplier == "hugging_face":
        return load_hf_llm()
    else:
        return load_ollama_llm()


def load_embedder():
    if embedder_config.supplier == "hugging_face":
        return load_hf_embedder()
    else:
        return load_ollama_embedder()
