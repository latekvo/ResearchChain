from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

from configurator import get_runtime_config

runtime_configuration = get_runtime_config()
llm_config = runtime_configuration.llm_config
embedder_config = runtime_configuration.embedder_config

# problem with the current caching: we have to share those singletons across instances

# fixme: n_gpu_layers=-1 is a poor approach, it can and will cause crashes.
#        with llama.cpp we have to manually calculate and set this number


def load_ollama_llm() -> Ollama:
    cached_llm = runtime_configuration.llm_object
    if cached_llm:
        return cached_llm
    else:
        llm = Ollama(model=llm_config.model_name)
        runtime_configuration.llm_object = llm
        return llm


def load_ollama_embedder() -> OllamaEmbeddings:
    cached_embedder = runtime_configuration.embedder_object
    if cached_embedder:
        return cached_embedder
    else:
        embedder = OllamaEmbeddings(model=embedder_config.model_name)
        runtime_configuration.embedder_object = embedder
        return embedder


def load_hf_llm():
    cached_llm = runtime_configuration.llm_object
    if cached_llm:
        return cached_llm
    else:
        base_model_path = hf_hub_download(
            llm_config.model_file, filename=llm_config.model_name
        )
        llm = Llama(
            model_path=base_model_path,
            n_gpu_layers=-1,
            n_batch=llm_config.model_token_limit,
            verbose=True,
        )
        runtime_configuration.llm_object = llm
        return llm


def load_hf_embedder():
    cached_embedder = runtime_configuration.embedder_object
    if cached_embedder:
        return cached_embedder
    else:
        embedder_model_path = hf_hub_download(
            embedder_config.model_file, filename=embedder_config.model_name
        )
        embedder = Llama(
            model_path=embedder_model_path,
            n_gpu_layers=-1,
            n_batch=embedder_config.model_token_limit,
            verbose=True,
        )
        runtime_configuration.embedder_object = embedder
        return embedder


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
