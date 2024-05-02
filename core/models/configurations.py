from arguments import MODEL_CHOICE
from core.models.configuration_objects.llm_configuration import LlmConfiguration
from core.models.configuration_objects.embedder_configuration import (
    EmbedderConfiguration,
)


def load_llm_config():
    llm_path = "core/models/configurations/llm/{}.json".format(MODEL_CHOICE)
    embed_path = "core/models/configurations/embeder/{}.json".format(MODEL_CHOICE)
    llm_confing = LlmConfiguration(llm_path)
    embed_confing = EmbedderConfiguration(embed_path)
    return llm_confing, embed_confing
