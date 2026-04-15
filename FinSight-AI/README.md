# FinSight AI – Intelligent Financial Advisor System

FinSight AI is an end-to-end machine learning project that analyzes monthly income/expenses, predicts overall financial health, classifies risk, and generates personalized recommendations. It runs as an interactive Streamlit dashboard and supports multi-country usage with currency-aware formatting.

This folder contains source code only (no personal data, no trained model binaries, no generated datasets).

---

## What it does

### Dashboard features
- **Income & expense analysis** with interactive charts
- **Financial health score prediction** (0–100)
- **Risk classification** (Low / Medium / High)
- **Forecast-style projections** for upcoming months (expenses + savings direction)
- **AI recommendation engine**: rule-based + pattern insights (self-contained, no external AI services)

### Advanced logic included
- Feature engineering with financial ratios:
  - `savings_ratio`, `expense_ratio`, `debt_to_income_ratio`, `investment_ratio`
- Custom risk scoring + classification
- Country configuration (benchmarks + currency formatting)

---

## Tech stack
- Python
- pandas, numpy
- scikit-learn, XGBoost
- plotly (dashboard charts)
- Streamlit (UI)

---

## Repository safety notes
To keep the repo safe and lightweight:
- Generated data (`data/*.csv`) is ignored.
- Trained models (`models/*.pkl`) are ignored.
- Virtual environments (`venv/`) are ignored.
- No secrets are stored in the repo.

Pickle files should never be downloaded from unknown sources and executed. Models are trained locally after cloning.

---

## Project structure
