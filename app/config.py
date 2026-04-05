# This is the KEY file — it reads all environment variables
# and makes them available throughout the entire app.
# Instead of hardcoding values anywhere, we import from here.

from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # App
    app_name: str = "RiskGuard AI"
    app_version: str = "1.0.0"
    debug: bool = True

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Database — SQLite by default, easy to swap to Postgres
    database_url: str = "sqlite:///./predictions.db"

    # Model paths — resolved relative to project root
    model_path: str = "model/best_model.pkl"
    scaler_path: str = "model/scaler.pkl"

    # Streamlit talks to FastAPI via this URL
    api_url: str = "http://localhost:8000"

    # MLflow
    mlflow_tracking_uri: str = "sqlite:///./mlflow.db"
    mlflow_experiment_name: str = "Credit_Risk_Prediction"

    # Security
    secret_key: str = "change-this-in-production"

    class Config:
        # This tells pydantic to read from .env file automatically
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False  # DATABASE_URL and database_url both work


# Single shared instance — import this everywhere
settings = Settings()