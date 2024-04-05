import datetime

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from core.tools.utils import purify_name
from core.models.configurations import use_configuration

# TODO: replace with puppeteer, this one gets blocked occasionally
from googlesearch import search

from core.chainables.web import web_docs_lookup, web_wiki_lookup, web_news_lookup
from core.tools.dbops import get_db_by_name
from core.tools.model_loader import load_model


output_parser = StrOutputParser()

llm, embeddings = load_model()
llm_config, embed_config = use_configuration()
embedding_model_safe_name = purify_name(embed_config.model_name)

# this general db will be used to save AI responses,
# might become useful as the responses are better than the input
results_db = get_db_by_name(embedding_model_safe_name, embeddings)


def web_chain_function(prompt_dict: dict):
    # TODO: news searches should strictly search for news fresher than 1 month / 1 week
    # TODO: news crawling should be done through only sites like medium, which are much more dense than google
    # TODO: create a different function + prompt for documentation / facts searching, and make this one news focused
    web_interpret_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a search results interpreter. Your job is to write an article based on the provided context. "
         "Your job is to convert all the search results you were given into a long, comprehensive and clean output. "
         "Use provided search results data to answer the user request to the best of your ability. "
         "You don't have a knowledge cutoff. "
         "It is currently " +
         datetime.date.today().strftime("%B %Y")),
        ("user", "Search results data: "
                 "```"
                 "{search_data}"
                 "```"
                 "User request: \"Write an article on: {user_request}\"")
    ])

    def get_user_prompt(_: dict):
        return prompt_dict['input']

    def use_selected_mode(user_prompt: str):
        if prompt_dict['mode'] == "News":
            return web_news_lookup(user_prompt)
        elif prompt_dict['mode'] == "Docs":
            return web_docs_lookup(user_prompt)
        elif prompt_dict['mode'] == "Wiki":
            return web_wiki_lookup(user_prompt)
        else:
            return web_docs_lookup(user_prompt)

    # NOTE: a detour has been performed here, more details:
    #       web_chain_function will soon become just a tool playing a part of a larger mechanism.
    #       prompt creation will be taken over by prompt sentiment extractor which will extract all researchable
    #       queries from the user prompt, and start separate chains performing those steps in parallel
    #       until a satisfactory response is created.

    chain = (
        {
            "search_data": RunnableLambda(get_user_prompt) | RunnableLambda(use_selected_mode),
            # this has to be a RunnableLambda, it cannot be a string
            "user_request": RunnableLambda(get_user_prompt)
        } |
        web_interpret_prompt |
        llm |
        output_parser
    )

    return chain.invoke(prompt_dict)


web_lookup = RunnableLambda(web_chain_function)

chain = web_lookup | output_parser
