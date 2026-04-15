"""
Multi-Model Training Pipeline
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    classification_report, confusion_matrix, 
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score
)
from xgboost import XGBClassifier, XGBRegressor
import joblib
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config

class FinancialModelTrainer:
    """Trains multiple models for different financial prediction tasks"""
    
    def __init__(self):
        self.models = {}
        self.metrics = {}
        
    def train_risk_classifier(self, X_train, y_train, X_test, y_test):
        """Train risk classification model"""
        print("\n🎯 Training Risk Classification Model...")
        
        risk_mapping = {'Low Risk': 0, 'Medium Risk': 1, 'High Risk': 2}
        y_train_encoded = y_train.map(risk_mapping)
        y_test_encoded = y_test.map(risk_mapping)
        
        model = XGBClassifier(
            **config.RISK_CLASSIFIER_PARAMS,
            objective='multi:softmax',
            num_class=3,
            eval_metric='mlogloss'
        )
        
        model.fit(
            X_train, y_train_encoded,
            eval_set=[(X_test, y_test_encoded)],
            verbose=False
        )
        
        y_pred = model.predict(X_test)
        y_pred_labels = [list(risk_mapping.keys())[i] for i in y_pred]
        
        accuracy = accuracy_score(y_test, y_pred_labels)
        report = classification_report(y_test, y_pred_labels, output_dict=True)
        
        print(f"  ✓ Accuracy: {accuracy:.4f}")
        print(f"  ✓ Macro F1-Score: {report['macro avg']['f1-score']:.4f}")
        
        feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        self.models['risk_classifier'] = model
        self.metrics['risk_classifier'] = {
            'accuracy': accuracy,
            'classification_report': report,
            'feature_importance': feature_importance
        }
        
        return model, accuracy
    
    def train_health_predictor(self, X_train, y_train, X_test, y_test):
        """Train financial health score predictor"""
        print("\n📊 Training Financial Health Predictor...")
        
        model = XGBRegressor(
            **config.HEALTH_PREDICTOR_PARAMS,
            objective='reg:squarederror'
        )
        
        model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            verbose=False
        )
        
        y_pred = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        print(f"  ✓ MAE: {mae:.2f} points")
        print(f"  ✓ RMSE: {rmse:.2f}")
        print(f"  ✓ R² Score: {r2:.4f}")
        
        feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        self.models['health_predictor'] = model
        self.metrics['health_predictor'] = {
            'mae': mae,
            'rmse': rmse,
            'r2_score': r2,
            'feature_importance': feature_importance
        }
        
        return model, mae
    
    def train_expense_forecaster(self, X_train, y_train, X_test, y_test):
        """Train expense forecasting model"""
        print("\n💰 Training Expense Forecaster...")
        
        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            random_state=config.RANDOM_STATE,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        
        print(f"  ✓ MAE: ${mae:.2f}")
        print(f"  ✓ RMSE: ${rmse:.2f}")
        print(f"  ✓ MAPE: {mape:.2f}%")
        print(f"  ✓ R² Score: {r2:.4f}")
        
        feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        self.models['expense_forecaster'] = model
        self.metrics['expense_forecaster'] = {
            'mae': mae,
            'rmse': rmse,
            'mape': mape,
            'r2_score': r2,
            'feature_importance': feature_importance
        }
        
        return model, mae
    
    def save_models(self):
        """Save all trained models"""
        joblib.dump(self.models['risk_classifier'], config.RISK_MODEL_PATH)
        joblib.dump(self.models['health_predictor'], config.HEALTH_MODEL_PATH)
        joblib.dump(self.models['expense_forecaster'], config.FORECAST_MODEL_PATH)
        print("\n💾 All models saved successfully")
    
    def load_models(self):
        """Load saved models"""
        self.models['risk_classifier'] = joblib.load(config.RISK_MODEL_PATH)
        self.models['health_predictor'] = joblib.load(config.HEALTH_MODEL_PATH)
        self.models['expense_forecaster'] = joblib.load(config.FORECAST_MODEL_PATH)
        