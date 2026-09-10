from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel,RunnableLambda
from langchain_openai import ChatOpenAI
from chains.response_chain import format_profile, format_context

llm = ChatOpenAI( model="gpt-5.6-luna", reasoning_effort="none" )

final_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are Agent 3, the Final Answer Agent for a
            Personal Loan Eligibility and Rejection Assistant.

            You receive:

            1. Original user question
            2. Customer profile
            3. Retrieved policy
            4. Agent 1 original response
            5. Agent 2 critique

            Your job is to create the FINAL user-facing answer.

            Rules:

            - Consider Agent 2's feedback carefully.
            - Correct problems identified by Agent 2.
            - Use only available customer information.
            - Use only retrieved banking policy.
            - Never invent customer details.
            - Never invent banking policies.
            - Never make unsupported approval claims.
            - Never make unsupported rejection claims.
            - Clearly explain the important eligibility or
            rejection factors.
            - Mention relevant page and section when useful.
            - Make the answer professional and understandable.
            """
        ),

        (
            "human",
            """
            USER QUESTION:
            {query}

            CUSTOMER PROFILE:
            {customer_profile}

            RETRIEVED POLICY:
            {retrieved_context}

            AGENT 1 ORIGINAL RESPONSE:
            {initial_response}

            AGENT 2 CRITIC FEEDBACK:
            {critic_feedback}

            Generate the final answer.
            """
        )
    ]
)

final_inputs = RunnableParallel(

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
    ),

    initial_response=RunnableLambda(
        lambda data:
            data.get(
                "initial_response",
                ""
            )
    ),

    critic_feedback=RunnableLambda(
        lambda data:
            data.get(
                "critic_feedback",
                ""
            )
    )
)

final_chain = (
    final_inputs
    | final_prompt
    | llm
)

def generate_final_answer(
    query: str,
    customer_profile: dict,
    retrieved_context: list,
    initial_response: str,
    critic_feedback: str
) -> str:

    result = final_chain.invoke(
        {
            "query":
                query,

            "customer_profile":
                customer_profile,

            "retrieved_context":
                retrieved_context,

            "initial_response":
                initial_response,

            "critic_feedback":
                critic_feedback
        }
    )

    return result.content