import datetime

from core.tools.scraper import web_query_google_lookup
from core.classes.query import WebQuery
from langchain_core.prompts import ChatPromptTemplate




def web_news_lookup(prompt_text: str):
    query = WebQuery('news', prompt_core=prompt_text)
    return web_query_google_lookup(query)


def web_wiki_lookup(prompt_text: str):
    query = WebQuery('wiki', prompt_core=prompt_text)
    return web_query_google_lookup(query)


def web_docs_lookup(prompt_text: str):
    query = WebQuery('docs', prompt_core=prompt_text)
    return web_query_google_lookup(query)


def web_docs_lookup_prompt():
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a search results interpreter. Your job is to write an article based on the provided context. "
            "Your job is to convert all the search results you were given into a long, comprehensive and clean output. "
            "Use provided search results data to answer the user request to the best of your ability. "
            "You don't have a knowledge cutoff. "
            "It is currently " + datetime.date.today().strftime("%B %Y"),
        ),
        (
            "user",
            "Search results data: "
            "```"
            "{search_data}"
            "```"
            'User request: "Write an article on: {user_request}"',
        ),
    ])


def web_wiki_lookup_prompt():
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a search results interpreter. Your job is to write an article based on the provided context. "
            "Your job is to convert all the search results you were given into a long, comprehensive and clean output. "
            "Use provided search results data to answer the user request to the best of your ability. "
            "You don't have a knowledge cutoff. "
            "It is currently " + datetime.date.today().strftime("%B %Y"),
        ),
        (
            "user",
            "Search results data: "
            "```"
            "{search_data}"
            "```"
            'User request: "Write an article on: {user_request}"',
        ),
    ])


def web_news_lookup_prompt():
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a search results interpreter. Your job is to write an article based on the provided context. "
            "Your job is to convert all the search results you were given into a long, comprehensive and clean output. "
            "Use provided search results data to answer the user request to the best of your ability. "
            "You don't have a knowledge cutoff. "
            "It is currently " + datetime.date.today().strftime("%B %Y"),
        ),
        (
            "user",
            "Search results data: "
            "```"
            "{search_data}"
            "```"
            'User request: "Write an article on: {user_request}"',
        ),
    ])