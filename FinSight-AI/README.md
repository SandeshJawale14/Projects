# FinSight AI – Intelligent Financial Advisor System

A production-style **machine learning + analytics dashboard** that helps users understand cashflow, predict financial health, classify risk, and receive actionable recommendations — all in one place.

FinSight AI is designed like a real fintech prototype: modular codebase, feature-engineered financial ratios, trained ML models, and a Streamlit UI that supports **multi-country + multi-currency** usage.

> This folder contains **source code only** (no personal data, no trained model binaries, no generated datasets).

---

## Highlights (Why this project matters)

- **End-to-end ML pipeline**: synthetic dataset → feature engineering → preprocessing → training → evaluation → model export
- **Real financial logic**: ratios + rule-driven signals instead of random “toy” suggestions
- **Multi-country ready**: currency formatting + localized savings benchmarks
- **Safe repo design**: excludes generated datasets + pickle artifacts from version control

---

## What the system does

### 1) Financial dashboard (Streamlit)
- Income vs expenses overview
- Expense category breakdown
- Financial ratio bar charts
- Financial health score gauge (0–100)
- Risk label + probability distribution (Low / Medium / High)

### 2) ML predictions
- **Financial Health Prediction (Regression)**  
  Predicts a normalized wellness score using engineered features and spending patterns.
- **Risk Classification (Multi-class)**  
  Classifies users into Low/Medium/High risk based on engineered ratios + learned patterns.
- **Expense Forecasting (Regression)**  
  Estimates future expenses (and supports projection charts in UI).

### 3) AI recommendation engine (self-contained)
- Rule-based recommendations + pattern insights (no external AI APIs)
- Priority-based action plan (emergency fund, debt, savings, investment, etc.)
- Country-specific tips for selected regions (where configured)

---

## Key features (advanced)

### Feature engineering
Derived indicators used in scoring & modeling:
- `savings_ratio`
- `expense_ratio`
- `debt_to_income_ratio`
- `investment_ratio`
- `emergency_fund_months`
- `risk_score` (rule-driven risk signals)

### Custom risk scoring (domain-driven)
Risk is not purely “model magic”. The system blends:
- Debt burden thresholds (DTI rules)
- Savings rate benchmarks
- Emergency fund coverage
- Expense pressure signals

### Multi-currency + multi-country support
- Country selection influences benchmarks (e.g., recommended savings target)
- Currency formatting included (e.g., INR lakh/crore formatting)

---

## Tech stack

**Core**
- Python
- pandas, numpy

**ML**
- scikit-learn
- XGBoost

**Visualization**
- plotly
- matplotlib / seaborn (training/EDA support)

**App**
- Streamlit

---

## Project structure

```text
FinSight-AI/
├── app.py                      # Streamlit dashboard
├── train.py                    # End-to-end training pipeline
├── config.py                   # Paths, thresholds, country/currency config
├── requirements.txt
├── README.md
└── src/
    ├── __init__.py
    ├── data_generator.py       # Synthetic dataset generation
    ├── feature_engineer.py     # Financial ratios + risk scoring
    ├── preprocessor.py         # Encoding, scaling, feature selection
    ├── model_trainer.py        # Train/evaluate models
    ├── recommender.py          # AI recommendation engine (self-contained)
    └── utils.py                # Formatting + charts + helpers
