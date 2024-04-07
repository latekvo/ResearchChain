import torch
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from terminal_gui import USE_HUGGING_FACE
from core.models.configurations import use_configuration
llm_config, embed_config = use_configuration()


def load_model():
    if USE_HUGGING_FACE:
        return load_hugging_face_model()
    else:
        return load_ollama_model()


def load_ollama_model():
    llm = Ollama(model=llm_config.model_name)
    embeddings = OllamaEmbeddings(model=embed_config.model_name)
    return llm, embeddings


def load_hugging_face_model():
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
    # Generation kwargs
    # generation_kwargs = {
    #     "max_tokens": 20000,
    #     "stop": ["</s>"],
    #     "echo": False,  # Echo the prompt in the output
    #     "top_k": 1,  # This is essentially greedy decoding, since the model will always return the highest-probability token. Set this value > 1 for sampling decoding
    # }

    # ## Run inference
    # prompt = "The meaning of life is "
    # res = llm(prompt, **generation_kwargs)  # Res is a dictionary

    # ## Unpack and the generated text from the LLM response dictionary and print it
    # print(res["choices"][0]["text"])
    # # res is short for result
    return llm, embeddings
