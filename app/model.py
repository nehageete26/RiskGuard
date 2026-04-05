# This file loads the trained ML model from disk and
# exposes a predict_risk() function the API can call.
#
# The model was trained in notebooks/model_training.ipynb
# and saved as .pkl (pickle) files using joblib.

import joblib
import numpy as np
from pathlib import Path
from app.config import settings  # ← reads from .env

# Resolve paths relative to project root
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / settings.model_path
SCALER_PATH = BASE_DIR / settings.scaler_path

# Load once when server starts — NOT on every request (that would be slow!)
# joblib is like pickle but better for large numpy arrays
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print(f"✅ Model loaded from: {MODEL_PATH}")
except FileNotFoundError:
    print("❌ Model not found! Run the training notebooks first.")
    model = None
    scaler = None


def predict_risk(data: dict) -> dict:
    """
    Takes applicant data as a dict, returns prediction.
    
    The feature ORDER matters — must match what the model was trained on.
    This order comes from preprocessing.ipynb where X = df.drop('SeriousDlqin2yrs')
    """
    if model is None or scaler is None:
        raise RuntimeError("Model not loaded. Run training notebooks first.")

    # Step 1: Extract features in the EXACT same order as training
    features = np.array([[
        data['revolving_utilization'],      # RevolvingUtilizationOfUnsecuredLines
        data['age'],                         # age
        data['times_30_59_days_late'],       # NumberOfTime30-59DaysPastDueNotWorse
        data['debt_ratio'],                  # DebtRatio
        data['monthly_income'],              # MonthlyIncome
        data['open_credit_lines'],           # NumberOfOpenCreditLinesAndLoans
        data['times_90_days_late'],          # NumberOfTimes90DaysLate
        data['real_estate_loans'],           # NumberRealEstateLoansOrLines
        data['times_60_89_days_late'],       # NumberOfTime60-89DaysPastDueNotWorse
        data['dependents']                   # NumberOfDependents
    ]])

    # Step 2: Scale using the SAME scaler fitted during training
    # (If you used different scaling, predictions would be wrong)
    features_scaled = scaler.transform(features)

    # Step 3: Get prediction (0 or 1) and probability (0.0 to 1.0)
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0][1]  # [1] = prob of being class 1 (high risk)

    return {
        "prediction": int(prediction),
        "risk_score": round(float(probability), 4),  # e.g. 0.7832
        "risk_level": "High Risk ⚠️" if prediction == 1 else "Low Risk ✅"
    }