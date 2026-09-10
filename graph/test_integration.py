import asyncio

from langgraph.graph import StateGraph, START, END

from graph.state import LoanState
from graph.nodes import profile_node


def build_graph():

    graph = StateGraph(LoanState)

    graph.add_node(
        "profile",
        profile_node
    )

    graph.add_edge(
        START,
        "profile"
    )

    graph.add_edge(
        "profile",
        END
    )

    return graph.compile()


async def main():

    # -----------------------------------------
    # User input
    # -----------------------------------------

    query = "Can I get a personal loan of ₹10,00,000?"

    customer_id = "C1001"

    state = {
        "query": query,
        "customer_id": customer_id
    }

    # -----------------------------------------
    # Build LangGraph
    # -----------------------------------------

    app = build_graph()

    # -----------------------------------------
    # Execute LangGraph
    # -----------------------------------------

    result = await app.ainvoke(state)

    # -----------------------------------------
    # Print result
    # -----------------------------------------

    print("\n" + "=" * 60)
    print("USER QUERY")
    print("=" * 60)

    print(query)

    print("\n" + "=" * 60)
    print("CUSTOMER ID")
    print("=" * 60)

    print(customer_id)

    print("\n" + "=" * 60)
    print("CUSTOMER PROFILE FROM MCP")
    print("=" * 60)

    print(
        result.get(
            "customer_profile",
            {}
        )
    )

    print("\n" + "=" * 60)
    print("ERROR")
    print("=" * 60)

    print(
        result.get(
            "error"
        )
    )

    print("\n" + "=" * 60)
    print("FINAL LANGGRAPH STATE")
    print("=" * 60)

    print(result)


if __name__ == "__main__":

    asyncio.run(main())