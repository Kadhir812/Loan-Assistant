from mcp_server.db import fetch_all
from mcp_server.errors import (
    CustomerNotFoundError,
    MCPToolError,
)


def get_customer_profile(customer_id: str) -> dict:
    """
    Retrieve all loan applications associated with a customer.

    The caller provides only the customer_id.
    SQL is completely controlled by the application.
    """

    # -----------------------------
    # Input validation
    # -----------------------------

    if not customer_id:
        raise MCPToolError(
            "customer_id is required."
        )

    customer_id = customer_id.strip()

    if not customer_id:
        raise MCPToolError(
            "customer_id cannot be empty."
        )

    # Optional format validation
    if len(customer_id) > 20:
        raise MCPToolError(
            "Invalid customer_id."
        )


    query = """
        SELECT
            application_id,
            customer_id,
            name,
            age,
            employment_type,
            employment_tenure_months,
            current_employer_tenure_months,
            monthly_income,
            existing_emi,
            credit_score,
            credit_history_months,
            credit_utilization_pct,
            defaults_last_24m,
            dpd_90_count,
            kyc_status,

            loan_type,
            requested_loan_amount,
            loan_tenure_years,
            documents_status,

            property_value,
            down_payment,
            property_type,
            is_under_construction,
            rera_registered,

            vehicle_type,
            vehicle_price,
            vehicle_age_years,

            course_type,
            academic_marks_pct,
            institution_recognized,
            co_applicant_income,
            co_applicant_credit_score,
            collateral_value

        FROM customer_loan_profile

        WHERE customer_id = ?
    """

    try:

        rows = fetch_all(
            query,
            (customer_id,)
        )

    except MCPToolError:
        raise

    except Exception as e:

        raise MCPToolError(
            f"Unable to retrieve customer profile: {e}"
        ) from e

    

    if not rows:

        raise CustomerNotFoundError(
            f"Customer '{customer_id}' was not found."
        )

    # Convert sqlite3.Row → dict
    profiles = [
        dict(row)
        for row in rows
    ]

    return {
        "success": True,
        "customer_id": customer_id,
        "application_count": len(profiles),
        "profiles": profiles,
    }