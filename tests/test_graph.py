from graph.routing import (
    route_after_critic
)


def test_pass_route():

    state = {
        "critic_status":
            "PASS"
    }


    result = route_after_critic(
        state
    )


    assert result == "final"


def test_needs_input_route():

    state = {
        "critic_status":
            "NEEDS_INPUT"
    }


    result = route_after_critic(
        state
    )


    assert result == "human"


def test_stop_route():

    state = {
        "critic_status":
            "STOP"
    }


    result = route_after_critic(
        state
    )


    assert result == "error"


def test_missing_status():

    state = {}


    result = route_after_critic(
        state
    )


    assert result == "error"