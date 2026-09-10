def detect_intent(query: str) -> str:

    query = query.lower()

    if (
        "reject" in query
        or "rejected" in query
        or "declined" in query
    ):
        return "loan_rejection"

    if (
        "eligible" in query
        or "eligibility" in query
        or "approve" in query
        or "approval" in query
    ):
        return "loan_eligibility"

    if "document" in query:
        return "required_documents"

    if (
        "credit score" in query
        or "score" in query
    ):
        return "credit_score"

    if (
        "emi" in query
        or "foir" in query
    ):
        return "repayment_capacity"

    if (
        "loan amount" in query
        or "maximum loan" in query
    ):
        return "loan_amount"

    return "general_personal_loan"