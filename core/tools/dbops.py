from os.path import exists

from langchain_community.vectorstores.faiss import FAISS
from langchain_core.embeddings import Embeddings


def create_db_if_not_exists(db_name: str, embeddings: Embeddings):
    if not exists("store/vector/" + db_name + ".faiss"):
        print("Creating new database:", db_name + ".faiss")
        tmp_db = FAISS.from_texts(
            ["You are a large language model, intended for research purposes."],
            embeddings,
        )
        tmp_db.save_local(folder_path="store/vector", index_name=db_name)
    else:
        print("Already exists:", db_name + ".faiss")


def get_db_by_name(db_name: str, embeddings: Embeddings) -> FAISS:
    create_db_if_not_exists(db_name, embeddings)

    try:
        # windows
        db_connection = FAISS.load_local(
            folder_path="store/vector",
            embeddings=embeddings,
            index_name=db_name,
            allow_dangerous_deserialization=True,
        )
    except Exception:
        # linux & mac
        db_connection = FAISS.load_local(
            folder_path="store/vector", embeddings=embeddings, index_name=db_name
        )

    return db_connection
