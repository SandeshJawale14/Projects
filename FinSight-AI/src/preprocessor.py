"""
Data Preprocessing Pipeline
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config

class FinancialDataPreprocessor:
    """Data preprocessing for financial data"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = None
        
    def handle_missing_values(self, df):
        """Handle missing values"""
        df = df.copy()
        
        numeric_features = df.select_dtypes(include=[np.number]).columns
        for col in numeric_features:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].median())
        
        categorical_features = df.select_dtypes(include=['object']).columns
        for col in categorical_features:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].mode()[0])
        
        return df
    
    def encode_categorical_features(self, df, fit=True):
        """Encode categorical variables"""
        df = df.copy()
        
        categorical_columns = ['employment_type']
        
        for col in categorical_columns:
            if col in df.columns:
                if fit:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
                else:
                    if col in self.label_encoders:
                        df[col] = self.label_encoders[col].transform(df[col].astype(str))
        
        return df
    
    def create_feature_matrix(self, df, target_col=None):
        """Create feature matrix for modeling"""
        exclude_cols = ['user_id', 'created_date', 'risk_category']
        
        if target_col:
            exclude_cols.append(target_col)
        
        feature_cols = [col for col in df.columns 
                       if col not in exclude_cols and df[col].dtype in [np.float64, np.int64]]
        
        X = df[feature_cols]
        self.feature_names = feature_cols
        
        if target_col and target_col in df.columns:
            y = df[target_col]
            return X, y
        
        return X
    
    def scale_features(self, X, fit=True):
        """Scale features using StandardScaler"""
        if fit:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        return pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
    
    def full_preprocessing_pipeline(self, df, target_col=None, fit=True):
        """Complete preprocessing pipeline"""
        print("🔄 Starting preprocessing pipeline...")
        
        df = self.handle_missing_values(df)
        print("  ✓ Missing values handled")
        
        df = self.encode_categorical_features(df, fit=fit)
        print("  ✓ Categorical features encoded")
        
        if target_col:
            X, y = self.create_feature_matrix(df, target_col=target_col)
            print(f"  ✓ Feature matrix created: {X.shape}")
        else:
            X = self.create_feature_matrix(df)
            y = None
            print(f"  ✓ Feature matrix created: {X.shape}")
        
        X_scaled = self.scale_features(X, fit=fit)
        print("  ✓ Features scaled")
        
        print("✅ Preprocessing complete\n")
        
        return X_scaled, y, df
    
    def save_preprocessor(self, filepath=config.SCALER_PATH):
        """Save scaler and encoders"""
        joblib.dump({
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names
        }, filepath)
        print(f"💾 Preprocessor saved to {filepath}")
    
    def load_preprocessor(self, filepath=config.SCALER_PATH):
        """Load saved preprocessor"""
        saved_objects = joblib.load(filepath)
        self.scaler = saved_objects['scaler']
        self.label_encoders = saved_objects['label_encoders']
        self.feature_names = saved_objects['feature_names']
        print(f"📂 Preprocessor loaded from {filepath}")