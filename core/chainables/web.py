from core.tools.scraper import web_query_google_lookup
from core.classes.query import WebQuery


def web_news_lookup(prompt_text: str):
    query = WebQuery('news', prompt_core=prompt_text)
    return web_query_google_lookup(query)


def web_wiki_lookup(prompt_text: str):
    query = WebQuery('wiki', prompt_core=prompt_text)
    return web_query_google_lookup(query)


def web_docs_lookup(prompt_text: str):
    query = WebQuery('docs', prompt_core=prompt_text)
    return web_query_google_lookup(query)
