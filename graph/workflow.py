from langgraph.graph import StateGraph,START,END
from graph.state import LoanState
from graph.nodes import (
    intent_node,
    profile_node,
    rag_node,
    response_node,
    critic_node,
    human_input_node,
    final_node,
    error_node
)
from graph.routing import route_after_critic
from graph.checkpoint import get_checkpointer

def build_workflow():

    builder = StateGraph( LoanState )
    builder.add_node( "intent", intent_node )
    builder.add_node( "profile", profile_node )
    builder.add_node( "rag", rag_node )
    builder.add_node( "response", response_node )
    builder.add_node( "critic", critic_node )
    builder.add_node( "human", human_input_node )
    builder.add_node( "final", final_node )
    builder.add_node( "error", error_node )

    builder.add_edge( START, "intent" )
    builder.add_edge( "intent", "profile" )
    builder.add_edge( "profile", "rag" )
    builder.add_edge( "rag", "response" )
    builder.add_edge( "response", "critic" )
    builder.add_conditional_edges(
        "critic",
        route_after_critic,
        {
            "final": "final",
            "human": "human",
            "error": "error"
        }
    )

    builder.add_edge( "human", "critic" )
    builder.add_edge( "final", END )
    builder.add_edge( "error", END )

    graph = builder.compile(
        checkpointer=
            get_checkpointer()
    )

    return graph

loan_graph = build_workflow()