from graph.state import LoanState

def route_after_critic( state: LoanState ):

    status = state.get(
        "critic_status",
        "STOP"
    )

    if status == "PASS":
        return "final"

    if status == "NEEDS_INPUT":
        return "human"

    return "error"