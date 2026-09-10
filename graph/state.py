from typing import TypedDict, Optional, Any

class LoanState(TypedDict, total=False):

    query: str
    customer_id: str
    intent: str

    customer_profile: dict[str, Any]

    retrieved_context: list[dict[str, Any]]

    initial_response: str

    critic_status: str
    can_proceed: bool
    missing_fields: list[str]
    critic_feedback: str

    human_input: Optional[dict[str, Any]]

    final_answer: str
    
    error: Optional[str]