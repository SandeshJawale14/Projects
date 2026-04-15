"""
FinSight AI - Global Multi-Currency Financial Advisor
Complete production-ready version with enhanced AI recommendations
Supports users from any country with localized currency and benchmarks
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import joblib
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.feature_engineer import FinancialFeatureEngineer
from src.preprocessor import FinancialDataPreprocessor
from src.recommender import FinancialRecommendationEngine
from src.utils import VisualizationUtils, DataUtils
import config

# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="FinSight AI - Global Financial Advisor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== GLOBAL CSS (ULTRA MODERN) ====================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%); }
    ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #667eea 0%, #764ba2 100%); border-radius: 10px; }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
    }
    
    .main-header {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        animation: gradientShift 8s ease infinite;
        padding: 2rem;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 45px 0 rgba(102, 126, 234, 0.4);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        transition: all 0.4s;
        cursor: pointer;
    }
    
    .metric-card:hover {
        transform: scale(1.05) translateY(-10px);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.6);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        border-radius: 50px;
        padding: 1rem 3rem;
        transition: all 0.4s;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.6);
    }
    
    .country-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        font-weight: 700;
        margin: 1rem 0;
    }
    
    .insight-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid;
        backdrop-filter: blur(10px);
    }
    
    .insight-critical {
        background: rgba(231, 76, 60, 0.1);
        border-left-color: #e74c3c;
    }
    
    .insight-warning {
        background: rgba(243, 156, 18, 0.1);
        border-left-color: #f39c12;
    }
    
    .insight-success {
        background: rgba(46, 204, 113, 0.1);
        border-left-color: #2ecc71;
    }
    
    .insight-opportunity {
        background: rgba(52, 152, 219, 0.1);
        border-left-color: #3498db;
    }
</style>
""", unsafe_allow_html=True)

# ==================== MAIN APP CLASS ====================

class GlobalFinSightApp:
    """Global Multi-Currency Financial Advisor"""
    
    def __init__(self):
        self.initialize_session_state()
        self.load_models()
        self.feature_engineer = FinancialFeatureEngineer()
        self.preprocessor = FinancialDataPreprocessor()
        self.recommender = FinancialRecommendationEngine()
        self.viz = VisualizationUtils()
        
        try:
            self.preprocessor.load_preprocessor()
        except:
            pass
    
    def initialize_session_state(self):
        """Initialize session state"""
        defaults = {
            'analyzed': False,
            'user_data': None,
            'user_features': None,
            'predictions': None,
            'country': 'India',
            'currency': 'INR'
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @st.cache_resource
    def load_models(_self):
        """Load trained models"""
        try:
            return {
                'risk_classifier': joblib.load(config.RISK_MODEL_PATH),
                'health_predictor': joblib.load(config.HEALTH_MODEL_PATH),
                'expense_forecaster': joblib.load(config.FORECAST_MODEL_PATH)
            }
        except FileNotFoundError:
            st.error("⚠️ Models not found! Run `python train.py` first.")
            st.stop()
    
    def render_header(self):
        """Render header with country info"""
        st.markdown('<h1 class="main-header">🌍 FinSight AI Global</h1>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="text-align: center;">
                <p style="color: #a8b2d1; font-size: 1.3rem;">
                    ✨ Your Next-Generation AI Financial Advisor ✨
                </p>
                <span class="country-badge">
                    📍 {st.session_state.country} | {config.CURRENCIES[st.session_state.currency]['symbol']} {config.CURRENCIES[st.session_state.currency]['name']}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    def render_sidebar(self):
        """Render modern sidebar"""
        st.sidebar.markdown("## 🌍 Location & Currency")
        
        country = st.sidebar.selectbox(
            "🗺️ Select Your Country",
            list(config.COUNTRY_CONFIG.keys()),
            index=list(config.COUNTRY_CONFIG.keys()).index(st.session_state.country)
        )
        
        country_config = config.COUNTRY_CONFIG[country]
        default_currency = country_config['currency']
        
        currency = st.sidebar.selectbox(
            "💱 Currency",
            list(config.CURRENCIES.keys()),
            index=list(config.CURRENCIES.keys()).index(default_currency)
        )
        
        st.session_state.country = country
        st.session_state.currency = currency
        
        st.sidebar.info(f"""
        **Country Settings:**
        - Recommended Savings: {country_config['savings_target']*100:.0f}%
        - Tax Rate: {country_config['tax_rate']*100:.0f}%
        - Cost of Living Index: {country_config['cost_of_living_index']}
        """)
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("## 📊 Financial Profile")
        
        min_income, max_income = country_config['avg_income_range']
        
        with st.sidebar.expander("👤 Personal Details", expanded=True):
            age = st.slider("🎂 Age", 18, 70, 30)
            employment = st.selectbox("💼 Employment", ["Full-time", "Part-time", "Self-employed"])
            dependents = st.number_input("👨‍👩‍👧‍👦 Dependents", 0, 10, 0)
            credit_score = st.slider("💳 Credit Score", 300, 850, 700)
        
        with st.sidebar.expander("💵 Income Sources", expanded=True):
            monthly_income = st.number_input(
                f"💰 Monthly Income ({config.CURRENCIES[currency]['symbol']})",
                0, int(max_income * 2), int(min_income), int(min_income/10)
            )
            additional_income = st.number_input(
                f"➕ Additional Income ({config.CURRENCIES[currency]['symbol']})",
                0, int(max_income), 0, int(min_income/10)
            )
            total_income = monthly_income + additional_income
            st.success(f"**Total:** {DataUtils.format_currency(total_income, currency)}")
        
        with st.sidebar.expander("💳 Monthly Expenses", expanded=True):
            rent = st.number_input(
                f"🏠 Rent/Mortgage ({config.CURRENCIES[currency]['symbol']})",
                0, int(max_income), int(monthly_income * 0.3), int(min_income/10)
            )
            groceries = st.number_input(
                f"🛒 Groceries ({config.CURRENCIES[currency]['symbol']})",
                0, int(max_income/5), int(monthly_income * 0.1), int(min_income/20)
            )
            utilities = st.number_input(
                f"💡 Utilities ({config.CURRENCIES[currency]['symbol']})",
                0, int(max_income/10), int(monthly_income * 0.05), int(min_income/20)
            )
            transportation = st.number_input(
                f"🚗 Transportation ({config.CURRENCIES[currency]['symbol']})",
                0, int(max_income/5), int(monthly_income * 0.08), int(min_income/20)
            )
            entertainment = st.number_input(
                f"🎬 Entertainment ({config.CURRENCIES[currency]['symbol']})",
                0, int(max_income/5), int(monthly_income * 0.05), int(min_income/20)
            )
        
        with st.sidebar.expander("🏦 Debt & Obligations", expanded=True):
            loan_payments = st.number_input(
                f"💳 Loan Payments ({config.CURRENCIES[currency]['symbol']})",
                0, int(max_income), int(monthly_income * 0.1), int(min_income/10)
            )
            credit_card_debt = st.number_input(
                f"💰 Credit Card Debt ({config.CURRENCIES[currency]['symbol']})",
                0, int(max_income * 10), int(monthly_income * 0.5), int(min_income)
            )
        
        with st.sidebar.expander("💎 Savings & Investments", expanded=True):
            savings = st.number_input(
                f"💵 Monthly Savings ({config.CURRENCIES[currency]['symbol']})",
                0, int(max_income), int(monthly_income * 0.2), int(min_income/20)
            )
            emergency_fund = st.number_input(
                f"🆘 Emergency Fund ({config.CURRENCIES[currency]['symbol']})",
                0, int(max_income * 20), int(monthly_income * 3), int(min_income)
            )
            investments = st.number_input(
                f"📈 Total Investments ({config.CURRENCIES[currency]['symbol']})",
                0, int(max_income * 50), int(monthly_income * 5), int(min_income)
            )
        
        total_expenses = rent + groceries + utilities + transportation + entertainment + loan_payments
        
        return {
            'country': country,
            'currency': currency,
            'age': age,
            'employment_type': employment,
            'dependents': dependents,
            'credit_score': credit_score,
            'monthly_income': monthly_income,
            'additional_income': additional_income,
            'total_income': total_income,
            'rent': rent,
            'groceries': groceries,
            'utilities': utilities,
            'transportation': transportation,
            'entertainment': entertainment,
            'loan_payments': loan_payments,
            'credit_card_debt': credit_card_debt,
            'savings': savings,
            'emergency_fund': emergency_fund,
            'investments': investments,
            'total_expenses': total_expenses
        }
    
    def engineer_user_features(self, user_data):
        """Engineer features"""
        df = pd.DataFrame([user_data])
        df['user_id'] = 'USER_INPUT'
        df['created_date'] = datetime.now().strftime('%Y-%m-%d')
        df_engineered = self.feature_engineer.engineer_all_features(df)
        return df_engineered.iloc[0].to_dict()
    
    def make_predictions(self, user_features_dict):
        """Make predictions"""
        df = pd.DataFrame([user_features_dict])
        
        try:
            X, _, _ = self.preprocessor.full_preprocessing_pipeline(df.copy(), fit=False)
            
            if hasattr(self.preprocessor, 'feature_names') and self.preprocessor.feature_names:
                missing_cols = set(self.preprocessor.feature_names) - set(X.columns)
                for col in missing_cols:
                    X[col] = 0
                X = X[self.preprocessor.feature_names]
            
            risk_pred = self.load_models()['risk_classifier'].predict(X)[0]
            risk_proba = self.load_models()['risk_classifier'].predict_proba(X)[0]
            risk_labels = ['Low Risk', 'Medium Risk', 'High Risk']
            
            health_score = self.load_models()['health_predictor'].predict(X)[0]
            expense_forecast = self.load_models()['expense_forecaster'].predict(X)[0]
            
            return {
                'risk_category': risk_labels[risk_pred],
                'risk_probabilities': {label: prob for label, prob in zip(risk_labels, risk_proba)},
                'predicted_health_score': max(0, min(100, health_score)),
                'forecasted_expenses': max(0, expense_forecast)
            }
        except Exception as e:
            st.error(f"Prediction error: {str(e)}")
            return {
                'risk_category': 'Medium Risk',
                'risk_probabilities': {'Low Risk': 0.33, 'Medium Risk': 0.34, 'High Risk': 0.33},
                'predicted_health_score': 50,
                'forecasted_expenses': user_features_dict.get('total_expenses', 0)
            }
    
    def render_overview_tab(self):
        """Render overview with animations"""
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.header("📊 Financial Dashboard")
        
        user_data = st.session_state.user_data
        user_features = st.session_state.user_features
        predictions = st.session_state.predictions
        currency = user_data['currency']
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("💵 Monthly Income", DataUtils.format_currency(user_data['total_income'], currency))
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("💳 Expenses", DataUtils.format_currency(user_data['total_expenses'], currency))
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            monthly_savings = user_data['total_income'] - user_data['total_expenses']
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("💰 Net Savings", DataUtils.format_currency(monthly_savings, currency))
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col4:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("🆘 Emergency Fund", DataUtils.format_currency(user_data['emergency_fund'], currency))
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Health Score & Risk
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("🎯 Financial Health Score")
            health_score = user_features.get('financial_health_score', 50)
            gauge_fig = self.viz.create_gauge_chart(health_score, "Health Score")
            st.plotly_chart(gauge_fig, use_container_width=True)
            
            interpretation, message = DataUtils.health_score_interpretation(health_score)
            if health_score >= 75:
                st.success(f"**{interpretation}**: {message}")
            elif health_score >= 50:
                st.info(f"**{interpretation}**: {message}")
            else:
                st.warning(f"**{interpretation}**: {message}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("⚠️ Risk Assessment")
            
            if not predictions or 'risk_category' not in predictions:
                st.error("⚠️ Risk data not available")
            else:
                risk_category = predictions.get('risk_category', 'Unknown')
                risk_color = DataUtils.risk_category_color(risk_category)
                
                st.markdown(f"""
                <div style="background: {risk_color}; padding: 30px; border-radius: 15px; 
                            text-align: center; color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                    <h1 style="margin: 0; font-size: 2.5rem;">{risk_category}</h1>
                    <p style="margin-top: 10px; opacity: 0.9;">Based on AI Analysis</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**📊 Risk Probability Distribution**")
                
                risk_probs = predictions.get('risk_probabilities', {})
                if risk_probs:
                    for label, prob in risk_probs.items():
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.progress(prob, text=label)
                        with col_b:
                            st.markdown(f"**{prob:.1%}**")
                else:
                    st.info("Risk probabilities not available")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Charts
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("💸 Expense Breakdown")
            expense_fig = self.viz.create_financial_breakdown_chart(user_data)
            st.plotly_chart(expense_fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("📈 Financial Ratios")
            
            country_config = config.COUNTRY_CONFIG[user_data['country']]
            
            ratios = {
                'Your Savings': user_features.get('savings_ratio', 0),
                f"Target ({user_data['country']})": country_config['savings_target'],
                'Debt-to-Income': user_features.get('debt_to_income_ratio', 0),
                'Expense Ratio': user_features.get('expense_ratio', 0)
            }
            
            fig = go.Figure(go.Bar(
                x=list(ratios.values()),
                y=list(ratios.keys()),
                orientation='h',
                marker=dict(color=['#2ecc71', '#3498db', '#e74c3c', '#f39c12'])
            ))
            
            fig.update_layout(
                xaxis_title="Ratio",
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    def render_recommendations_tab(self):
        """Render enhanced AI recommendations"""
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.header("🤖 AI-Powered Financial Recommendations")
        
        user_features = st.session_state.user_features
        user_data = st.session_state.user_data
        
        # AI Insights (NEW!)
        with st.spinner("🧠 AI is analyzing patterns..."):
            insights = self.recommender.generate_ai_insights(user_features)
        
        if insights:
            st.subheader("💡 AI Pattern Analysis")
            for insight in insights:
                css_class = f"insight-{insight['type']}"
                st.markdown(f"""
                <div class="insight-card {css_class}">
                    <strong>{insight['title']}</strong><br>
                    {insight['message']}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Country-specific advice
        country_config = config.COUNTRY_CONFIG[user_data['country']]
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.info(f"""
        **📍 {user_data['country']}-Specific Financial Advice:**
        - 🎯 Target Savings Rate: {country_config['savings_target']*100:.0f}%
        - 📊 Your Current Rate: {user_features.get('savings_ratio', 0)*100:.1f}%
        - 💰 Tax Considerations: {country_config['tax_rate']*100:.0f}% effective rate
        - 📈 Cost of Living Index: {country_config['cost_of_living_index']}
        """)
        
        # Country-specific recommendations
        country_recs = self.recommender.get_country_specific_recommendations(user_data['country'])
        if country_recs:
            st.markdown("**🌍 Country-Specific Strategies:**")
            for rec in country_recs[:3]:
                st.success(rec)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Generate recommendations
        recommendations = self.recommender.generate_recommendations(user_features)
        analysis = self.recommender.analyze_financial_profile(user_features)
        
        # SWOT Analysis
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📋 SWOT Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Strengths")
            if analysis.get('strengths'):
                for s in analysis['strengths']:
                    st.success(s)
            else:
                st.info("Build your financial strengths!")
            
            st.markdown("### 🎯 Opportunities")
            if analysis.get('opportunities'):
                for o in analysis['opportunities']:
                    st.info(o)
            else:
                st.info("Focus on current priorities")
        
        with col2:
            st.markdown("### ⚠️ Weaknesses")
            if analysis.get('weaknesses'):
                for w in analysis['weaknesses']:
                    st.warning(w)
            else:
                st.success("No major weaknesses!")
            
            st.markdown("### 🚨 Threats")
            if analysis.get('threats'):
                for t in analysis['threats']:
                    st.error(t)
            else:
                st.success("No threats detected!")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Detailed Action Plan (Enhanced)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📝 Personalized Action Plan")
        st.markdown("*AI-generated recommendations ranked by priority and impact*")
        
        for i, rec in enumerate(recommendations[:8], 1):
            priority_emoji = "🔴" if rec['priority'] <= 2 else "🟡" if rec['priority'] <= 4 else "🟢"
            
            with st.expander(
                f"{priority_emoji} Priority {rec['priority']}: {rec['category']}", 
                expanded=(i <= 3)
            ):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**💡 Recommendation:**")
                    st.info(rec['recommendation'])
                    
                    st.markdown(f"**🎯 Action Step:**")
                    st.success(rec['action'])
                    
                    st.markdown(f"**📊 Expected Impact:** {rec['impact']}")
                
                with col2:
                    st.metric("Timeline", rec.get('timeline', 'Varies'))
                    st.metric("Difficulty", rec.get('difficulty', 'Medium'))
                    
                    priority_score = (9 - rec['priority']) / 8 * 100
                    st.progress(priority_score / 100, text=f"Priority: {priority_score:.0f}%")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_forecast_tab(self):
        """Render forecast"""
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.header("🔮 Financial Forecast & Projections")
        
        user_data = st.session_state.user_data
        predictions = st.session_state.predictions
        currency = user_data['currency']
        
        current_expenses = user_data['total_expenses']
        forecasted_expenses = predictions.get('forecasted_expenses', current_expenses)
        
        historical_data = DataUtils.generate_time_series_data(current_expenses, num_months=12)
        
        future_dates = pd.date_range(start=datetime.now() + timedelta(days=30), periods=6, freq='ME')
        forecast_data = pd.DataFrame({
            'date': future_dates,
            'value': [forecasted_expenses * (1.015 ** i) for i in range(6)],
            'lower_bound': [forecasted_expenses * (1.015 ** i) * 0.92 for i in range(6)],
            'upper_bound': [forecasted_expenses * (1.015 ** i) * 1.08 for i in range(6)]
        })
        
        forecast_fig = self.viz.create_forecast_chart(historical_data, forecast_data, f"Monthly Expenses ({currency})")
        st.plotly_chart(forecast_fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current", DataUtils.format_currency(current_expenses, currency))
        with col2:
            st.metric("6-Month Forecast", DataUtils.format_currency(forecast_data['value'].iloc[-1], currency))
        with col3:
            st.metric("Total (6mo)", DataUtils.format_currency(forecast_data['value'].sum(), currency))
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Savings Projection
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📈 Savings Growth Projection")
        
        monthly_savings = user_data['total_income'] - user_data['total_expenses']
        months = list(range(1, 37))
        cumulative = [monthly_savings * m for m in months]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months, y=cumulative, mode='lines+markers',
            fill='tozeroy', name='Savings',
            line=dict(color='#2ecc71', width=3),
            marker=dict(size=6, color='#2ecc71')
        ))
        
        fig.update_layout(
            title="36-Month Savings Projection",
            xaxis_title="Months",
            yaxis_title=f"Cumulative Savings ({currency})",
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Milestones
        col1, col2, col3, col4 = st.columns(4)
        milestones = [6, 12, 24, 36]
        labels = ["6 Months", "1 Year", "2 Years", "3 Years"]
        
        for col, months_val, label in zip([col1, col2, col3, col4], milestones, labels):
            with col:
                st.metric(label, DataUtils.format_currency(monthly_savings * months_val, currency))
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_welcome_screen(self):
        """Render welcome screen"""
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <h2>🌍 Welcome to FinSight AI Global!</h2>
                <p style="font-size: 1.2rem; color: #a8b2d1;">
                    Financial advice tailored to your country & currency
                </p>
                <br>
                <p style="color: #a8b2d1;">
                    Select your country in the sidebar and enter your financial details to get started!
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Feature highlights
        col1, col2, col3 = st.columns(3)
        
        cards = [
            ("🎯", "Health Score", "AI-calculated financial health (0-100)"),
            ("💡", "Smart Advice", "8+ categories of personalized recommendations"),
            ("🔮", "AI Predictions", "Pattern analysis & future forecasts")
        ]
        
        for col, (icon, title, desc) in zip([col1, col2, col3], cards):
            with col:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; padding: 2rem;">
                    <h1>{icon}</h1>
                    <h3>{title}</h3>
                    <p style="color: #a8b2d1;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
    
    def run(self):
        """Main app execution"""
        self.render_header()
        
        user_data = self.render_sidebar()
        
        st.sidebar.markdown("---")
        analyze_button = st.sidebar.button("🚀 Analyze My Finances", type="primary", use_container_width=True)
        
        if analyze_button:
            if user_data['total_income'] == 0:
                st.error("⚠️ Please enter your income.")
                return
            
            with st.spinner("🤖 AI is analyzing your financial profile..."):
                user_features = self.engineer_user_features(user_data)
                predictions = self.make_predictions(user_features)
                
                st.session_state.user_data = user_data
                st.session_state.user_features = user_features
                st.session_state.predictions = predictions
                st.session_state.analyzed = True
                
                st.success("✅ Analysis complete!")
                st.rerun()
        
        if st.session_state.analyzed:
            tabs = st.tabs(["📊 Dashboard", "💡 Recommendations", "🔮 Forecast"])
            
            with tabs[0]:
                self.render_overview_tab()
            
            with tabs[1]:
                self.render_recommendations_tab()
            
            with tabs[2]:
                self.render_forecast_tab()
        else:
            self.render_welcome_screen()
        
        # Footer
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; color: #a8b2d1; padding: 2rem;">
            <h3>🌍 FinSight AI Global</h3>
            <p>Supporting users from {len(config.COUNTRY_CONFIG)} countries worldwide</p>
            <p style="font-size: 0.9rem; margin-top: 1rem;">
                Built with ❤️ using Python • Streamlit • XGBoost • Machine Learning
            </p>
            <p style="font-size: 0.8rem; color: #667eea; margin-top: 1rem;">
                🤖 Powered by Self-Contained AI Engine • No External Dependencies
            </p>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Entry point"""
    try:
        app = GlobalFinSightApp()
        app.run()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()