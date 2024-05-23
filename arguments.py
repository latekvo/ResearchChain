import argparse

from core.models.configuration_objects.embedder_configuration import (
    EmbedderConfiguration,
)
from core.models.configuration_objects.llm_configuration import LlmConfiguration

parser = argparse.ArgumentParser()

parser.add_argument(
    "-M",
    "--llm-model",
    type=str,
    dest="llm_choice",
    choices=[
        "ollama_medium",
        "ollama_small",
        "ollama_large",
        "hugging_face_medium",
        "hugging_face_small",
        "hugging_face_large",
    ],
    default="ollama_medium",
    help="Select model configuration",
)
parser.add_argument(
    "-M",
    "--embedder-model",
    type=str,
    dest="embedder_choice",
    choices=[
        "ollama_medium",
        "ollama_small",
        "ollama_large",
        "hugging_face_medium",
        "hugging_face_small",
        "hugging_face_large",
    ],
    default="ollama_medium",
    help="Select model configuration",
)
parser.add_argument(
    "-w",
    "--run-worker",
    type=str,
    dest="worker_type",
    choices=[
        "none",  # legacy runner, todo: to be removed
        "crawler",
        "embedder",
        "summarizer",
    ],
    default="none",
    help="Select worker to run",
)

args = parser.parse_args()

llm_path = "core/models/configurations/llm/{}.json".format(args.llm_choice)
embed_path = "core/models/configurations/embeder/{}.json".format(args.embedder_choice)
llm_config = LlmConfiguration(llm_path)
embedder_config = EmbedderConfiguration(embed_path)

# hf or ollama (compatibility)
llm_supplier = llm_config.supplier
embedder_supplier = embedder_config.supplier

if llm_supplier != embedder_supplier:
    # todo: we should actually allow for this behaviour, should be a simple fix as well
    raise ValueError(
        "LLM and EMBEDDER suppliers differ, please use the same supplier for both."
    )

LLM_CHOICE = args.llm_choice
EMBEDDER_CHOICE = args.embedder_choice
USE_HUGGING_FACE = llm_supplier == "hugging_face"


def get_running_config():
    return {
        "worker_type": args.worker_type,
        "llm_config_name": args.llm_choice,
        "embedder_config_name": args.embedder_choice,
        "llm_config": llm_config,
        "embedder_config": embedder_config,
    }
