CUSTOMERS = {

    "C1001": {
        "customer_id": "C1001",
        "name": "Arun Kumar",
        "age": 29,
        "employment_type": "Salaried",
        "monthly_income": 65000,
        "existing_emi": 18000,
        "credit_score": 680,
        "requested_loan_amount": 800000,
        "loan_tenure_years": 5,
        "kyc_status": "Verified"
    },

    "C1002": {
        "customer_id": "C1002",
        "name": "Priya Sharma",
        "age": 32,
        "employment_type": "Salaried",
        "monthly_income": 85000,
        "existing_emi": 10000,
        "credit_score": 760,
        "requested_loan_amount": 1000000,
        "loan_tenure_years": 5,
        "kyc_status": "Verified"
    },

    "C1003": {
        "customer_id": "C1003",
        "name": "Ravi Kumar",
        "age": 41,
        "employment_type": "Self-Employed",
        "monthly_income": 120000,

        # Existing EMI intentionally missing
        # Used for human-in-the-loop testing

        "credit_score": 720,
        "requested_loan_amount": 1500000,
        "loan_tenure_years": 5,
        "kyc_status": "Verified"
    },

    "C1004": {
        "customer_id": "C1004",
        "name": "Meera Nair",
        "age": 26,
        "employment_type": "Salaried",
        "monthly_income": 22000,
        "existing_emi": 5000,
        "credit_score": 590,
        "requested_loan_amount": 500000,
        "loan_tenure_years": 3,
        "kyc_status": "Verified"
    }
}


def fetch_customer_profile(customer_id: str) -> dict:

    customer = CUSTOMERS.get(customer_id)

    if customer is None:
        return { }

    res = { "Name": customer["name"] , "Age": customer["age"], "Employment_type": customer["employment_type"] , "Monthy_Income": customer["monthly_income"] , "Existing_EMI ": customer["existing_emi"]}

    return res
