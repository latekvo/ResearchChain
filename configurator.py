import argparse
from dataclasses import dataclass

from core.classes.configuration import (
    RuntimeConfiguration,
    load_runtime_config_from_file,
)
from core.models.configuration_objects.embedder_configuration import (
    EmbedderConfiguration,
)
from core.models.configuration_objects.llm_configuration import LlmConfiguration

parser = argparse.ArgumentParser()

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
    help="Select one of the ready worker configs to be used",
)
parser.add_argument(
    "-c",
    "--custom-worker-path",
    type=str,
    dest="worker_config_path",
    default="none",
    help="Specify a relative path to the worker config file",
)
parser.add_argument(
    "-L",
    "--llm-model",
    type=str,
    dest="llm_choice",
    help="Select generative model configuration.\n"
    "Out of the box choices include:\n"
    "- ollama_medium\n"
    "- ollama_small\n"
    "- ollama_large\n"
    "- hugging_face_medium\n"
    "- hugging_face_small\n"
    "- hugging_face_large\n",
    default="none",
)
parser.add_argument(
    "-E",
    "--embedder-model",
    type=str,
    dest="embed_choice",
    help="Select embedding model configuration.\n"
    "Out of the box choices include:\n"
    "- ollama_medium\n"
    "- ollama_small\n"
    "- ollama_large\n"
    "- hugging_face_medium\n"
    "- hugging_face_small\n"
    "- hugging_face_large\n",
    default="none",
)

args = parser.parse_args()

runtime_config = None


def get_runtime_config():
    global runtime_config

    # fetch cache
    if runtime_config:
        return runtime_config

    # default path
    worker_config_path = "configs/{}.json".format(args.worker_type)

    if args.worker_config_path != "none":
        worker_config_path = args.worker_config_path
        runtime_config.worker_config_path = worker_config_path

    runtime_config = load_runtime_config_from_file(worker_config_path)

    llm_path = "core/models/configurations/llm/{}.json".format(args.llm_choice)
    embed_path = "core/models/configurations/embeder/{}.json".format(args.embed_choice)

    if args.worker_type != "none":
        runtime_config.worker_type = args.worker_type
    if args.llm_choice != "none":
        runtime_config.llm_config_name = args.llm_choice
    if args.llm_choice != "none":
        runtime_config.embedder_config_name = args.embed_choice

    if runtime_config.llm_config is None:
        llm_config = LlmConfiguration(llm_path)
        runtime_config.llm_config = llm_config
    if runtime_config.embedder_config is None:
        embedder_config = EmbedderConfiguration(embed_path)
        runtime_config.embedder_config = embedder_config

    return runtime_config
