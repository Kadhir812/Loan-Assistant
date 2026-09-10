from typing import Literal
from pydantic import BaseModel, Field 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda 
from langchain_openai import ChatOpenAI
from chains.response_chain import format_profile, format_context

class CriticResult(BaseModel):

    status: Literal[
        "PASS",
        "NEEDS_INPUT",
        "STOP"
    ]

    can_proceed: bool

    missing_fields: list[str] = Field(
        default_factory=list
    )

    feedback: str


llm = ChatOpenAI( model="gpt-5.6-luna", reasoning_effort="none" )

structured_llm = (
    llm.with_structured_output(
        CriticResult
    )
)

critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are Agent 2, the Critic Agent for a
            Personal Loan Eligibility and Rejection Assistant.

            Your job is RUNTIME VALIDATION.

            You are NOT DeepEval.

            Do NOT compare the answer against a ground truth
            or expected answer.

            Use only the runtime information supplied to you:

            1. Original user question
            2. Intent
            3. Customer profile
            4. Retrieved policy evidence
            5. Agent 1 response

            Check the following:

            - Is customer information available?
            - Are required customer fields available?
            - Did Agent 1 use correct customer values?
            - Did Agent 1 invent customer information?
            - Is Agent 1 consistent with retrieved policy?
            - Did Agent 1 invent a banking rule?
            - Does the answer make an unsupported approval claim?
            - Does the answer make an unsupported rejection claim?
            - Is more customer information required?
            - Can the workflow proceed to Agent 3?

            For loan eligibility questions, fields that may be
            important include:

            - age
            - employment_type
            - monthly_income
            - existing_emi
            - credit_score
            - requested_loan_amount
            - loan_tenure_years
            - kyc_status

            Return:

            PASS:
            The runtime evidence is sufficient and the workflow
            can proceed.

            NEEDS_INPUT:
            A customer-specific field required to continue is
            missing.

            STOP:
            The customer profile or essential runtime evidence
            is unavailable.

            When status is NEEDS_INPUT, include the exact missing
            field names in missing_fields.
            """
        ),

        (
            "human",
            """
            USER QUESTION:
            {query}

            DETECTED INTENT:
            {intent}

            CUSTOMER PROFILE:
            {customer_profile}

            RETRIEVED POLICY:
            {retrieved_context}

            AGENT 1 ORIGINAL RESPONSE:
            {initial_response}

            Critique Agent 1's response and determine
            whether the workflow can continue.
            """
        )
    ]
)

critic_inputs = RunnableParallel(

    query=RunnableLambda(
        lambda data:
            data["query"]
    ),

    intent=RunnableLambda(
        lambda data:
            data.get(
                "intent",
                "unknown"
            )
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
    )
)

critic_chain = (
    critic_inputs
    | critic_prompt
    | structured_llm
)

def critique_response(
    query: str,
    intent: str,
    customer_profile: dict,
    retrieved_context: list,
    initial_response: str
) -> CriticResult:

    result = critic_chain.invoke(
        {
            "query":
                query,

            "intent":
                intent,

            "customer_profile":
                customer_profile,

            "retrieved_context":
                retrieved_context,

            "initial_response":
                initial_response
        }
    )

    return result