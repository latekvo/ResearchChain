from core.tools.scraper import web_query_google_lookup
from core.tools.query import WebQuery

DEFAULT_NEWS_TOKEN_LIMIT = 1024
DEFAULT_WIKI_TOKEN_LIMIT = 256
DEFAULT_DOCS_TOKEN_LIMIT = 1024


def web_news_lookup(prompt_text: str):
    query = WebQuery('news', prompt_core=prompt_text)
    return web_query_google_lookup(query, DEFAULT_NEWS_TOKEN_LIMIT)


def web_wiki_lookup(prompt_text: str):
    query = WebQuery('wiki', prompt_core=prompt_text)
    return web_query_google_lookup(query, DEFAULT_WIKI_TOKEN_LIMIT)


def web_docs_lookup(prompt_text: str):
    query = WebQuery('docs', prompt_core=prompt_text)
    return web_query_google_lookup(query, DEFAULT_DOCS_TOKEN_LIMIT)
