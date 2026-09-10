from langchain_core.prompts import ChatPromptTemplate

from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda
)

def format_profile( profile: dict ) -> str:

    if not profile:
        return "Customer profile unavailable."

    lines = []

    for key, value in profile.items():

        lines.append(
            f"{key}: {value}"
        )

    return "\n".join(lines)

def format_context( context: list ) -> str:

    if not context:
        return "No policy context retrieved."

    sections = []

    for chunk in context:

        source = chunk.get(
            "source",
            "Unknown"
        )

        page = chunk.get(
            "page",
            "Unknown"
        )

        section = chunk.get(
            "section",
            "Unknown"
        )

        content = chunk.get(
            "content",
            ""
        )

        formatted_chunk = f"""
            Source: {source}
            Page: {page}
            Section: {section}
            Content: {content}
            """

        sections.append(
            formatted_chunk.strip()
        )

    return "\n\n".join(
        sections
    )

def create_response_chain(llm):

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are Agent 1, the Response Agent for a
                Personal Loan Eligibility and Rejection Assistant.

                Your responsibility is to create an INITIAL answer.

                Use ONLY:

                1. Customer Profile
                2. Retrieved Personal Loan Policy

                Rules:

                - Never invent customer information.
                - Never invent banking policies.
                - Never modify customer values.
                - Do not guarantee approval or rejection unless
                the evidence clearly supports it.
                - Clearly mention when information is insufficient.
                - Answer only Personal Loan related queries.
                - Keep the answer professional and easy to understand.

                Your response will next be reviewed by a Critic Agent.
                """
            ),

            (
                "human",
                """
                USER QUESTION:
                {query}

                CUSTOMER PROFILE:
                {customer_profile}

                RETRIEVED PERSONAL LOAN POLICY:
                {retrieved_context}

                Generate the initial response.
                """
            )
        ]
    )

    prepare_inputs = RunnableParallel(

        query=RunnableLambda(
            lambda data:
                data["query"]
        ),

        customer_profile=RunnableLambda(
            lambda data:
                format_profile(
                    data.get(
                        "customer_profile",
                        {}
                    )
                )
        ),

        retrieved_context=RunnableLambda(
            lambda data:
                format_context(
                    data.get(
                        "retrieved_context",
                        []
                    )
                )
        )
    )

    chain = (
        prepare_inputs
        | prompt
        | llm
    )


    return chain