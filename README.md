# 🛡️ RiskGuard AI

> 🚀 ML-powered Credit Risk Prediction System
> Built with XGBoost, FastAPI, Streamlit & Docker

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

---

## 📌 Overview

RiskGuard AI is a **Machine Learning system** that predicts whether a loan applicant is:

* ✅ **Low Risk**
* ⚠️ **High Risk**

It helps automate loan approval decisions using real-world financial data.

📊 Built on **150,000 credit records** and optimized using **XGBoost (AUC ≈ 0.82)**.

💡 Fully runs locally using Docker — no cloud dependency required.

---

## 🧠 How It Works

```
Applicant Data → ML Model → Risk Score → Decision
```

### Input Features:

* Age
* Monthly Income
* Debt Ratio
* Credit Utilization
* Payment History (30/60/90 days late)
* Number of Loans

### Output:

* Prediction (0 / 1)
* Risk Score (%)
* Risk Level

---

## 🏗️ System Architecture

```
             ┌───────────────┐
             │  Streamlit UI │
             └──────┬────────┘
                    │ API Calls
                    ▼
             ┌───────────────┐
             │   FastAPI     │
             └──────┬────────┘
                    │
        ┌───────────▼───────────┐
        │   ML Model (XGBoost)  │
        └───────────┬───────────┘
                    │
             ┌──────▼──────┐
             │  SQLite DB  │
             └─────────────┘
```

---

## 📁 Project Structure

```
riskguard-ai/
│
├── app/                # FastAPI backend
├── streamlit_app/      # Frontend UI
├── notebooks/          # ML pipeline
├── model/              # Trained models
├── reports/            # Visualizations
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
```

---

## ⚙️ ML Pipeline

1. **Preprocessing**

   * Missing value handling
   * Outlier clipping
   * Feature scaling
   * SMOTE (class balancing)

2. **Model Training**

   * Logistic Regression
   * Random Forest
   * ✅ XGBoost (Best)

3. **Explainability**

   * SHAP analysis
   * Feature importance

4. **Experiment Tracking**

   * MLflow

---

## 📊 Model Performance

| Model               | AUC-ROC    | F1 Score |
| ------------------- | ---------- | -------- |
| Logistic Regression | 0.8035     | 0.54     |
| Random Forest       | 0.8176     | 0.57     |
| **XGBoost**         | **0.8198** | **0.58** |

---

## 🖥️ Features

✅ Real-time prediction API
✅ Interactive Streamlit dashboard
✅ Analytics & history tracking
✅ SHAP explainability
✅ MLflow experiment tracking
✅ Dockerized deployment

---

## 🚀 Quick Start

### 1️⃣ Clone Repo

```bash
git clone https://github.com/your-username/riskguard-ai.git
cd riskguard-ai
```

---

### 2️⃣ Setup Environment

```bash
cp .env.example .env
pip install -r requirements.txt
```

---

### 3️⃣ Run Locally

```bash
uvicorn app.main:app --reload
streamlit run streamlit_app/app.py
```

* API → http://localhost:8000/docs
* UI  → http://localhost:8501

---

### 🐳 Run with Docker (Recommended)

```bash
docker compose up --build
```

🔥 One command runs everything!

---

## 📊 API Endpoints

| Endpoint               | Method | Description         |
| ---------------------- | ------ | ------------------- |
| `/health`              | GET    | Check API status    |
| `/predict`             | POST   | Get risk prediction |
| `/analytics`           | GET    | Stats dashboard     |
| `/predictions/history` | GET    | Past predictions    |

---

## 🔍 Example Request

```json
{
  "age": 35,
  "monthly_income": 5000,
  "debt_ratio": 0.3,
  "revolving_utilization": 0.5,
  "dependents": 1
}
```

---

## 📈 Sample Output

```json
{
  "prediction": 1,
  "risk_score": 0.78,
  "risk_level": "High Risk ⚠️"
}
```

---

## 🧪 Notebooks

* preprocessing.ipynb
* model_training.ipynb
* shap_analysis.ipynb
* mlflow_tracking.ipynb

---

## 🔐 Environment Variables

```env
DATABASE_URL=sqlite:///./predictions.db
MODEL_PATH=model/best_model.pkl
SCALER_PATH=model/scaler.pkl
API_URL=http://localhost:8000
```

---

## 🌐 Deployment

This project is designed to run **locally or via Docker**.

### 🖥️ Local Deployment

```bash
uvicorn app.main:app --reload
streamlit run streamlit_app/app.py
```

---

### 🐳 Docker Deployment

```bash
docker compose up --build
```

---

### 📊 MLflow (Optional)

```bash
mlflow ui --backend-store-uri sqlite:///./mlflow.db
```

Open → http://localhost:5000

---

## 📸 Screenshots 

### 🖥️ UI Dashboard

(Add your screenshot here)

### 📊 Analytics

(Add charts here)

---

## 💡 Key Highlights

* Handles **real-world imbalanced data**
* Uses **SMOTE + XGBoost**
* Fully **production-ready architecture**
* Clean separation: ML + API + UI

---

## 👨‍💻 Author

**Neha Geete**

---

## ⭐ Give a Star

If you liked this project, consider giving it a ⭐ on GitHub!
