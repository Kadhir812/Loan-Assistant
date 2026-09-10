from langgraph.types import interrupt
from graph.state import LoanState
from agents.intent_agent import detect_intent
from agents.profile_agent import ProfileAgent
from agents.response_agent import generate_response
from agents.critic_agent import critique_response
from agents.final_agent import generate_final_answer

POLICY_CONTEXT = [

    {
        "source":
            "Meridian Trust Bank Loan Policy Manual",

        "page":
            3,

        "section":
            "Personal Loan Eligibility",

        "content":
            """
            Minimum applicant age is 21 years.

            Applicants must satisfy applicable age,
            employment/business vintage, income,
            credit-score, FOIR, KYC and credit-history
            requirements.
            """
    },

    {
        "source":
            "Meridian Trust Bank Loan Policy Manual",

        "page":
            4,

        "section":
            "Income Requirements",

        "content":
            """
            Minimum monthly income for salaried applicants
            is ₹25,000.

            Minimum monthly income for self-employed applicants
            is ₹30,000.
            """
    },

    {
        "source":
            "Meridian Trust Bank Loan Policy Manual",

        "page":
            5,

        "section":
            "Credit Score Criteria",

        "content":
            """
            Credit score classification:

            750-900: Excellent
            700-749: Good
            650-699: Moderate
            600-649: High Risk / Conditional Approval
            Below 600: Very High Risk / Declined

            Minimum credit score for standard approval
            is 650.
            """
    },

    {
        "source":
            "Meridian Trust Bank Loan Policy Manual",

        "page":
            5,

        "section":
            "FOIR Rules",

        "content":
            """
            FOIR is total monthly debt obligations divided
            by net monthly income multiplied by 100.

            Maximum permitted FOIR is 50%.

            The proposed Personal Loan EMI must also be
            included when calculating FOIR.

            Maximum DTI is 55%.
            """
    },

    {
        "source":
            "Meridian Trust Bank Loan Policy Manual",

        "page":
            6,

        "section":
            "Maximum Loan Amount",

        "content":
            """
            Personal Loan amount ranges from ₹50,000
            to ₹25,00,000.

            The maximum eligible amount is the lowest of:

            1. 20 times net monthly income
            2. ₹25,00,000
            3. Amount that keeps FOIR within 50%

            Applicants with a credit score from 650 to 699
            are capped at 70 percent of the computed ceiling.
            """
    },

    {
        "source":
            "Meridian Trust Bank Loan Policy Manual",

        "page":
            7,

        "section":
            "KYC and Documents",

        "content":
            """
            Applicants must provide complete KYC and
            mandatory income and employment documentation.

            Invalid KYC or missing mandatory documents can
            affect loan approval.
            """
    },

    {
        "source":
            "Meridian Trust Bank Loan Policy Manual",

        "page":
            8,

        "section":
            "Common Rejection Reasons",

        "content":
            """
        Common Personal Loan rejection reasons include:

        - Credit score below 600
        - FOIR exceeding 50 percent without viable restructuring
        - DTI exceeding 55 percent
        - Income below the applicable minimum
        - Recent unresolved default or write-off
        - Invalid KYC
        - Missing mandatory documentation
        - Insufficient employment or business vintage
        """
    }
]

#Node 1 - Intent
def intent_node(
    state: LoanState
):

    intent = detect_intent(
        state["query"]
    )

    return {
        "intent":
            intent
    }

# Node 2 - Customer Profile
async def profile_node(
    state: LoanState
):

    customer_id = state.get(
        "customer_id",
        ""
    )

    profile_agent = ProfileAgent()

    profile = await profile_agent.get_customer_profile(
        customer_id
    )

    if not profile.get("success"):

        return {
            "customer_profile": {},
            "error": profile.get(
                "message",
                "Customer profile was not found."
            )
        }

    return {
        "customer_profile": profile,
        "error": None
    }
    
#Node 3 - Rag
def rag_node(
    state: LoanState
):

    return {
        "retrieved_context":
            POLICY_CONTEXT
    }

#Node 4 - response
def response_node(
    state: LoanState
):

    response = generate_response(

        query=
            state["query"],

        customer_profile=
            state.get(
                "customer_profile",
                {}
            ),

        retrieved_context=
            state.get(
                "retrieved_context",
                []
            )
    )

    return {
        "initial_response":
            response
    }

#Node 5 - Critic
def critic_node(
    state: LoanState
):

    customer_profile = state.get(
        "customer_profile",
        {}
    )

    if not customer_profile:

        return {
            "critic_status":
                "STOP",

            "can_proceed":
                False,

            "missing_fields":
                [],

            "critic_feedback":
                "Customer profile is unavailable."
        }


    result = critique_response(

        query=
            state["query"],

        intent=
            state.get(
                "intent",
                ""
            ),

        customer_profile=
            customer_profile,

        retrieved_context=
            state.get(
                "retrieved_context",
                []
            ),

        initial_response=
            state.get(
                "initial_response",
                ""
            )
    )


    return {

        "critic_status":
            result.status,

        "can_proceed":
            result.can_proceed,

        "missing_fields":
            result.missing_fields,

        "critic_feedback":
            result.feedback
    }

#Node 6 - Human-in Loop
def human_input_node(
    state: LoanState
):

    missing_fields = state.get(
        "missing_fields",
        []
    )


    human_response = interrupt(
        {
            "type":
                "missing_customer_information",

            "message":
                "Additional customer information "
                "is required before continuing.",

            "missing_fields":
                missing_fields
        }
    )


    updated_profile = dict(
        state.get(
            "customer_profile",
            {}
        )
    )


    if isinstance(
        human_response,
        dict
    ):

        updated_profile.update(
            human_response
        )


    return {

        "customer_profile":
            updated_profile,

        "human_input":
            human_response
    }

#Node 7 - Final Output
def final_node(
    state: LoanState
):

    final_answer = (
        generate_final_answer(

            query=
                state["query"],

            customer_profile=
                state.get(
                    "customer_profile",
                    {}
                ),

            retrieved_context=
                state.get(
                    "retrieved_context",
                    []
                ),

            initial_response=
                state.get(
                    "initial_response",
                    ""
                ),

            critic_feedback=
                state.get(
                    "critic_feedback",
                    ""
                )
        )
    )


    return {
        "final_answer":
            final_answer
    }

#Error Handling Node
def error_node(
    state: LoanState
):

    message = (
        state.get(
            "error"
        )
        or
        state.get(
            "critic_feedback"
        )
        or
        "Required information is unavailable."
    )


    return {
        "final_answer":
            "Unable to complete the Personal Loan "
            "assessment. "
            + message
    }