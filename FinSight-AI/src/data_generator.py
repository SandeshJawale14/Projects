"""
Synthetic Financial Data Generator
Creates realistic financial profiles for training
"""

import numpy as np
import pandas as pd
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config

class FinancialDataGenerator:
    """Generates synthetic but realistic financial data"""
    
    def __init__(self, num_samples=config.NUM_SAMPLES, random_state=config.RANDOM_STATE):
        self.num_samples = num_samples
        self.random_state = random_state
        np.random.seed(random_state)
        
    def generate_income_data(self):
        """Generate income data with realistic distribution"""
        monthly_income = np.random.lognormal(mean=8.5, sigma=0.6, size=self.num_samples)
        monthly_income = np.clip(monthly_income, 2500, 15000)
        
        has_additional = np.random.choice([0, 1], size=self.num_samples, p=[0.8, 0.2])
        additional_income = has_additional * np.random.gamma(2, 300, size=self.num_samples)
        
        return monthly_income, additional_income
    
    def generate_expense_data(self, monthly_income):
        """Generate expenses correlated with income"""
        rent = monthly_income * np.random.uniform(0.25, 0.35, size=self.num_samples)
        groceries = np.random.normal(400, 100, size=self.num_samples).clip(200, 1000)
        utilities = np.random.normal(150, 50, size=self.num_samples).clip(80, 400)
        transportation = monthly_income * np.random.uniform(0.05, 0.15, size=self.num_samples)
        entertainment = monthly_income * np.random.uniform(0.03, 0.10, size=self.num_samples)
        
        return {
            'rent': rent,
            'groceries': groceries,
            'utilities': utilities,
            'transportation': transportation,
            'entertainment': entertainment
        }
    
    def generate_debt_data(self, monthly_income):
        """Generate debt obligations"""
        has_loan = np.random.choice([0, 1], size=self.num_samples, p=[0.3, 0.7])
        loan_payments = has_loan * monthly_income * np.random.uniform(0.1, 0.25, size=self.num_samples)
        
        has_cc_debt = np.random.choice([0, 1], size=self.num_samples, p=[0.4, 0.6])
        credit_card_debt = has_cc_debt * np.random.gamma(2, 200, size=self.num_samples)
        
        return loan_payments, credit_card_debt
    
    def generate_savings_data(self, monthly_income, total_expenses):
        """Generate savings based on income and expenses"""
        potential_savings = monthly_income - total_expenses
        savings_efficiency = np.random.beta(5, 2, size=self.num_samples)
        savings = np.maximum(0, potential_savings * savings_efficiency)
        
        emergency_fund = total_expenses * np.random.uniform(1, 6, size=self.num_samples)
        
        invests = np.random.choice([0, 1], size=self.num_samples, p=[0.5, 0.5])
        investments = invests * savings * np.random.uniform(0.3, 0.7, size=self.num_samples)
        
        return savings, emergency_fund, investments
    
    def generate_demographics(self):
        """Generate demographic information"""
        ages = np.random.normal(35, 10, size=self.num_samples).clip(22, 65).astype(int)
        employment_types = np.random.choice(
            ['Full-time', 'Part-time', 'Self-employed'],
            size=self.num_samples,
            p=[0.75, 0.15, 0.10]
        )
        dependents = np.random.choice([0, 1, 2, 3], size=self.num_samples, p=[0.3, 0.3, 0.25, 0.15])
        credit_scores = np.random.normal(700, 80, size=self.num_samples).clip(500, 850).astype(int)
        
        return ages, employment_types, dependents, credit_scores
    
    def generate_complete_dataset(self):
        """Generate complete financial dataset"""
        print("🔄 Generating synthetic financial data...")
        
        monthly_income, additional_income = self.generate_income_data()
        total_income = monthly_income + additional_income
        
        expenses = self.generate_expense_data(monthly_income)
        total_expenses = sum(expenses.values())
        
        loan_payments, credit_card_debt = self.generate_debt_data(monthly_income)
        total_expenses += loan_payments
        
        savings, emergency_fund, investments = self.generate_savings_data(total_income, total_expenses)
        ages, employment_types, dependents, credit_scores = self.generate_demographics()
        
        df = pd.DataFrame({
            'user_id': [f'USER_{i:05d}' for i in range(self.num_samples)],
            'age': ages,
            'employment_type': employment_types,
            'dependents': dependents,
            'credit_score': credit_scores,
            'monthly_income': monthly_income,
            'additional_income': additional_income,
            'total_income': total_income,
            'rent': expenses['rent'],
            'groceries': expenses['groceries'],
            'utilities': expenses['utilities'],
            'transportation': expenses['transportation'],
            'entertainment': expenses['entertainment'],
            'total_expenses': total_expenses,
            'loan_payments': loan_payments,
            'credit_card_debt': credit_card_debt,
            'savings': savings,
            'emergency_fund': emergency_fund,
            'investments': investments,
            'created_date': datetime.now().strftime('%Y-%m-%d')
        })
        
        print(f"✅ Generated {len(df)} financial records")
        return df
    
    def save_data(self, df, filepath=config.RAW_DATA_PATH):
        """Save generated data to CSV"""
        df.to_csv(filepath, index=False)
        print(f"💾 Data saved to {filepath}")


if __name__ == "__main__":
    generator = FinancialDataGenerator()
    df = generator.generate_complete_dataset()
    generator.save_data(df)