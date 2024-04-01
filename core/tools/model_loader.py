from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import torch
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama


def load_base_ollama_model(MODEL_NAME: str):
    llm = Ollama(model=MODEL_NAME)
    return llm

def load_embeddings_ollama_model(EMBEDDING_MODEL_NAME: str):
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
    return embeddings

def load_huging_face_model(MODEL_NAME: str, MODEL_FILE: str):
    model_path = hf_hub_download(MODEL_NAME, filename=MODEL_FILE)
    ## Instantiate model from downloaded file
    llm = Llama(
        model_path=model_path,
        n_ctx=16000,  # Context length to use
        torch_dtype=torch.float16,
    )

    ## Generation kwargs
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
    return llm
