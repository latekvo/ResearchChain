from __future__ import annotations

import json
from dataclasses import dataclass

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from llama_cpp import Llama

from core.models.configuration_objects.embedder_configuration import (
    EmbedderConfiguration,
)
from core.models.configuration_objects.llm_configuration import LlmConfiguration


# global config, storage and caching object
@dataclass
class RuntimeConfiguration:
    worker_type: str
    worker_config_path: str
    llm_config_name: str
    embedder_config_name: str

    # set at runtime for now
    llm_config: LlmConfiguration = None
    embedder_config: EmbedderConfiguration = None
    llm_object: Ollama | Llama = None
    embedder_object: OllamaEmbeddings | Llama = None


def load_runtime_config_from_file(path: str):
    with open(path) as f:
        data = json.load(f)
        config = RuntimeConfiguration(
            worker_type=data["worker_type"],
            worker_config_path=path,
            llm_config_name=data["llm_config_name"],
            embedder_config_name=data["embedder_config_name"],
        )

        # todo: maybe move logic regarding x_objects and x_configs here?

    return config
