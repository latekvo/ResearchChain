import datetime
from langchain_core.prompts import ChatPromptTemplate


def web_docs_lookup_prompt():
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a search results interpreter."
                "Your job is to write an detailed instruction based on the provided context. "
                "Your job is to convert all the search results you were given into a long, "
                "comprehensive and clean output. "
                "Use context data to explain "
                "the topic of user request to the best of your ability. "
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
        ]
    )


def web_wiki_lookup_prompt():
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a search results interpreter. "
                "Your job is to write an article based on the provided context. "
                "Your job is to convert all the search results you were given into a long, "
                "comprehensive and clean output. "
                "Use context data to answer "
                "the user request to the best of your ability. "
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
        ]
    )


def web_news_lookup_prompt():
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a search results interpreter. "
                "Your job is to write an article based on the provided context. "
                "Your job is to convert all the search results you were given into a long, "
                "comprehensive and clean output. "
                "Use provided context to answer the user request to the best of your ability. "
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
        ]
    )
