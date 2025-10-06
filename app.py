import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px

# =====================
# Load Model
# =====================
with open("loan_default_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

st.title("💳 Loan Default Prediction & Amortization Dashboard")

st.sidebar.header("Borrower Information")

# =====================
# Helper Functions
# =====================
def calculate_amortization(loan_amount, annual_rate, months):
    """
    Generate amortization schedule: monthly payment, breakdown of principal & interest.
    """
    monthly_rate = annual_rate / 100 / 12
    if monthly_rate == 0:
        monthly_payment = loan_amount / months
    else:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** months) / (
            (1 + monthly_rate) ** months - 1
        )

    schedule = []
    balance = loan_amount
    for m in range(1, months + 1):
        interest = balance * monthly_rate
        principal = monthly_payment - interest
        balance -= principal
        schedule.append({
            "Month": m,
            "Payment": round(monthly_payment, 2),
            "Principal": round(principal, 2),
            "Interest": round(interest, 2),
            "Remaining Balance": round(max(balance, 0), 2)
        })
    return pd.DataFrame(schedule)


# =====================
# Collect User Input
# =====================
age = st.sidebar.number_input("Age", 18, 100, 30)
income = st.sidebar.number_input("Annual Income", 0, 1000000, 50000)
loan_amount = st.sidebar.number_input("Loan Amount", 1000, 1000000, 20000)
credit_score = st.sidebar.number_input("Credit Score", 300, 850, 650)
months_employed = st.sidebar.number_input("Months Employed", 0, 600, 24)
interest_rate = st.sidebar.slider("Interest Rate (%)", 1.0, 30.0, 10.0)
loan_term = st.sidebar.selectbox("Loan Term (months)", [12, 24, 36, 60, 120, 240, 360])

monthly_income = st.sidebar.number_input("Monthly Income", 0, 100000, 4000)
monthly_debt = st.sidebar.number_input(
    "Other Monthly Debt Payments (e.g. credit card, car loan)", 0, 100000, 1200
)

# Compute DTI ratio
dti_ratio = (monthly_debt / monthly_income * 100) if monthly_income > 0 else 0
st.sidebar.write(f"Calculated DTI Ratio: {dti_ratio:.2f}%")

education = st.sidebar.selectbox("Education", ["High School", "Bachelor's", "Master's", "PhD"])
employment_type = st.sidebar.selectbox("Employment Type", ["Salaried", "Self-employed", "Unemployed", "Part-time"])
marital_status = st.sidebar.selectbox("Marital Status", ["Single", "Married", "Divorced"])
loan_purpose = st.sidebar.selectbox("Loan Purpose", ["Home", "Business", "Education", "Other"])

# ✅ Map Yes/No to numeric (matches training pipeline)
has_mortgage = 1 if st.sidebar.selectbox("Has Mortgage?", ["No", "Yes"]) == "Yes" else 0
has_dependents = 1 if st.sidebar.selectbox("Has Dependents?", ["No", "Yes"]) == "Yes" else 0
has_cosigner = 1 if st.sidebar.selectbox("Has Co-signer?", ["No", "Yes"]) == "Yes" else 0

# =====================
# Build input DataFrame
# =====================
input_data = pd.DataFrame([{
    "Age": age,
    "Income": income,
    "LoanAmount": loan_amount,
    "CreditScore": credit_score,
    "MonthsEmployed": months_employed,
    "InterestRate": interest_rate,
    "LoanTerm": loan_term,
    "DTIRatio": dti_ratio,
    "Education": education,
    "EmploymentType": employment_type,
    "MaritalStatus": marital_status,
    "HasMortgage": has_mortgage,
    "HasDependents": has_dependents,
    "LoanPurpose": loan_purpose,
    "HasCoSigner": has_cosigner
}])


# =====================
# Prediction + Results
# =====================
if st.button("Predict Loan Default"):
    prob_default = model.predict_proba(input_data)[:, 1][0]

    # Generate amortization schedule
    schedule = calculate_amortization(loan_amount, interest_rate, loan_term)

    # Reminder Message with Color Coding
    next_payment = schedule.iloc[0]["Payment"]
    due_date = f"Month {schedule.iloc[0]['Month']}"

    if prob_default > 0.5:
        risk_color = "#ffcccc"  # red background
        msg = f"⚠️ High Risk of Default! Next payment of <b>${next_payment}</b> due on <b>{due_date}</b>."
    else:
        risk_color = "#ccffcc"  # green background
        msg = f"✅ Low Risk of Default. Next payment of <b>${next_payment}</b> due on <b>{due_date}</b>."

    st.markdown(
        f"""
        <div style="
            background-color:{risk_color};
            padding:20px;
            border-radius:10px;
            text-align:center;
            animation: blinker 1s linear infinite;
        ">
        <h2 style="color:black;">{msg}</h2>
        </div>
        <style>
        @keyframes blinker {{
          50% {{ opacity: 0; }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Show Default Probability
    st.subheader(f"📊 Probability of Default: {prob_default:.2%}")

    # =========================
    # Amortization Table & Charts
    # =========================
    st.subheader("📅 Loan Amortization Schedule")
    st.dataframe(schedule)

    fig = px.line(schedule, x="Month", y=["Principal", "Interest", "Remaining Balance"],
                  title="Loan Payment Breakdown")
    st.plotly_chart(fig, use_container_width=True)
