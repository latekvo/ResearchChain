from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

from arguments import USE_HUGGING_FACE, get_runtime_config

runtime_configuration = get_runtime_config()
llm_config = runtime_configuration.llm_config
embedder_config = runtime_configuration.embedder_config

# problem with the caching requests below: we have to share those singletons across instances


def load_ollama_model():
    # todo: w/ caching same here, use singletons to avoid crashes
    llm = Ollama(model=llm_config.model_name)
    embeddings = OllamaEmbeddings(model=embedder_config.model_name)
    return llm, embeddings


def load_hugging_face_model():
    # todo: for this to be memory efficient,
    #       we have to cache returns as singletons, and serve them

    base_model_path = hf_hub_download(
        llm_config.model_file, filename=llm_config.model_name
    )

    # fixme: n_gpu_layers=-1 is a poor approach, it can and will cause crashes.
    #        with llama.cpp we have to manually calculate and set this number
    llm = Llama(
        model_path=base_model_path,
        n_gpu_layers=-1,
        n_batch=llm_config.model_token_limit,
        verbose=True,
    )
    embedder_model_path = hf_hub_download(
        embedder_config.model_file, filename=embedder_config.model_name
    )
    # Instantiate model from downloaded file
    embeddings = Llama(
        model_path=embedder_model_path,
        n_gpu_layers=-1,
        n_batch=embedder_config.model_token_limit,
        verbose=True,
    )

    return llm, embeddings


def load_model():
    # todo: split up into separate llm and embedder functions
    if llm_config.supplier == "hugging_face":
        return load_hugging_face_model()
    else:
        return load_ollama_model()
