import streamlit as st
import pandas as pd
import joblib


# -----------------------------------------
# Load trained model
# -----------------------------------------
model = joblib.load("customer_churn_model.pkl")


# -----------------------------------------
# Page configuration
# -----------------------------------------
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="centered"
)


# -----------------------------------------
# Title
# -----------------------------------------
st.title("📊 Customer Churn Prediction")

st.write(
    "Enter customer details to predict the probability of customer churn."
)


# -----------------------------------------
# Customer Inputs
# -----------------------------------------

credit_score = st.number_input(
    "Credit Score",
    min_value=300,
    max_value=850,
    value=650
)

country = st.selectbox(
    "Country",
    ["France", "Spain", "Germany"]
)

gender = st.selectbox(
    "Gender",
    ["Female", "Male"]
)

age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=35
)

tenure = st.number_input(
    "Tenure",
    min_value=0,
    max_value=10,
    value=5
)

balance = st.number_input(
    "Balance",
    min_value=0.0,
    value=75000.0
)

products_number = st.number_input(
    "Number of Products",
    min_value=1,
    max_value=4,
    value=2
)

credit_card = st.selectbox(
    "Has Credit Card?",
    ["Yes", "No"]
)

active_member = st.selectbox(
    "Active Member?",
    ["Yes", "No"]
)

estimated_salary = st.number_input(
    "Estimated Salary",
    min_value=0.0,
    value=60000.0
)


# -----------------------------------------
# Convert Yes/No to 1/0
# -----------------------------------------

credit_card_value = 1 if credit_card == "Yes" else 0

active_member_value = 1 if active_member == "Yes" else 0


# -----------------------------------------
# Create customer DataFrame
# -----------------------------------------

new_customer = pd.DataFrame({
    "credit_score": [credit_score],
    "country": [country],
    "gender": [gender],
    "age": [age],
    "tenure": [tenure],
    "balance": [balance],
    "products_number": [products_number],
    "credit_card": [credit_card_value],
    "active_member": [active_member_value],
    "estimated_salary": [estimated_salary]
})


# -----------------------------------------
# Prediction
# -----------------------------------------

if st.button("🔍 Predict Churn"):

    # Make prediction
    prediction = model.predict(new_customer)

    # Get probability
    probability = model.predict_proba(new_customer)

    # Extract probabilities
    no_churn_probability = probability[0][0]
    churn_probability = probability[0][1]


    # -------------------------------------
    # Prediction Result
    # -------------------------------------

    st.subheader("Prediction Result")


    if prediction[0] == 1:

        st.error("⚠️ Customer is likely to churn")

    else:

        st.success("✅ Customer is unlikely to churn")


    # -------------------------------------
    # Display Probabilities
    # -------------------------------------

    st.write(
        f"**Probability of No Churn:** "
        f"{no_churn_probability:.2%}"
    )

    st.write(
        f"**Probability of Churn:** "
        f"{churn_probability:.2%}"
    )


    # -------------------------------------
    # Churn Probability Bar
    # -------------------------------------

    st.write("### Churn Probability")

    st.progress(float(churn_probability))


    # -------------------------------------
    # Risk Level
    # -------------------------------------

    if churn_probability < 0.30:

        risk_level = "Low Risk"

    elif churn_probability < 0.60:

        risk_level = "Medium Risk"

    else:

        risk_level = "High Risk"


    st.subheader(
        f"Churn Risk: {risk_level}"
    )


    # -------------------------------------
    # Business Recommendation
    # -------------------------------------

    if risk_level == "Low Risk":

        st.info(
            "This customer currently has a low estimated "
            "churn risk. No immediate retention action may "
            "be required."
        )

    elif risk_level == "Medium Risk":

        st.warning(
            "This customer has a moderate estimated churn "
            "risk. Consider monitoring the customer and "
            "understanding potential reasons for dissatisfaction."
        )

    else:

        st.error(
            "This customer has a high estimated churn risk. "
            "The business may consider proactive retention "
            "strategies."
        )