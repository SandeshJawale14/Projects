"""
Main Training Pipeline
Orchestrates complete model training workflow
"""

import sys
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from src.data_generator import FinancialDataGenerator
from src.feature_engineer import FinancialFeatureEngineer
from src.preprocessor import FinancialDataPreprocessor
from src.model_trainer import FinancialModelTrainer
import config

class FinSightTrainingPipeline:
    """Complete end-to-end training pipeline"""
    
    def __init__(self):
        self.data_generator = FinancialDataGenerator()
        self.feature_engineer = FinancialFeatureEngineer()
        self.preprocessor = FinancialDataPreprocessor()
        self.model_trainer = FinancialModelTrainer()
        
        self.raw_data = None
        self.engineered_data = None
        
    def step1_generate_data(self):
        """Step 1: Generate synthetic financial data"""
        print("\n" + "="*70)
        print("STEP 1: DATA GENERATION")
        print("="*70)
        
        if config.RAW_DATA_PATH.exists():
            user_input = input("Raw data already exists. Regenerate? (y/n): ")
            if user_input.lower() != 'y':
                print("Loading existing data...")
                self.raw_data = pd.read_csv(config.RAW_DATA_PATH)
                print(f"✅ Loaded {len(self.raw_data)} records")
                return
        
        self.raw_data = self.data_generator.generate_complete_dataset()
        self.data_generator.save_data(self.raw_data)
        
        print("\n📊 Data Summary:")
        print(self.raw_data[['monthly_income', 'total_expenses', 'savings', 'credit_score']].describe())
        
    def step2_feature_engineering(self):
        """Step 2: Engineer features"""
        print("\n" + "="*70)
        print("STEP 2: FEATURE ENGINEERING")
        print("="*70)
        
        self.engineered_data = self.feature_engineer.engineer_all_features(self.raw_data)
        self.engineered_data.to_csv(config.PROCESSED_DATA_PATH, index=False)
        
        print("\n📊 Sample Engineered Features:")
        feature_cols = ['savings_ratio', 'debt_to_income_ratio', 'financial_health_score', 'risk_category']
        print(self.engineered_data[feature_cols].head())
        
        print("\n📈 Risk Category Distribution:")
        print(self.engineered_data['risk_category'].value_counts())
        
    def step3_train_models(self):
        """Step 3: Train all models"""
        print("\n" + "="*70)
        print("STEP 3: MODEL TRAINING")
        print("="*70)
        
        # Model 1: Risk Classification
        print("\n" + "-"*70)
        print("Training Model 1: Risk Classifier")
        print("-"*70)
        
        X_risk, y_risk, _ = self.preprocessor.full_preprocessing_pipeline(
            self.engineered_data.copy(),
            target_col='risk_category',
            fit=True
        )
        
        if 'risk_score' in X_risk.columns:
            X_risk = X_risk.drop('risk_score', axis=1)
        
        X_train_risk, X_test_risk, y_train_risk, y_test_risk = train_test_split(
            X_risk, y_risk, test_size=0.2, random_state=config.RANDOM_STATE, stratify=y_risk
        )
        
        risk_model, risk_accuracy = self.model_trainer.train_risk_classifier(
            X_train_risk, y_train_risk, X_test_risk, y_test_risk
        )
        
        print("\n🔍 Top 10 Features for Risk Prediction:")
        importance = self.model_trainer.metrics['risk_classifier']['feature_importance'].head(10)
        print(importance.to_string(index=False))
        
        # Model 2: Financial Health Score
        print("\n" + "-"*70)
        print("Training Model 2: Financial Health Predictor")
        print("-"*70)
        
        preprocessor_health = FinancialDataPreprocessor()
        
        X_health, y_health, _ = preprocessor_health.full_preprocessing_pipeline(
            self.engineered_data.copy(),
            target_col='financial_health_score',
            fit=True
        )
        
        X_train_health, X_test_health, y_train_health, y_test_health = train_test_split(
            X_health, y_health, test_size=0.2, random_state=config.RANDOM_STATE
        )
        
        health_model, health_mae = self.model_trainer.train_health_predictor(
            X_train_health, y_train_health, X_test_health, y_test_health
        )
        
        print("\n🔍 Top 10 Features for Health Score:")
        importance = self.model_trainer.metrics['health_predictor']['feature_importance'].head(10)
        print(importance.to_string(index=False))
        
        # Model 3: Expense Forecasting
        print("\n" + "-"*70)
        print("Training Model 3: Expense Forecaster")
        print("-"*70)
        
        preprocessor_expense = FinancialDataPreprocessor()
        
        X_expense, y_expense, _ = preprocessor_expense.full_preprocessing_pipeline(
            self.engineered_data.copy(),
            target_col='total_expenses',
            fit=True
        )
        
        X_train_expense, X_test_expense, y_train_expense, y_test_expense = train_test_split(
            X_expense, y_expense, test_size=0.2, random_state=config.RANDOM_STATE
        )
        
        expense_model, expense_mae = self.model_trainer.train_expense_forecaster(
            X_train_expense, y_train_expense, X_test_expense, y_test_expense
        )
        
        print("\n🔍 Top 10 Features for Expense Prediction:")
        importance = self.model_trainer.metrics['expense_forecaster']['feature_importance'].head(10)
        print(importance.to_string(index=False))
        
    def step4_save_artifacts(self):
        """Step 4: Save all models and preprocessors"""
        print("\n" + "="*70)
        print("STEP 4: SAVING ARTIFACTS")
        print("="*70)
        
        self.model_trainer.save_models()
        self.preprocessor.save_preprocessor()
        
        print("✅ All artifacts saved successfully")
        
    def step5_generate_report(self):
        """Step 5: Generate training summary report"""
        print("\n" + "="*70)
        print("STEP 5: TRAINING SUMMARY")
        print("="*70)
        
        report = f"""
╔════════════════════════════════════════════════════════════════════╗
║                    FINSIGHT AI TRAINING REPORT                     ║
╚════════════════════════════════════════════════════════════════════╝

📅 Training Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 Dataset Size: {len(self.engineered_data)} records
🔢 Total Features: {len(self.engineered_data.columns)}

┌────────────────────────────────────────────────────────────────────┐
│ MODEL PERFORMANCE METRICS                                          │
└────────────────────────────────────────────────────────────────────┘

1️⃣  RISK CLASSIFIER (XGBoost)
   • Accuracy: {self.model_trainer.metrics['risk_classifier']['accuracy']:.4f}
   • Macro F1: {self.model_trainer.metrics['risk_classifier']['classification_report']['macro avg']['f1-score']:.4f}
   
2️⃣  HEALTH PREDICTOR (XGBoost)
   • MAE: {self.model_trainer.metrics['health_predictor']['mae']:.2f} points
   • R² Score: {self.model_trainer.metrics['health_predictor']['r2_score']:.4f}
   
3️⃣  EXPENSE FORECASTER (Random Forest)
   • MAE: ${self.model_trainer.metrics['expense_forecaster']['mae']:.2f}
   • MAPE: {self.model_trainer.metrics['expense_forecaster']['mape']:.2f}%

┌────────────────────────────────────────────────────────────────────┐
│ NEXT STEPS                                                         │
└────────────────────────────────────────────────────────────────────┘

🚀 Run: streamlit run app.py
📊 Models are ready for deployment

        """
        
        print(report)
        
    def run_complete_pipeline(self):
        """Execute complete training pipeline"""
        try:
            self.step1_generate_data()
            self.step2_feature_engineering()
            self.step3_train_models()
            self.step4_save_artifacts()
            self.step5_generate_report()
            
            print("\n" + "="*70)
            print("🎉 TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
            print("="*70)
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()


def main():
    """Main execution function"""
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║              🚀 FINSIGHT AI TRAINING PIPELINE 🚀               ║
    ║                                                                ║
    ║         Intelligent Financial Advisor System - Training       ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    pipeline = FinSightTrainingPipeline()
    pipeline.run_complete_pipeline()


if __name__ == "__main__":
    main()