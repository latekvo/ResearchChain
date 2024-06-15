from os.path import exists

from langchain_community.vectorstores.faiss import FAISS
from langchain_core.embeddings import Embeddings


def create_faiss_db_if_not_exists(
    db_name: str, folder_path: str, embeddings: Embeddings
):
    if not exists(folder_path + "/" + db_name + ".faiss"):
        print("Creating new database:", db_name + ".faiss")
        tmp_db = FAISS.from_texts(
            ["You are a large language model, intended for research purposes."],
            embeddings,
        )
        print("aaa: ", folder_path, db_name)
        tmp_db.save_local(folder_path=folder_path, index_name=db_name)
    else:
        print("Already exists:", db_name + ".faiss")


def get_vec_db_by_name(db_name: str, embeddings: Embeddings) -> FAISS:
    folder_path = "store/vector"

    create_faiss_db_if_not_exists(db_name, folder_path, embeddings)

    try:
        # windows
        db_connection = FAISS.load_local(
            folder_path=folder_path,
            embeddings=embeddings,
            index_name=db_name,
            allow_dangerous_deserialization=True,
        )
    except Exception:
        # linux & mac
        db_connection = FAISS.load_local(
            folder_path=folder_path,
            embeddings=embeddings,
            index_name=db_name,
            allow_dangerous_deserialization=True,
        )

    return db_connection
