from langchain_community.embeddings import OllamaEmbeddings

from core.tools.utils import purify_name

embeddings_chunk_size = 600  # it is not recommended to play with this value, [100 - 600]
embeddings_article_limit = 50  # adjust depending on how fast 'database vectorization' runs [3 - 100]
embeddings_buffer_stops = ["\n\n\n", "\n\n", "\n", ". ", ", ", " ", ""]  # N of elements LTR [4 - 7]
embeddings_chunk_overlap = 200

embedding_model_name = "nomic-embed-text"  # this is not a good model, change asap
embedding_model_safe_name = purify_name(embedding_model_name)

embeddings = OllamaEmbeddings(model=embedding_model_name)