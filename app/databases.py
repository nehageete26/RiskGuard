# Database setup using SQLAlchemy ORM.
# ORM means you write Python classes instead of raw SQL.
# PredictionLog class = "predictions" table in the database.

from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import settings  # ← reads from .env

# create_engine connects Python to the database
# check_same_thread=False is needed only for SQLite (threading issue)
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# SessionLocal is a factory — each request gets its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class all your DB models inherit from
Base = declarative_base()


class PredictionLog(Base):
    """
    This Python class maps directly to a database table.
    Every attribute = one column in the table.
    Every instance = one row (one prediction log entry).
    """
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Float)
    monthly_income = Column(Float)
    debt_ratio = Column(Float)
    revolving_utilization = Column(Float)
    risk_score = Column(Float)
    prediction = Column(Integer)   # 0 = low risk, 1 = high risk
    risk_level = Column(String)    # "High Risk ⚠️" or "Low Risk ✅"
    created_at = Column(DateTime, default=datetime.utcnow)


# This creates the actual table in the DB if it doesn't exist yet
# Safe to run multiple times — won't duplicate tables
Base.metadata.create_all(bind=engine)