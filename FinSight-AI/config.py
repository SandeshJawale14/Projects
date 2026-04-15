"""
Configuration file for FinSight AI - Multi-Country Version
Supports multiple currencies and regional financial standards
"""

import os
from pathlib import Path

# Project Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
MODEL_DIR = BASE_DIR / 'models'

# Create directories
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, MODEL_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# File Paths
RAW_DATA_PATH = RAW_DATA_DIR / 'financial_data.csv'
PROCESSED_DATA_PATH = PROCESSED_DATA_DIR / 'processed_financial_data.csv'
RISK_MODEL_PATH = MODEL_DIR / 'risk_classifier.pkl'
HEALTH_MODEL_PATH = MODEL_DIR / 'health_predictor.pkl'
FORECAST_MODEL_PATH = MODEL_DIR / 'expense_forecaster.pkl'
SCALER_PATH = MODEL_DIR / 'scaler.pkl'

# Data Generation Parameters
NUM_SAMPLES = 3000
RANDOM_STATE = 42

# Model Hyperparameters
RISK_CLASSIFIER_PARAMS = {
    'n_estimators': 200,
    'max_depth': 10,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'random_state': RANDOM_STATE
}

HEALTH_PREDICTOR_PARAMS = {
    'n_estimators': 150,
    'max_depth': 8,
    'learning_rate': 0.05,
    'random_state': RANDOM_STATE
}

# ==================== MULTI-CURRENCY CONFIGURATION ====================

CURRENCIES = {
    'USD': {'symbol': '$', 'name': 'US Dollar', 'rate': 1.0},
    'EUR': {'symbol': '€', 'name': 'Euro', 'rate': 0.92},
    'GBP': {'symbol': '£', 'name': 'British Pound', 'rate': 0.79},
    'INR': {'symbol': '₹', 'name': 'Indian Rupee', 'rate': 83.12},
    'AED': {'symbol': 'د.إ', 'name': 'UAE Dirham', 'rate': 3.67},
    'CAD': {'symbol': 'C$', 'name': 'Canadian Dollar', 'rate': 1.36},
    'AUD': {'symbol': 'A$', 'name': 'Australian Dollar', 'rate': 1.53},
    'SGD': {'symbol': 'S$', 'name': 'Singapore Dollar', 'rate': 1.35},
    'JPY': {'symbol': '¥', 'name': 'Japanese Yen', 'rate': 149.50},
    'CNY': {'symbol': '¥', 'name': 'Chinese Yuan', 'rate': 7.24}
}

# ==================== COUNTRY-SPECIFIC CONFIGURATIONS ====================

COUNTRY_CONFIG = {
    'United States': {
        'currency': 'USD',
        'avg_income_range': (3000, 12000),
        'rent_percentage': (25, 35),
        'savings_target': 0.20,
        'emergency_months': 6,
        'tax_rate': 0.25,
        'cost_of_living_index': 1.0
    },
    'India': {
        'currency': 'INR',
        'avg_income_range': (30000, 200000),
        'rent_percentage': (20, 30),
        'savings_target': 0.25,
        'emergency_months': 6,
        'tax_rate': 0.20,
        'cost_of_living_index': 0.35
    },
    'United Kingdom': {
        'currency': 'GBP',
        'avg_income_range': (2500, 10000),
        'rent_percentage': (30, 40),
        'savings_target': 0.15,
        'emergency_months': 6,
        'tax_rate': 0.30,
        'cost_of_living_index': 1.15
    },
    'UAE': {
        'currency': 'AED',
        'avg_income_range': (10000, 50000),
        'rent_percentage': (25, 35),
        'savings_target': 0.30,
        'emergency_months': 6,
        'tax_rate': 0.00,
        'cost_of_living_index': 1.05
    },
    'Canada': {
        'currency': 'CAD',
        'avg_income_range': (4000, 15000),
        'rent_percentage': (25, 35),
        'savings_target': 0.20,
        'emergency_months': 6,
        'tax_rate': 0.28,
        'cost_of_living_index': 0.95
    },
    'Australia': {
        'currency': 'AUD',
        'avg_income_range': (5000, 18000),
        'rent_percentage': (25, 35),
        'savings_target': 0.20,
        'emergency_months': 6,
        'tax_rate': 0.27,
        'cost_of_living_index': 1.10
    },
    'Singapore': {
        'currency': 'SGD',
        'avg_income_range': (4000, 20000),
        'rent_percentage': (20, 30),
        'savings_target': 0.30,
        'emergency_months': 6,
        'tax_rate': 0.18,
        'cost_of_living_index': 1.25
    }
}

# Financial Thresholds
SAVINGS_RATIO_THRESHOLD = {
    'excellent': 0.30,
    'good': 0.20,
    'moderate': 0.10,
    'poor': 0.05
}

DEBT_TO_INCOME_THRESHOLD = {
    'low_risk': 0.20,
    'medium_risk': 0.35,
    'high_risk': 0.50
}

EXPENSE_RATIO_THRESHOLD = {
    'conservative': 0.50,
    'moderate': 0.70,
    'aggressive': 0.90
}

# Feature Groups
FEATURE_GROUPS = {
    'income_features': ['monthly_income', 'additional_income', 'total_income'],
    'expense_features': ['rent', 'groceries', 'utilities', 'entertainment', 
                        'transportation', 'total_expenses'],
    'savings_features': ['savings', 'emergency_fund', 'investments'],
    'debt_features': ['loan_payments', 'credit_card_debt'],
    'ratio_features': ['savings_ratio', 'debt_to_income_ratio', 'expense_ratio', 'investment_ratio']
}

# Risk Categories
RISK_LABELS = ['Low Risk', 'Medium Risk', 'High Risk']