import os

import pytest

from dotenv import load_dotenv

from app import (
    start_request
)


load_dotenv()


pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    not os.getenv(
        "OPENAI_API_KEY"
    ),
    reason=
        "OPENAI_API_KEY is not configured."
)
def test_complete_customer():

    result, config = (
        start_request(
            "C1002",
            "Am I eligible for a personal loan?"
        )
    )


    assert result is not None


    assert (
        result.get(
            "customer_profile"
        )
        is not None
    )


    assert (
        result.get(
            "initial_response"
        )
        is not None
    )


    assert (
        result.get(
            "critic_status"
        )
        in [
            "PASS",
            "NEEDS_INPUT",
            "STOP"
        ]
    )


@pytest.mark.skipif(
    not os.getenv(
        "OPENAI_API_KEY"
    ),
    reason=
        "OPENAI_API_KEY is not configured."
)
def test_invalid_customer():

    result, config = (
        start_request(
            "INVALID",
            "Am I eligible for a personal loan?"
        )
    )


    assert (
        result.get(
            "customer_profile"
        )
        == {}
    )


    assert (
        result.get(
            "critic_status"
        )
        == "STOP"
    )


    assert (
        result.get(
            "final_answer"
        )
        is not None
    )