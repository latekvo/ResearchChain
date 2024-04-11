from core.tools.utils import use_tinydb

db = use_tinydb("embeddings")


# this global db has to actually be a set of multiple
# separate dbs, each associated with its own embed model

# this file will be populated in a separate PR, along with an embedding server
