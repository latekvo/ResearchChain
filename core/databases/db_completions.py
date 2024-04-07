from tinydb import TinyDB

db_name = "completions"
db_path = "../../store/data/{}.json".format(db_name)
db = TinyDB(db_path)

# no issues come to mind with this implementation
