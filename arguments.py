import argparse
from dataclasses import dataclass

from core.models.configuration_objects.embedder_configuration import (
    EmbedderConfiguration,
)
from core.models.configuration_objects.llm_configuration import LlmConfiguration

parser = argparse.ArgumentParser()

# todo: llm and embedder choices should not be fixed,
#       there should be an option to specify a custom config
parser.add_argument(
    "-L",
    "--llm-model",
    type=str,
    dest="llm_choice",
    choices=[
        "none",
        "ollama_medium",
        "ollama_small",
        "ollama_large",
        "hugging_face_medium",
        "hugging_face_small",
        "hugging_face_large",
    ],
    default="ollama_medium",
    help="Select llm model configuration",
)
parser.add_argument(
    "-E",
    "--embedder-model",
    type=str,
    dest="embed_choice",
    choices=[
        "none",
        "ollama_medium",
        "ollama_small",
        "ollama_large",
        "hugging_face_medium",
        "hugging_face_small",
        "hugging_face_large",
    ],
    default="ollama_medium",
    help="Select embedding model configuration",
)

# use config specified either by one of the configuration files or by a custom path
# idea behind this: user can either configure their workers by editing the config files,
#                   or by providing their own configs. One of these methods can be deleted,
#                   once we determine which is more useful for dockerized applications
parser.add_argument(
    "-w",
    "--run-worker",
    type=str,
    dest="worker_type",
    choices=[
        "none",  # legacy runner / custom worker path
        "crawler",
        "embedder",
        "summarizer",
    ],
    default="none",
    help="Select worker to run",
)
parser.add_argument(
    "-c",
    "--custom-worker-path",
    type=str,
    dest="worker_config_path",
    default="none",
    help="Specify worker config to run",
)

args = parser.parse_args()


@dataclass
class RuntimeConfiguration:
    worker_type: str
    worker_config_path: str
    llm_config_name: str
    embedder_config_name: str
    llm_config: LlmConfiguration
    embedder_config: EmbedderConfiguration


def get_runtime_config():
    llm_path = "core/models/configurations/llm/{}.json".format(args.llm_choice)
    embed_path = "core/models/configurations/embeder/{}.json".format(args.embed_choice)

    llm_config = LlmConfiguration(llm_path)
    embedder_config = EmbedderConfiguration(embed_path)

    # hf or ollama (compatibility)
    llm_supplier = llm_config.supplier
    embedder_supplier = embedder_config.supplier

    # todo: we should actually allow for this behaviour, should be a simple fix as well
    if llm_supplier != embedder_supplier:
        raise ValueError(
            "LLM and EMBEDDER suppliers differ, please use the same supplier for both."
        )

    worker_config_path = "configs/{}.json".format(args.worker_type)

    # todo: load one of the standard configs based on worker_type, and overlay flags atop
    return RuntimeConfiguration(
        worker_type=args.worker_type,
        worker_config_path=worker_config_path,
        llm_config_name=args.llm_choice,
        embedder_config_name=args.embed_choice,
        llm_config=llm_config,
        embedder_config=embedder_config,
    )
