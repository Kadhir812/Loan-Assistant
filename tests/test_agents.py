from agents.intent_agent import (
    detect_intent
)

from agents.profile_agent import (
    fetch_customer_profile
)


def test_eligibility_intent():

    result = detect_intent(
        "Am I eligible for a personal loan?"
    )

    assert result == (
        "loan_eligibility"
    )


def test_rejection_intent():

    result = detect_intent(
        "Why was my personal loan rejected?"
    )

    assert result == (
        "loan_rejection"
    )


def test_credit_score_intent():

    result = detect_intent(
        "Is my credit score enough?"
    )

    assert result == (
        "credit_score"
    )


def test_foir_intent():

    result = detect_intent(
        "What is my FOIR?"
    )

    assert result == (
        "repayment_capacity"
    )


def test_existing_customer():

    profile = (
        fetch_customer_profile(
            "C1001"
        )
    )

    assert profile != {}

    assert (
        profile[
            "customer_id"
        ]
        == "C1001"
    )


def test_invalid_customer():

    profile = (
        fetch_customer_profile(
            "INVALID"
        )
    )

    assert profile == {}


def test_hitl_customer_missing_emi():

    profile = (
        fetch_customer_profile(
            "C1003"
        )
    )

    assert (
        "existing_emi"
        not in profile
    )