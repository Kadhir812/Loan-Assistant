from langchain_openai import ChatOpenAI

from chains.response_chain import (
    create_response_chain
)

llm = ChatOpenAI( model="gpt-5.6-luna", reasoning_effort="none" )

response_chain = (
    create_response_chain(
        llm
    )
)

def generate_response(
    query: str,
    customer_profile: dict,
    retrieved_context: list
) -> str:

    result = response_chain.invoke(
        {
            "query":
                query,

            "customer_profile":
                customer_profile,

            "retrieved_context":
                retrieved_context
        }
    )

    return result.content