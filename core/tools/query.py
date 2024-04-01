import datetime
from typing import Literal, Union


class WebQuery:
    """class for bundling all data required for embedding and search operations"""
    query_type: Literal['wiki', 'news', 'docs']

    prompt_core: str = ''

    web_query: str = ''
    web_extra_params: Union[dict, None] = None
    web_tbs = 0

    db_search_query: str = ''  # query to search by
    db_embedding_prefix: str = ''  # prefixed to each article saved to faiss db
    db_embedding_postfix: str = ''  # -||-
    db_save_file_extension: str = ''  # most types will have dedicated db for them
    db_chunk_size: int = 600  # legacy default

    def __init__(self, query_type: Literal['wiki', 'news', 'docs'], prompt_core: str):
        self.query_type = query_type
        self.prompt_core = prompt_core
        self.db_embed_query = prompt_core  # query to search by

        if query_type == 'wiki':
            self.web_query = 'wikipedia ' + prompt_core
            self.db_save_file_extension = '_facts'
            self.db_chunk_size = 400


        elif query_type == 'news':
            # this prompt works well for Google News searches
            self.web_query = f"{prompt_core} news comprehensive overview "
            self.web_extra_params = {
                'tbm': 'nws',  # news only
            }
            self.web_tbs = 'qdr:m'  # last month only
            self.db_search_query = f"{prompt_core} news and innovations"
            self.db_save_file_extension = f"_news_{datetime.date.today().strftime('%Y_%m_%d').lower()}"
            self.db_chunk_size = 1000


        elif query_type == 'docs':
            self.web_query = 'documentation ' + prompt_core
            self.db_save_file_extension = "_docs"
            self.db_chunk_size = 600
