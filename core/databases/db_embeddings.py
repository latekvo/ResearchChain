from tinydb import TinyDB

db_name = "embeddings"
db_path = "../../store/data/{}.json".format(db_name)
db = TinyDB(db_path)

# this global db has to actually be a set of multiple
# separate dbs, each associated with its own embed model

# this file will be populated in a separate PR, along with an embedding server
