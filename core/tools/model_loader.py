import torch
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from core.models.configurations import (
    llm_ollama_heavy,
    embedder_ollama_heavy,
    llm_hugging_face_heavy,
    embedder_hugging_face_heavy,
)


def load_model():
    use_ollama = True
    if use_ollama:
        return load_ollama_model()
    else:
        return load_hugging_face_model()


def load_ollama_model():
    llm = Ollama(model=llm_ollama_heavy.model_name)
    embeddings = OllamaEmbeddings(model=embedder_ollama_heavy.model_name)
    return llm, embeddings


def load_hugging_face_model():
    base_model_path = hf_hub_download(
        llm_hugging_face_heavy.model_file, filename=llm_hugging_face_heavy.model_name
    )
    # Instantiate model from downloaded file
    llm = Llama(
        model_path=base_model_path,
        n_ctx=16000,  # Context length to use
        torch_dtype=torch.float16,
    )
    embedder_model_path = hf_hub_download(
        embedder_hugging_face_heavy.model_file, filename=embedder_hugging_face_heavy.model_name
    )
    # Instantiate model from downloaded file
    embeddings = Llama(
        model_path=embedder_model_path,
        n_ctx=16000,  # Context length to use
        torch_dtype=torch.float16,
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
