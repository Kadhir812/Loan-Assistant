from chains.response_chain import (
    format_profile,
    format_context
)


def test_format_profile():

    profile = {
        "name":
            "Arun",

        "monthly_income":
            65000
    }


    result = format_profile(
        profile
    )


    assert (
        "name: Arun"
        in result
    )

    assert (
        "monthly_income: 65000"
        in result
    )


def test_empty_profile():

    result = format_profile(
        {}
    )


    assert result == (
        "Customer profile unavailable."
    )


def test_format_context():

    context = [
        {
            "source":
                "Loan Manual",

            "page":
                5,

            "section":
                "Credit Score",

            "content":
                "Minimum score is 650."
        }
    ]


    result = format_context(
        context
    )


    assert (
        "Page: 5"
        in result
    )

    assert (
        "Credit Score"
        in result
    )

    assert (
        "Minimum score is 650."
        in result
    )


def test_empty_context():

    result = format_context(
        []
    )


    assert result == (
        "No policy context retrieved."
    )