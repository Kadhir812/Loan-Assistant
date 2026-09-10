DROP TABLE IF EXISTS customer_loan_profile;

CREATE TABLE customer_loan_profile (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_id VARCHAR(20) NOT NULL,
    name VARCHAR(100),
    age INTEGER,

    employment_type VARCHAR(50),
    employment_tenure_months INTEGER,
    current_employer_tenure_months INTEGER,

    monthly_income DECIMAL(12,2),
    existing_emi DECIMAL(12,2),

    credit_score INTEGER,
    credit_history_months INTEGER,
    credit_utilization_pct DECIMAL(5,2),
    defaults_last_24m INTEGER,
    dpd_90_count INTEGER,

    kyc_status VARCHAR(20),

    -- Loan application details
    loan_type VARCHAR(20),
    requested_loan_amount DECIMAL(14,2),
    loan_tenure_years INTEGER,
    documents_status VARCHAR(20),

    -- Home Loan specific
    property_value DECIMAL(14,2),
    down_payment DECIMAL(12,2),
    property_type VARCHAR(30),
    is_under_construction VARCHAR(5),
    rera_registered VARCHAR(5),

    -- Car Loan specific
    vehicle_type VARCHAR(10),
    vehicle_price DECIMAL(12,2),
    vehicle_age_years INTEGER,

    -- Education Loan specific
    course_type VARCHAR(20),
    academic_marks_pct DECIMAL(5,2),
    institution_recognized VARCHAR(5),
    co_applicant_income DECIMAL(12,2),
    co_applicant_credit_score INTEGER,
    collateral_value DECIMAL(14,2)
);

CREATE INDEX idx_customer_id
ON customer_loan_profile(customer_id);