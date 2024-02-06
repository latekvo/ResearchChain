from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = Ollama(model="llama2-uncensored:7b")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a researching assistant."),
    ("user", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

output_text = chain.invoke({"input": "How can LLMs help with research?"})

print(output_text)