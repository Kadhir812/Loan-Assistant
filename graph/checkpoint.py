from langgraph.checkpoint.memory import (
    InMemorySaver
)

# Shared checkpointer
checkpointer = InMemorySaver()

def get_checkpointer():

    return checkpointer