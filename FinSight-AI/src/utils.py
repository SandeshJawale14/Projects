"""
Utility functions for FinSight AI
Helper functions for visualization, formatting, and common operations
FINAL CORRECTED VERSION
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config

sns.set_style("whitegrid")

# ==================== VISUALIZATION UTILITIES ====================

class VisualizationUtils:
    """Visualization utilities for financial data"""
    
    @staticmethod
    def create_gauge_chart(value, title, min_val=0, max_val=100):
        """Create gauge chart for financial health score"""
        if value >= 75:
            color = 'green'
        elif value >= 50:
            color = 'orange'
        else:
            color = 'red'
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title, 'font': {'size': 24, 'color': 'white'}},
            delta={'reference': 70},
            gauge={
                'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': 'white'},
                'bar': {'color': color},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "rgba(255,255,255,0.3)",
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(231, 76, 60, 0.3)'},
                    {'range': [50, 75], 'color': 'rgba(243, 156, 18, 0.3)'},
                    {'range': [75, 100], 'color': 'rgba(46, 204, 113, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        return fig
    
    @staticmethod
    def create_financial_breakdown_chart(user_data):
        """Create pie chart of expense breakdown"""
        expense_categories = {
            'Rent': user_data.get('rent', 0),
            'Groceries': user_data.get('groceries', 0),
            'Utilities': user_data.get('utilities', 0),
            'Transportation': user_data.get('transportation', 0),
            'Entertainment': user_data.get('entertainment', 0),
            'Loan Payments': user_data.get('loan_payments', 0)
        }
        
        expense_categories = {k: v for k, v in expense_categories.items() if v > 0}
        
        fig = px.pie(
            values=list(expense_categories.values()),
            names=list(expense_categories.keys()),
            title='Monthly Expense Breakdown',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12
        )
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            showlegend=True,
            legend=dict(
                font=dict(color='white'),
                bgcolor='rgba(255,255,255,0.1)'
            )
        )
        
        return fig
    
    @staticmethod
    def create_forecast_chart(historical_data, forecast_data, metric_name):
        """Create forecast visualization with confidence intervals"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=historical_data['date'],
            y=historical_data['value'],
            mode='lines+markers',
            name='Historical',
            line=dict(color='#3498db', width=3),
            marker=dict(size=8, color='#3498db')
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_data['date'],
            y=forecast_data['value'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#e74c3c', width=3, dash='dash'),
            marker=dict(size=8, color='#e74c3c')
        ))
        
        if 'lower_bound' in forecast_data.columns and 'upper_bound' in forecast_data.columns:
            fig.add_trace(go.Scatter(
                x=forecast_data['date'],
                y=forecast_data['upper_bound'],
                mode='lines',
                name='Upper Bound',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast_data['date'],
                y=forecast_data['lower_bound'],
                mode='lines',
                name='Confidence Interval',
                fill='tonexty',
                fillcolor='rgba(231, 76, 60, 0.2)',
                line=dict(width=0),
                showlegend=True
            ))
        
        fig.update_layout(
            title=f'{metric_name} Forecast',
            xaxis_title='Date',
            yaxis_title=metric_name,
            hovermode='x unified',
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                color='white'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                color='white'
            ),
            legend=dict(
                font=dict(color='white'),
                bgcolor='rgba(255,255,255,0.1)'
            )
        )
        
        return fig


# ==================== DATA UTILITIES ====================

class DataUtils:
    """Data manipulation utilities with multi-currency support"""
    
    @staticmethod
    def format_currency(amount, currency='USD', country=None):
        """Format number as currency based on country/currency"""
        if currency in config.CURRENCIES:
            symbol = config.CURRENCIES[currency]['symbol']
            
            if currency == 'INR':
                if amount >= 10000000:
                    return f"{symbol}{amount/10000000:.2f} Cr"
                elif amount >= 100000:
                    return f"{symbol}{amount/100000:.2f} L"
                else:
                    return f"{symbol}{amount:,.2f}"
            
            elif currency == 'JPY':
                return f"{symbol}{amount:,.0f}"
            
            return f"{symbol}{amount:,.2f}"
        
        return f"${amount:,.2f}"
    
    @staticmethod
    def convert_currency(amount, from_currency, to_currency):
        """Convert amount between currencies"""
        if from_currency == to_currency:
            return amount
        
        usd_amount = amount / config.CURRENCIES.get(from_currency, {}).get('rate', 1.0)
        target_amount = usd_amount * config.CURRENCIES.get(to_currency, {}).get('rate', 1.0)
        
        return target_amount
    
    @staticmethod
    def get_country_adjusted_threshold(base_threshold, country):
        """Get country-adjusted financial thresholds"""
        country_config = config.COUNTRY_CONFIG.get(country, config.COUNTRY_CONFIG['United States'])
        col_index = country_config['cost_of_living_index']
        
        return base_threshold * col_index
    
    @staticmethod
    def format_percentage(value):
        """Format decimal as percentage"""
        return f"{value * 100:.1f}%"
    
    @staticmethod
    def format_large_number(number, currency='USD'):
        """Format large numbers with K, M, B suffixes"""
        if currency == 'INR':
            if number >= 10000000:
                return f"₹{number/10000000:.2f} Cr"
            elif number >= 100000:
                return f"₹{number/100000:.2f} L"
            else:
                return f"₹{number:,.0f}"
        else:
            if number >= 1000000000:
                return f"${number/1000000000:.2f}B"
            elif number >= 1000000:
                return f"${number/1000000:.2f}M"
            elif number >= 1000:
                return f"${number/1000:.2f}K"
            else:
                return f"${number:,.2f}"
    
    @staticmethod
    def generate_time_series_data(base_value, num_months=12, trend=0.02, seasonality=0.1):
        """
        Generate synthetic time series for forecasting demo
        FINAL CORRECTED VERSION - Guaranteed to work
        
        Args:
            base_value: Base value for time series
            num_months: Number of months to generate
            trend: Monthly growth rate
            seasonality: Seasonal variation amplitude
            
        Returns:
            DataFrame with 'date' and 'value' columns
        """
        # Create exact number of dates using list comprehension
        # WHY: Manual creation ensures exact length match
        base_date = datetime.now()
        dates = [base_date - timedelta(days=30*(num_months-i-1)) for i in range(num_months)]
        
        # Create time index array
        time_index = np.arange(num_months)
        
        # Trend component (exponential growth)
        # WHY: Financial metrics typically show exponential trends
        trend_component = base_value * (1 + trend) ** time_index
        
        # Seasonal component (annual cycle)
        # WHY: Expenses show seasonal patterns (holidays, summer, etc.)
        seasonal_component = base_value * seasonality * np.sin(time_index * 2 * np.pi / 12)
        
        # Random noise (realistic variation)
        # WHY: Real data has random fluctuations
        np.random.seed(42)  # Reproducible randomness
        noise = np.random.normal(0, base_value * 0.05, num_months)
        
        # Combine all components
        values = trend_component + seasonal_component + noise
        
        # Ensure no negative values (expenses can't be negative)
        values = np.maximum(values, 0)
        
        # Create DataFrame
        df = pd.DataFrame({
            'date': dates,
            'value': values
        })
        
        return df
    
    @staticmethod
    def risk_category_color(category):
        """Return color for risk category"""
        color_map = {
            'Low Risk': '#2ecc71',
            'Medium Risk': '#f39c12',
            'High Risk': '#e74c3c'
        }
        return color_map.get(category, '#95a5a6')
    
    @staticmethod
    def health_score_interpretation(score):
        """Interpret health score"""
        if score >= 80:
            return "Excellent", "Your financial health is outstanding! 🌟"
        elif score >= 65:
            return "Good", "Solid financial foundation with room for optimization. 👍"
        elif score >= 50:
            return "Fair", "Some areas need attention. Follow recommendations. ⚠️"
        else:
            return "Needs Improvement", "Immediate action required to improve financial stability. 🚨"
    
    @staticmethod
    def calculate_payoff_months(principal, monthly_payment, annual_rate):
        """Calculate months needed to pay off debt"""
        if monthly_payment <= 0:
            return float('inf')
        
        monthly_rate = annual_rate / 12
        
        if monthly_rate == 0:
            return principal / monthly_payment
        
        if monthly_payment <= principal * monthly_rate:
            return float('inf')
        
        months = -np.log(1 - (principal * monthly_rate / monthly_payment)) / np.log(1 + monthly_rate)
        
        return months
    
    @staticmethod
    def calculate_compound_interest(principal, monthly_contribution, annual_rate, years):
        """Calculate compound interest growth"""
        months = years * 12
        monthly_rate = annual_rate / 12
        
        future_value = principal * (1 + monthly_rate) ** months
        
        if monthly_rate > 0:
            future_value += monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        else:
            future_value += monthly_contribution * months
        
        total_invested = principal + (monthly_contribution * months)
        gains = future_value - total_invested
        
        return {
            'future_value': future_value,
            'total_invested': total_invested,
            'gains': gains,
            'roi_percentage': (gains / total_invested * 100) if total_invested > 0 else 0
        }


# ==================== REPORT GENERATOR ====================

class ReportGenerator:
    """Generate financial reports"""
    
    @staticmethod
    def generate_summary_report(user_data, predictions, recommendations):
        """Generate comprehensive financial summary report"""
        report = {
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'country': user_data.get('country', 'Not specified'),
            'currency': user_data.get('currency', 'USD'),
            'user_profile': {
                'income': user_data.get('total_income', 0),
                'expenses': user_data.get('total_expenses', 0),
                'savings': user_data.get('savings', 0),
                'debt': user_data.get('loan_payments', 0) + user_data.get('credit_card_debt', 0)
            },
            'key_metrics': {
                'savings_ratio': user_data.get('savings_ratio', 0),
                'debt_to_income': user_data.get('debt_to_income_ratio', 0),
                'expense_ratio': user_data.get('expense_ratio', 0)
            },
            'predictions': predictions,
            'top_recommendations': recommendations[:3] if recommendations else []
        }
        
        return report


if __name__ == "__main__":
    print("✅ Utility functions loaded successfully")
    
    # Test time series generation
    print("\n🧪 Testing time series generation...")
    try:
        test_data = DataUtils.generate_time_series_data(5000, num_months=12)
        print(f"✅ Generated {len(test_data)} time series points")
        print(f"📅 Date range: {test_data['date'].min()} to {test_data['date'].max()}")
        print(f"💰 Value range: ${test_data['value'].min():.2f} to ${test_data['value'].max():.2f}")
        print("\n📊 Sample data:")
        print(test_data.head())
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()