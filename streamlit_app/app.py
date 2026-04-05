import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

# Load .env so Streamlit also has access to environment variables
load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="RiskGuard AI",
    page_icon="🛡️",
    layout="wide"
)

st.sidebar.title("🛡️ RiskGuard AI")
page = st.sidebar.radio("Navigation", [
    "🏠 Home",
    "🔍 Single Prediction",
    "📊 Analytics",
    "📋 Prediction History"
])

# ─── HOME ──────────────────────────────────────────────────────
if page == "🏠 Home":
    st.title("🛡️ RiskGuard AI")
    st.subheader("ML-Powered Credit Risk Prediction System")

    # Check if API is alive
    try:
        r = requests.get(f"{API_URL}/health", timeout=3)
        if r.status_code == 200:
            st.success(f"✅ API Connected — {API_URL}")
        else:
            st.error("❌ API not responding")
    except:
        st.error(f"❌ Cannot reach API at {API_URL}")

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Best Model", "XGBoost")
    col2.metric("AUC-ROC", "0.8198")
    col3.metric("Training Records", "150,000")

    st.markdown("""
    ### How It Works
    1. Enter applicant financial details in **Single Prediction**
    2. The model returns **High Risk ⚠️** or **Low Risk ✅**
    3. View trends in the **Analytics** dashboard
    """)

# ─── SINGLE PREDICTION ─────────────────────────────────────────
elif page == "🔍 Single Prediction":
    st.title("🔍 Single Risk Prediction")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 18, 100, 35)
        monthly_income = st.number_input("Monthly Income ($)", 0, 200000, 5000)
        debt_ratio = st.slider("Debt Ratio (0 = no debt, 1 = income = debt)", 0.0, 1.0, 0.3)
        revolving_utilization = st.slider("Credit Utilization (% of credit used)", 0.0, 1.0, 0.5)
        dependents = st.number_input("Number of Dependents", 0, 20, 1)

    with col2:
        times_30_59 = st.number_input("Times 30–59 Days Late on Payment", 0, 20, 0)
        times_60_89 = st.number_input("Times 60–89 Days Late on Payment", 0, 20, 0)
        times_90 = st.number_input("Times 90+ Days Late on Payment", 0, 20, 0)
        open_credit = st.number_input("Open Credit Lines", 0, 50, 5)
        real_estate = st.number_input("Real Estate Loans", 0, 20, 1)

    if st.button("🔍 Predict Risk", type="primary"):
        payload = {
            "age": age,
            "monthly_income": monthly_income,
            "debt_ratio": debt_ratio,
            "revolving_utilization": revolving_utilization,
            "times_30_59_days_late": times_30_59,
            "times_60_89_days_late": times_60_89,
            "times_90_days_late": times_90,
            "open_credit_lines": open_credit,
            "real_estate_loans": real_estate,
            "dependents": dependents
        }
        try:
            response = requests.post(f"{API_URL}/predict", json=payload)
            result = response.json()

            st.markdown("---")
            if result['prediction'] == 1:
                st.error(f"## {result['risk_level']}")
                st.write("This applicant shows signs of credit risk.")
            else:
                st.success(f"## {result['risk_level']}")
                st.write("This applicant appears financially stable.")

            st.metric("Risk Score", f"{result['risk_score'] * 100:.1f}%",
                      help="Probability of defaulting. Above 50% = High Risk.")
        except Exception as e:
            st.error(f"Error calling API: {e}")

# ─── ANALYTICS ─────────────────────────────────────────────────
elif page == "📊 Analytics":
    st.title("📊 Analytics Dashboard")

    try:
        data = requests.get(f"{API_URL}/analytics").json()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Predictions", data['total_predictions'])
        col2.metric("High Risk", data['high_risk'])
        col3.metric("Low Risk", data['low_risk'])
        col4.metric("High Risk %", f"{data['high_risk_percentage']}%")

        if data['total_predictions'] > 0:
            fig = px.pie(
                values=[data['high_risk'], data['low_risk']],
                names=['High Risk ⚠️', 'Low Risk ✅'],
                color_discrete_sequence=['#FF6B6B', '#51CF66'],
                title='Risk Distribution of All Predictions'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No predictions yet. Go to Single Prediction to get started!")
    except Exception as e:
        st.error(f"Could not load analytics: {e}")

# ─── HISTORY ───────────────────────────────────────────────────
elif page == "📋 Prediction History":
    st.title("📋 Recent Predictions")

    try:
        data = requests.get(f"{API_URL}/predictions/history?limit=50").json()
        if data:
            df = pd.DataFrame(data)
            df['risk_score'] = (df['risk_score'] * 100).round(1).astype(str) + "%"
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No predictions logged yet.")
    except Exception as e:
        st.error(f"Could not load history: {e}")