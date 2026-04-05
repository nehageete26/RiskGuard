# FastAPI is like Flask but faster and with automatic API docs.
# Visit http://localhost:8000/docs to see all endpoints.
#
# Each function decorated with @app.get() or @app.post()
# becomes an HTTP endpoint the frontend can call.

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.databases import SessionLocal, PredictionLog
from app.model import predict_risk
from app.config import settings
from datetime import datetime

# Create the FastAPI app — title shows in /docs
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# CORS allows the Streamlit frontend to call this API
# (browsers block cross-origin requests by default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # In production, restrict to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Database Dependency ───────────────────────────────────────
def get_db():
    """
    This is a FastAPI dependency — it creates a DB session for each
    request and closes it afterward, even if an error occurs.
    The 'yield' makes it a context manager automatically.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─── Input Schema ─────────────────────────────────────────────
class PredictionInput(BaseModel):
    """
    Pydantic model = input validation.
    FastAPI automatically validates incoming JSON against this.
    If 'age' is missing or not a number, it returns a 422 error automatically.
    """
    age: float = Field(..., ge=18, le=100, description="Applicant age")
    monthly_income: float = Field(..., ge=0, description="Monthly income in $")
    debt_ratio: float = Field(..., ge=0, le=1, description="Debt as fraction of income")
    revolving_utilization: float = Field(..., ge=0, le=1, description="Credit card usage %")
    times_30_59_days_late: float = Field(default=0, ge=0)
    times_60_89_days_late: float = Field(default=0, ge=0)
    times_90_days_late: float = Field(default=0, ge=0)
    open_credit_lines: float = Field(default=0, ge=0)
    real_estate_loans: float = Field(default=0, ge=0)
    dependents: float = Field(default=0, ge=0)


# ─── Endpoints ────────────────────────────────────────────────
@app.get("/health")
def health_check():
    """Simple ping to check if the server is alive."""
    return {
        "status": "✅ RiskGuard AI is running!",
        "app": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug
    }


@app.post("/predict")
def predict(input_data: PredictionInput, db: Session = Depends(get_db)):
    """
    Main prediction endpoint.
    1. Receives applicant JSON
    2. Calls ML model
    3. Saves result to DB
    4. Returns prediction
    """
    # Call the ML model
    result = predict_risk(input_data.dict())

    # Log to database (for analytics later)
    log = PredictionLog(
        age=input_data.age,
        monthly_income=input_data.monthly_income,
        debt_ratio=input_data.debt_ratio,
        revolving_utilization=input_data.revolving_utilization,
        risk_score=result['risk_score'],
        prediction=result['prediction'],
        risk_level=result['risk_level']
    )
    db.add(log)
    db.commit()

    return result


@app.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    """Returns aggregated stats on all predictions made so far."""
    total = db.query(PredictionLog).count()
    high_risk = db.query(PredictionLog).filter(PredictionLog.prediction == 1).count()
    low_risk = db.query(PredictionLog).filter(PredictionLog.prediction == 0).count()

    return {
        "total_predictions": total,
        "high_risk": high_risk,
        "low_risk": low_risk,
        "high_risk_percentage": round(high_risk / total * 100, 2) if total > 0 else 0
    }


@app.get("/predictions/history")
def prediction_history(limit: int = 50, db: Session = Depends(get_db)):
    """Returns the last N predictions — useful for audit logs."""
    logs = db.query(PredictionLog)\
             .order_by(PredictionLog.created_at.desc())\
             .limit(limit)\
             .all()

    return [
        {
            "id": log.id,
            "age": log.age,
            "monthly_income": log.monthly_income,
            "risk_score": log.risk_score,
            "risk_level": log.risk_level,
            "created_at": log.created_at.isoformat()
        }
        for log in logs
    ]