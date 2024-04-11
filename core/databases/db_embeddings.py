import os

from tinydb import TinyDB

from core.databases import defaults

data_path = defaults.DATA_PATH
if not os.path.exists(data_path):
    os.makedirs(data_path)

db_name = "embeddings"
db_path = data_path + "{}.json".format(db_name)
db = TinyDB(db_path)

# this global db has to actually be a set of multiple
# separate dbs, each associated with its own embed model

# this file will be populated in a separate PR, along with an embedding server
