from arguments import LLM_CHOICE, EMBEDDER_CHOICE
from core.models.configuration_objects.llm_configuration import LlmConfiguration
from core.models.configuration_objects.embedder_configuration import (
    EmbedderConfiguration,
)


def load_llm_config():
    # fixme: this cannot really be an absolute path like this,
    #        users must be able to specify their own path in some way
    llm_path = "core/models/configurations/llm/{}.json".format(LLM_CHOICE)
    embed_path = "core/models/configurations/embeder/{}.json".format(EMBEDDER_CHOICE)
    llm_config = LlmConfiguration(llm_path)
    embed_config = EmbedderConfiguration(embed_path)
    return llm_config, embed_config
