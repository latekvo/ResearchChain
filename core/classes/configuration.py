from __future__ import annotations

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
