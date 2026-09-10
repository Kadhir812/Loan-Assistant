import uuid
from dotenv import load_dotenv
from langgraph.types import Command
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from graph.workflow import loan_graph

load_dotenv()
langfuse = get_client()

def create_config( customer_id: str ):

    thread_id = (
        customer_id
        + "-"
        + str(
            uuid.uuid4()
        )
    )

    langfuse_handler = (
        CallbackHandler()
    )

    config = {

        "configurable": {

            "thread_id":
                thread_id
        },

        "callbacks": [
            langfuse_handler
        ],

        "metadata": {

            "langfuse_user_id":
                customer_id,

            "langfuse_session_id":
                thread_id,

            "langfuse_tags": [
                "personal-loan",
                "langgraph",
                "module-3"
            ]
        }
    }

    return config

def start_request( customer_id: str, query: str ):

    config = create_config(
        customer_id
    )

    initial_state = {

        "customer_id":
            customer_id,

        "query":
            query
    }

    result = loan_graph.invoke(
        initial_state,
        config=config
    )

    return result, config


def resume_request( config: dict, human_data: dict ):

    result = loan_graph.invoke(

        Command( resume=human_data ),

        config=config
    )

    return result


def convert_value( field: str, value: str ):

    integer_fields = {
        "age",
        "credit_score",
        "loan_tenure_years"
    }

    number_fields = {
        "monthly_income",
        "existing_emi",
        "requested_loan_amount",
        "proposed_emi"
    }

    try:

        if field in integer_fields:

            return int( value )


        if field in number_fields:

            return float( value )

    except ValueError:

        return value

    return value


def get_interrupt_data( result ):

    if not isinstance( result, dict ):

        return None

    interrupts = result.get( "__interrupt__" )

    if not interrupts:

        return None

    first_interrupt = ( interrupts[0])

    if hasattr( first_interrupt, "value" ):

        return first_interrupt.value

    if isinstance( first_interrupt, dict ):

        return first_interrupt

    return None

def main():

    print()

    print( "PERSONAL LOAN ELIGIBILITY & REJECTION ASSISTANT")

    print( "Available Test Customers" )

    print( "C1001 - Moderate profile")

    print( "C1002 - Strong profile" )

    print( "C1003 - Missing EMI / HITL test" )

    print( "C1004 - Low income and credit score" )

    customer_id = input( "\nEnter Customer ID: " ).strip()
    query = input( "Enter Question: " ).strip()

    try:

        result, config = (
            start_request(
                customer_id,
                query
            )
        )

        while True:

            interrupt_data = (
                get_interrupt_data(
                    result
                )
            )

            if not interrupt_data:

                break

            print()

            print( "HUMAN-IN-THE-LOOP" )

            print(
                interrupt_data.get(
                    "message",
                    "Additional information required."
                )
            )

            missing_fields = (
                interrupt_data.get(
                    "missing_fields",
                    []
                )
            )

            human_data = {}

            for field in missing_fields:

                value = input( f"Enter {field}: " )

                human_data[ field ] = convert_value(
                    field,
                    value
                )

            result = (
                resume_request(
                    config,
                    human_data
                )
            )

        print()
        print( "DETECTED INTENT" )
        print(
            result.get(
                "intent",
                "-"
            )
        )

        print()
        print( "CUSTOMER PROFILE" )
        print(
            result.get(
                "customer_profile",
                {}
            )
        )

        print()
        print( "AGENT 1 - RESPONSE AGENT" )
        print(
            result.get(
                "initial_response",
                "-"
            )
        )

        print()
        print( "AGENT 2 - CRITIC AGENT" )
        print(
            "Status:",
            result.get(
                "critic_status",
                "-"
            )
        )
        print(
            "Can Proceed:",
            result.get(
                "can_proceed",
                "-"
            )
        )
        print(
            "Missing Fields:",
            result.get(
                "missing_fields",
                []
            )
        )


        print()
        print( "Critic Feedback:" )
        print(
            result.get(
                "critic_feedback",
                "-"
            )
        )

        print()
        print( "AGENT 3 - FINAL ANSWER" )
        print(
            result.get(
                "final_answer",
                "No final answer generated."
            )
        )


        print()
        print( "WORKFLOW COMPLETED" )

    except Exception as error:

        print()
        print( "APPLICATION ERROR" )
        print( str(error) )

    finally:

        try:

            langfuse.flush()

        except Exception as error:

            print(
                "Langfuse flush warning:",
                error
            )


if __name__ == "__main__":

    main()