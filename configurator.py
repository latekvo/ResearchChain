import argparse
from dataclasses import dataclass

from colorama import Fore, Style

from core.classes.configuration import (
    RuntimeConfiguration,
    load_runtime_config_from_file,
)
from core.models.configuration_objects.embedder_configuration import (
    EmbedderConfiguration,
)
from core.models.configuration_objects.llm_configuration import LlmConfiguration
from core.tools import errorlib

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
    "ollama_medium, "
    "ollama_small, "
    "ollama_large, "
    "hugging_face_medium, "
    "hugging_face_small, "
    "hugging_face_large, ",
    default="none",
)
parser.add_argument(
    "-E",
    "--embedder-model",
    type=str,
    dest="embed_choice",
    help="Select embedding model configuration. "
    "Out of the box choices include: "
    "ollama_medium, "
    "ollama_small, "
    "ollama_large, "
    "hugging_face_medium, "
    "hugging_face_small, "
    "hugging_face_large, ",
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

    try:
        runtime_config = load_runtime_config_from_file(worker_config_path)
    except FileNotFoundError:
        # this error format deserves its own tiny library :3
        errorlib.pretty_error(
            title="No valid configuration was selected",
            advice=f"Try setting the {Fore.CYAN}-w{Fore.RESET} flag",
        )

    llm_path = "core/models/configurations/llm/{}.json".format(args.llm_choice)
    embed_path = "core/models/configurations/embeder/{}.json".format(args.embed_choice)

    # set x_config_name
    if args.worker_type != "none":
        runtime_config.worker_type = args.worker_type
    if args.llm_choice != "none":
        runtime_config.llm_config_name = args.llm_choice
    if args.embed_choice != "none":
        runtime_config.embedder_config_name = args.embed_choice

    # check if x_configs are available
    llm_config_available = runtime_config.llm_config_name != "none"
    embedder_config_available = runtime_config.embedder_config_name != "none"

    # generate x_config
    if runtime_config.llm_config is None and llm_config_available:
        runtime_config.llm_config = LlmConfiguration(llm_path)
    if runtime_config.embedder_config is None and embedder_config_available:
        runtime_config.embedder_config = EmbedderConfiguration(embed_path)

    return runtime_config
