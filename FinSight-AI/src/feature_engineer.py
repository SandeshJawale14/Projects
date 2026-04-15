"""
Advanced Feature Engineering for Financial Analysis
"""

import numpy as np
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config

class FinancialFeatureEngineer:
    """Feature engineering for financial data"""
    
    def __init__(self):
        self.feature_names = []
        
    def create_ratio_features(self, df):
        """Create financial ratio features"""
        df = df.copy()
        
        df['savings_ratio'] = (df['savings'] / df['total_income']).clip(0, 1)
        
        total_debt = df['loan_payments'] + (df['credit_card_debt'] * 0.03)
        df['debt_to_income_ratio'] = (total_debt / df['total_income']).clip(0, 1)
        
        df['expense_ratio'] = (df['total_expenses'] / df['total_income']).clip(0, 1.5)
        
        df['emergency_fund_months'] = (df['emergency_fund'] / (df['total_expenses'] + 1)).clip(0, 12)
        
        df['discretionary_ratio'] = (df['entertainment'] / df['total_income']).clip(0, 1)
        
        if 'investments' not in df.columns:
            df['investments'] = 0
        df['investment_ratio'] = (df['investments'] / df['total_income']).clip(0, 1)
        
        return df
    
    def create_financial_health_score(self, df):
        """Create composite financial health score (0-100)"""
        df = df.copy()
        
        savings_score = np.clip(df['savings_ratio'] * 100 / 0.3, 0, 100)
        debt_score = np.clip(100 - (df['debt_to_income_ratio'] * 100 / 0.5), 0, 100)
        emergency_score = np.clip(df['emergency_fund_months'] * 100 / 6, 0, 100)
        credit_score_norm = (df['credit_score'] - 500) / 350 * 100
        
        df['financial_health_score'] = (
            savings_score * 0.30 +
            debt_score * 0.25 +
            emergency_score * 0.20 +
            credit_score_norm * 0.25
        ).clip(0, 100)
        
        return df
    
    def create_risk_category(self, df):
        """Create risk classification"""
        df = df.copy()
        
        risk_score = np.zeros(len(df))
        
        risk_score += np.where(df['debt_to_income_ratio'] > 0.43, 3,
                              np.where(df['debt_to_income_ratio'] > 0.36, 2, 1))
        
        risk_score += np.where(df['savings_ratio'] < 0.05, 3,
                              np.where(df['savings_ratio'] < 0.15, 2, 1))
        
        risk_score += np.where(df['emergency_fund_months'] < 1, 3,
                              np.where(df['emergency_fund_months'] < 3, 2, 1))
        
        df['risk_category'] = ['Low Risk' if score <= 5 else 'Medium Risk' if score <= 7 else 'High Risk' 
                               for score in risk_score]
        
        df['risk_score'] = risk_score
        
        return df
    
    def engineer_all_features(self, df):
        """Apply all feature engineering transformations"""
        print("🔧 Engineering financial features...")
        
        df = self.create_ratio_features(df)
        print("  ✓ Ratio features created")
        
        df = self.create_financial_health_score(df)
        print("  ✓ Health score computed")
        
        df = self.create_risk_category(df)
        print("  ✓ Risk categories assigned")
        
        print(f"✅ Feature engineering complete. Total features: {len(df.columns)}")
        
        return df


if __name__ == "__main__":
    df = pd.read_csv(config.RAW_DATA_PATH)
    engineer = FinancialFeatureEngineer()
    df_engineered = engineer.engineer_all_features(df)
    df_engineered.to_csv(config.PROCESSED_DATA_PATH, index=False)