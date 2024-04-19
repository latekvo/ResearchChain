import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-H",
    "--use-hugging-face",
    dest="use_hugging_face",
    action="store_true",
    help="Use Hugging Face as the model provider",
)
parser.add_argument(
    "-M",
    "--pick-model",
    type=str,
    dest="model_choice",
    choices=["default", "small", "large"],
    default="default",
    help="Select model configuration",
)

args = parser.parse_args()

USE_HUGGING_FACE = args.use_hugging_face
MODEL_CHOICE = args.model_choice
