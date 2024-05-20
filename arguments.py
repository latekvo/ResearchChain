# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument(
#     "-H",
#     "--use-hugging-face",
#     dest="use_hugging_face",
#     action="store_true",
#     help="Use Hugging Face as the model provider",
# )
# parser.add_argument(
#     "-M",
#     "--pick-model",
#     type=str,
#     dest="model_choice",
#     choices=[
#         "ollama_medium",
#         "ollama_small",
#         "ollama_large",
#         "hugging_face_medium",
#         "hugging_face_small",
#         "hugging_face_large",
#     ],
#     default="ollama_medium",
#     help="Select model configuration",
# )

# args = parser.parse_args()

USE_HUGGING_FACE = True
MODEL_CHOICE = "ollama_medium"
#TODO: Handle the arguments parsing
