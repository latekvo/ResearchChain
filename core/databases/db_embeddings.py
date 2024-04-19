from core.tools.utils import use_faiss

vector_db = use_faiss("embeddings", "placeholder")

# this global db has to actually be a set of multiple
# separate dbs, each associated with its own embed model

# this file will be populated in a separate PR, along with an embedding server
