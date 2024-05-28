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


# this is a serializable singleton global configuration file


# global config, storage and caching object
@dataclass
class RuntimeConfiguration:
    worker_type: str
    worker_config_path: str
    llm_config_name: str
    embedder_config_name: str
    llm_config: LlmConfiguration
    embedder_config: EmbedderConfiguration
    llm_object: Ollama | Llama = None
    embedder_object: OllamaEmbeddings | Llama = None


def load_runtime_config_from_file(path: str):
    with open(path) as f:
        data = json.load(f)
        config = RuntimeConfiguration(
            worker_type=data["worker_type"],
            worker_config_path=data["worker_config_path"],
            llm_config_name=data["llm_config_name"],
            embedder_config_name=data["embedder_config_name"],
            # vvv - check if these save correctly, if not, remove
            llm_config=data["llm_config"],
            embedder_config=data["embedder_config"],
        )

        # todo: move logic regarding x_objects and x_configs here?

    return config
