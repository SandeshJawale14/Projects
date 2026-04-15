"""
Enhanced AI-Powered Financial Recommendation Engine
Advanced recommendations using pattern matching and financial rules
"""

import numpy as np
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config

class FinancialRecommendationEngine:
    """
    Advanced AI recommendation system with multi-dimensional analysis
    Uses rule-based AI combined with pattern recognition
    """
    
    def __init__(self):
        self.recommendation_database = self._build_recommendation_database()
        
    def _build_recommendation_database(self):
        """Build comprehensive recommendation database"""
        return {
            'emergency_fund': {
                'critical': [
                    "🚨 **URGENT**: Build emergency fund immediately. Start with $1,000 baseline.",
                    "⚠️ **High Priority**: Set up automatic transfer of 10% income to emergency savings.",
                    "💡 **Quick Win**: Cut one non-essential expense and redirect to emergency fund."
                ],
                'low': [
                    "⚠️ **Action Needed**: Your emergency fund covers less than 2 months. Aim for 3-6 months.",
                    "📊 **Target**: Build emergency fund to cover {months} months of expenses.",
                    "💰 **Strategy**: Allocate {amount} per month to reach 6-month coverage in 1 year."
                ],
                'moderate': [
                    "✅ **Good Progress**: You have {months} months covered. Aim for 6 months.",
                    "📈 **Enhancement**: Consider high-yield savings account for emergency fund.",
                    "🎯 **Goal**: Increase emergency fund by {percentage}% over next 6 months."
                ]
            },
            'debt_management': {
                'high': [
                    "🔴 **Critical Debt Level**: Debt-to-income ratio is {dti}%. Immediate action required.",
                    "💳 **Debt Avalanche**: Focus on highest interest rate debt first (typically credit cards).",
                    "📉 **Consolidation**: Consider debt consolidation loan if rate is below {current_rate}%.",
                    "⚡ **Quick Impact**: Pay extra ${amount} toward debt monthly to reduce payoff time by {months} months.",
                    "🎯 **Target**: Reduce DTI to below 36% within 12 months."
                ],
                'medium': [
                    "⚠️ **Debt Optimization**: Your DTI is {dti}%. Industry standard recommends below 36%.",
                    "💡 **Balance Transfer**: Explore 0% APR balance transfer cards for credit card debt.",
                    "📊 **Snowball Method**: Pay off smallest debt first for psychological wins.",
                    "🔄 **Refinancing**: Check if you can refinance high-interest loans at lower rates."
                ],
                'low': [
                    "✅ **Healthy Debt Level**: DTI of {dti}% is well-managed.",
                    "📈 **Optimization**: Consider extra payments to save on interest long-term.",
                    "💰 **Investment vs Debt**: With low debt, focus more on investing for higher returns."
                ]
            },
            'savings_optimization': {
                'poor': [
                    "🚨 **Savings Alert**: Current savings rate is {rate}%. Aim for minimum 15-20%.",
                    "💡 **Pay Yourself First**: Set up automatic transfer on payday to savings account.",
                    "📊 **Expense Audit**: Review subscriptions and recurring charges - cut unused services.",
                    "🎯 **Challenge**: Increase savings rate by 1% each month for next 6 months.",
                    "💰 **Side Income**: Consider freelancing or part-time work to boost savings."
                ],
                'moderate': [
                    "📈 **Good Start**: {rate}% savings rate is solid. Push toward 20-25% for excellence.",
                    "🔄 **Automation**: Automate savings increases with each raise or bonus.",
                    "💡 **Tax Advantage**: Max out tax-advantaged accounts (401k, IRA) first.",
                    "🎯 **Goal**: Reach {target}% savings rate within 12 months."
                ],
                'excellent': [
                    "🌟 **Outstanding**: {rate}% savings rate is excellent! You're wealth-building.",
                    "📈 **Next Level**: Focus on optimizing investment allocation for growth.",
                    "💎 **Tax Efficiency**: Review tax-loss harvesting and Roth conversions.",
                    "🎯 **Wealth Building**: Consider real estate or business investment opportunities."
                ]
            },
            'investment_strategy': {
                'beginner': [
                    "📚 **Start Simple**: Begin with low-cost index funds (S&P 500, Total Market).",
                    "🎯 **401(k) First**: Contribute enough to get full employer match (free money!).",
                    "💰 **Roth IRA**: Open Roth IRA and contribute ${amount} monthly.",
                    "📊 **Diversification**: Follow 60/40 stocks/bonds allocation for balanced growth.",
                    "⏰ **Time is Power**: Starting now gives you {years} years of compound growth."
                ],
                'intermediate': [
                    "📈 **Portfolio Review**: Rebalance portfolio quarterly to maintain target allocation.",
                    "💎 **Tax Optimization**: Use tax-loss harvesting to offset capital gains.",
                    "🌍 **International Exposure**: Add 20-30% international stocks for diversification.",
                    "🏠 **Real Estate**: Consider REITs for real estate exposure without buying property.",
                    "🎯 **Target**: Aim for {target_percentage}% portfolio growth over next 3 years."
                ],
                'advanced': [
                    "🚀 **Alternative Investments**: Explore opportunities in private equity or startups.",
                    "💼 **Business Ventures**: Your financial foundation supports entrepreneurship.",
                    "🌐 **Geographic Diversification**: Consider international real estate or assets.",
                    "📊 **Advanced Strategies**: Use options for income generation (covered calls).",
                    "🎯 **Wealth Preservation**: Focus on asset protection and estate planning."
                ]
            },
            'tax_optimization': {
                'strategies': [
                    "💰 **Tax-Advantaged Accounts**: Max out 401(k) (${k401_limit}) and IRA (${ira_limit}).",
                    "📊 **HSA Triple Tax Advantage**: If eligible, max out HSA - tax deductible, grows tax-free, withdraws tax-free.",
                    "🎯 **Capital Gains**: Hold investments >1 year for lower long-term capital gains tax.",
                    "💡 **Tax-Loss Harvesting**: Offset gains with losses to reduce taxable income.",
                    "🏠 **Homeownership**: Mortgage interest and property tax deductions if applicable.",
                    "📈 **Roth Conversion**: Consider Roth IRA conversion in low-income years."
                ]
            },
            'lifestyle_optimization': {
                'high_discretionary': [
                    "⚠️ **Lifestyle Inflation**: Discretionary spending is {percentage}% of income - aim for <15%.",
                    "💡 **30-Day Rule**: Wait 30 days before purchases over ${amount}.",
                    "📱 **Subscription Audit**: Cancel unused subscriptions (average person wastes $200/month).",
                    "🎯 **Challenge**: Reduce discretionary spending by 20% for 3 months.",
                    "💰 **Redirect Savings**: Put 50% of spending cuts toward investments."
                ],
                'balanced': [
                    "✅ **Balanced Lifestyle**: Your discretionary spending is well-controlled.",
                    "📊 **Optimization**: Look for value optimization (better deals on same items).",
                    "💡 **Mindful Spending**: Continue tracking expenses to maintain awareness.",
                    "🎯 **Upgrade**: With controlled spending, focus on income growth."
                ]
            },
            'income_growth': {
                'strategies': [
                    "🚀 **Career Advancement**: Negotiate raise or seek promotion (avg increase: 10-20%).",
                    "💼 **Side Income**: Start freelancing in your expertise area.",
                    "📚 **Skill Development**: Invest in courses that increase earning potential.",
                    "🌐 **Passive Income**: Create digital products, courses, or rental income streams.",
                    "🎯 **Target**: Increase income by {percentage}% within 12 months.",
                    "💡 **Job Market**: Update resume and explore market value (avg 20% increase when switching)."
                ]
            },
            'retirement_planning': {
                'age_based': {
                    '20s-30s': [
                        "⚡ **Time Advantage**: You have 30-40 years for compound growth - invest aggressively.",
                        "📈 **Target Allocation**: 80-90% stocks, 10-20% bonds for maximum growth.",
                        "🎯 **Retirement Goal**: Save 1x annual salary by age 30, 3x by age 40.",
                        "💰 **Minimum**: Contribute 15% of income to retirement accounts.",
                        "🚀 **Power of Starting Early**: $500/month at 25 = $1.2M at 65 (7% return)."
                    ],
                    '40s-50s': [
                        "⏰ **Critical Decade**: 40s-50s are peak earning years - maximize savings.",
                        "🎯 **Catch-Up**: If behind, you can contribute extra $7,500 to 401(k) after age 50.",
                        "📊 **Target Allocation**: 60-70% stocks, 30-40% bonds as you approach retirement.",
                        "💡 **Retirement Calculator**: Need ${target_amount} for ${desired_income}/month in retirement.",
                        "🏠 **Mortgage**: Consider paying off mortgage before retirement to reduce expenses."
                    ],
                    '50s-60s': [
                        "🎯 **Retirement Ready**: Focus on preservation and guaranteed income.",
                        "📉 **Risk Reduction**: Shift to 40-50% stocks, 50-60% bonds/fixed income.",
                        "💰 **Social Security**: Delay claiming until 70 for maximum benefit (8% increase/year).",
                        "🏥 **Healthcare**: Plan for Medicare gap coverage and long-term care insurance.",
                        "📊 **Withdrawal Strategy**: Plan 4% safe withdrawal rate from retirement portfolio."
                    ]
                }
            },
            'country_specific': {
                'India': [
                    "🇮🇳 **PPF/EPF**: Maximize Public Provident Fund contributions (tax-free returns).",
                    "💰 **Tax Saving**: Utilize Section 80C deductions (₹1.5L limit).",
                    "🏠 **Home Loan**: Take advantage of additional ₹2L deduction under Section 24(b).",
                    "📊 **ELSS Funds**: Invest in Equity Linked Savings Schemes for tax benefits + growth.",
                    "🎯 **NPS**: Consider National Pension System for retirement (extra ₹50K deduction)."
                ],
                'UAE': [
                    "🇦🇪 **Tax-Free Advantage**: No income tax - save/invest 40-50% of income.",
                    "💰 **Offshore Investment**: Set up offshore investment accounts for long-term wealth.",
                    "🏠 **Property**: Consider Dubai real estate for residency + rental income.",
                    "📊 **Gratuity Planning**: Factor in end-of-service gratuity in financial planning.",
                    "🎯 **Repatriation**: Plan for eventual home country return - currency considerations."
                ],
                'United States': [
                    "🇺🇸 **401(k) Match**: Contribute minimum 6% to get full employer match.",
                    "💰 **Roth IRA**: If eligible, contribute $7,000/year for tax-free growth.",
                    "📊 **HSA**: Triple tax advantage - contribute $4,150 (individual) or $8,300 (family).",
                    "🏠 **Mortgage Interest**: Deduct mortgage interest up to $750K loan.",
                    "🎯 **FIRE Movement**: Financial Independence Retire Early - save 50-70% income."
                ],
                'United Kingdom': [
                    "🇬🇧 **ISA Allowance**: Use full £20,000 ISA allowance for tax-free growth.",
                    "💰 **Pension Contributions**: Maximize workplace pension with employer match.",
                    "📊 **Lifetime ISA**: Get 25% government bonus on contributions (up to £4,000/year).",
                    "🏠 **Help to Buy**: First-time buyers - use government schemes.",
                    "🎯 **Tax Relief**: Get 20-45% tax relief on pension contributions."
                ],
                'Canada': [
                    "🇨🇦 **RRSP**: Maximize RRSP contributions for tax deduction.",
                    "💰 **TFSA**: Tax-Free Savings Account - $6,500/year contribution room.",
                    "📊 **RESP**: If you have children, use RESP for education savings (20% government grant).",
                    "🏠 **First Home Savings**: New FHSA allows tax-free saving for first home.",
                    "🎯 **Employer Match**: Contribute enough to get full employer RRSP match."
                ],
                'Australia': [
                    "🇦🇺 **Superannuation**: Salary sacrifice to super for tax savings.",
                    "💰 **Concessional Contributions**: Contribute up to $27,500/year pre-tax.",
                    "📊 **First Home Super Saver**: Use super to save for first home deposit.",
                    "🏠 **Negative Gearing**: If investing in property, understand negative gearing benefits.",
                    "🎯 **Government Co-contribution**: Earn up to $500 government match on super."
                ],
                'Singapore': [
                    "🇸🇬 **CPF Top-Up**: Maximize CPF Special/Retirement Account contributions.",
                    "💰 **SRS**: Supplementary Retirement Scheme for tax relief (up to $15,300/year).",
                    "📊 **CPF Investment Scheme**: Invest excess CPF for better returns.",
                    "🏠 **HDB Grant**: First-time buyers - utilize CPF Housing Grant.",
                    "🎯 **Tax Relief**: Utilize all available personal tax reliefs."
                ]
            }
        }
    
    def analyze_financial_profile(self, user_features):
        """Comprehensive SWOT analysis"""
        analysis = {
            'strengths': [],
            'weaknesses': [],
            'opportunities': [],
            'threats': []
        }
        
        # Extract metrics
        savings_ratio = user_features.get('savings_ratio', 0)
        dti = user_features.get('debt_to_income_ratio', 0)
        expense_ratio = user_features.get('expense_ratio', 0)
        emergency_months = user_features.get('emergency_fund_months', 0)
        health_score = user_features.get('financial_health_score', 0)
        discretionary_ratio = user_features.get('discretionary_ratio', 0)
        investment_ratio = user_features.get('investment_ratio', 0)
        
        # Strengths
        if savings_ratio > 0.20:
            analysis['strengths'].append(f"💪 Excellent savings rate of {savings_ratio*100:.1f}% (above 20% benchmark)")
        if dti < 0.20:
            analysis['strengths'].append(f"✅ Low debt burden - DTI of {dti*100:.1f}% is very healthy")
        if emergency_months >= 6:
            analysis['strengths'].append(f"🛡️ Robust emergency fund covering {emergency_months:.1f} months")
        if health_score >= 75:
            analysis['strengths'].append(f"🌟 Strong financial health score of {health_score:.0f}/100")
        if investment_ratio > 0.10:
            analysis['strengths'].append(f"📈 Good investment activity - {investment_ratio*100:.1f}% of income invested")
        
        # Weaknesses
        if savings_ratio < 0.10:
            analysis['weaknesses'].append(f"📉 Low savings rate ({savings_ratio*100:.1f}%) - aim for 20%+")
        if dti > 0.36:
            analysis['weaknesses'].append(f"⚠️ High debt burden ({dti*100:.1f}% DTI) - reduce to below 36%")
        if emergency_months < 3:
            analysis['weaknesses'].append(f"🚨 Insufficient emergency fund ({emergency_months:.1f} months) - need 3-6 months")
        if discretionary_ratio > 0.15:
            analysis['weaknesses'].append(f"💸 High discretionary spending ({discretionary_ratio*100:.1f}%) - optimize lifestyle costs")
        if expense_ratio > 0.75:
            analysis['weaknesses'].append(f"📊 High expense ratio ({expense_ratio*100:.1f}%) - living paycheck to paycheck")
        
        # Opportunities
        if savings_ratio < 0.15 and expense_ratio < 0.70:
            analysis['opportunities'].append("💡 Room to increase savings without major lifestyle changes")
        if dti < 0.30 and investment_ratio < 0.10:
            analysis['opportunities'].append("📈 Low debt enables higher investment allocation")
        if discretionary_ratio > 0.10:
            analysis['opportunities'].append("🎯 Opportunity to redirect discretionary spending to investments")
        if emergency_months >= 6:
            analysis['opportunities'].append("🚀 Strong emergency fund - ready for aggressive wealth building")
        
        # Threats
        if emergency_months == 0:
            analysis['threats'].append("🚨 No emergency fund - vulnerable to unexpected expenses")
        if dti > 0.43:
            analysis['threats'].append("⛔ Critical debt level - risk of financial distress")
        if savings_ratio < 0.05 and dti > 0.30:
            analysis['threats'].append("❌ Low savings + high debt = financial vulnerability")
        if expense_ratio > 0.90:
            analysis['threats'].append("⚠️ Extremely tight budget - no buffer for emergencies")
        
        return analysis
    
    def generate_recommendations(self, user_features):
        """Generate advanced AI-powered recommendations"""
        recommendations = []
        
        # Extract all metrics
        income = user_features.get('total_income', 1)
        expenses = user_features.get('total_expenses', 0)
        savings = user_features.get('savings', 0)
        savings_ratio = user_features.get('savings_ratio', 0)
        dti = user_features.get('debt_to_income_ratio', 0)
        emergency_months = user_features.get('emergency_fund_months', 0)
        discretionary_ratio = user_features.get('discretionary_ratio', 0)
        investment_ratio = user_features.get('investment_ratio', 0)
        health_score = user_features.get('financial_health_score', 0)
        age = user_features.get('age', 30)
        
        # Priority 1: Emergency Fund (if critical)
        if emergency_months < 1:
            target = expenses * 3
            monthly_needed = target / 12
            recommendations.append({
                'priority': 1,
                'category': '🆘 Emergency Fund - CRITICAL',
                'recommendation': self.recommendation_database['emergency_fund']['critical'][0],
                'action': f"Save ${monthly_needed:.0f}/month for 12 months to build 3-month emergency fund (${target:,.0f})",
                'impact': '🔴 CRITICAL - Protects against financial catastrophe',
                'timeline': '12 months',
                'difficulty': 'High'
            })
        elif emergency_months < 3:
            target = expenses * 6
            gap = target - (expenses * emergency_months)
            recommendations.append({
                'priority': 2,
                'category': '🛡️ Emergency Fund',
                'recommendation': self.recommendation_database['emergency_fund']['low'][0],
                'action': f"Increase emergency fund by ${gap:,.0f} to reach 6-month coverage",
                'impact': '🟡 HIGH - Essential financial safety net',
                'timeline': '18 months',
                'difficulty': 'Medium'
            })
        
        # Priority 2: High Debt
        if dti > 0.43:
            reduction_needed = (dti - 0.36) * income
            recommendations.append({
                'priority': 1 if emergency_months >= 1 else 2,
                'category': '💳 Debt Reduction - URGENT',
                'recommendation': self.recommendation_database['debt_management']['high'][0].format(dti=dti*100),
                'action': f"Reduce monthly debt payments by ${reduction_needed:.0f} using avalanche method",
                'impact': '🔴 CRITICAL - Reduce financial stress and interest costs',
                'timeline': '24-36 months',
                'difficulty': 'High'
            })
        elif dti > 0.36:
            recommendations.append({
                'priority': 3,
                'category': '📉 Debt Optimization',
                'recommendation': self.recommendation_database['debt_management']['medium'][0].format(dti=dti*100),
                'action': "Explore refinancing options and balance transfer cards",
                'impact': '🟡 MEDIUM - Save on interest and improve cash flow',
                'timeline': '12 months',
                'difficulty': 'Medium'
            })
        
        # Priority 3: Low Savings Rate
        if savings_ratio < 0.10:
            target_savings = income * 0.20
            increase_needed = target_savings - savings
            recommendations.append({
                'priority': 3,
                'category': '💰 Savings Acceleration',
                'recommendation': self.recommendation_database['savings_optimization']['poor'][0].format(rate=savings_ratio*100),
                'action': f"Increase monthly savings by ${increase_needed:.0f} to reach 20% savings rate",
                'impact': '🟡 HIGH - Build wealth and financial security',
                'timeline': '6-12 months (gradual increase)',
                'difficulty': 'Medium'
            })
        elif savings_ratio < 0.20:
            recommendations.append({
                'priority': 4,
                'category': '📈 Savings Enhancement',
                'recommendation': self.recommendation_database['savings_optimization']['moderate'][0].format(rate=savings_ratio*100),
                'action': "Increase savings rate by 1-2% monthly until reaching 20-25%",
                'impact': '🟢 MEDIUM - Accelerate wealth building',
                'timeline': '12 months',
                'difficulty': 'Low-Medium'
            })
        
        # Priority 4: High Discretionary Spending
        if discretionary_ratio > 0.15:
            reduction = income * (discretionary_ratio - 0.10)
            recommendations.append({
                'priority': 4,
                'category': '🎯 Lifestyle Optimization',
                'recommendation': self.recommendation_database['lifestyle_optimization']['high_discretionary'][0].format(percentage=discretionary_ratio*100),
                'action': f"Reduce discretionary spending by ${reduction:.0f}/month (audit subscriptions, dining out)",
                'impact': '🟢 MEDIUM - Redirect to savings/investments',
                'timeline': '3 months',
                'difficulty': 'Low'
            })
        
        # Priority 5: Investment Strategy
        if health_score >= 70 and savings_ratio >= 0.15 and investment_ratio < 0.15:
            invest_amount = income * 0.15
            recommendations.append({
                'priority': 5,
                'category': '📈 Investment Growth',
                'recommendation': self.recommendation_database['investment_strategy']['intermediate'][0],
                'action': f"Start investing ${invest_amount:.0f}/month in diversified index funds",
                'impact': '🟢 HIGH (Long-term) - Compound growth over time',
                'timeline': 'Ongoing (long-term)',
                'difficulty': 'Low'
            })
        
        # Priority 6: Tax Optimization
        if income > 5000:
            recommendations.append({
                'priority': 6,
                'category': '💼 Tax Strategy',
                'recommendation': self.recommendation_database['tax_optimization']['strategies'][0].format(
                    k401_limit='23,000',
                    ira_limit='7,000'
                ),
                'action': "Max out tax-advantaged accounts (401k, IRA, HSA) to reduce taxable income",
                'impact': '🟢 MEDIUM - Save 20-30% on taxes annually',
                'timeline': 'This tax year',
                'difficulty': 'Low'
            })
        
        # Priority 7: Income Growth
        if savings_ratio < 0.15 and expense_ratio > 0.75:
            recommendations.append({
                'priority': 7,
                'category': '🚀 Income Enhancement',
                'recommendation': self.recommendation_database['income_growth']['strategies'][0],
                'action': "Negotiate 10-15% raise or explore job market for 20% income increase",
                'impact': '🟢 HIGH - More impactful than cutting expenses',
                'timeline': '6-12 months',
                'difficulty': 'Medium'
            })
        
        # Priority 8: Retirement Planning
        age_group = '20s-30s' if age < 40 else '40s-50s' if age < 55 else '50s-60s'
        retirement_recs = self.recommendation_database['retirement_planning']['age_based'][age_group]
        
        recommendations.append({
            'priority': 8,
            'category': '🏖️ Retirement Planning',
            'recommendation': retirement_recs[0],
            'action': retirement_recs[4] if len(retirement_recs) > 4 else retirement_recs[1],
            'impact': '🟢 CRITICAL (Long-term) - Secure future',
            'timeline': 'Long-term',
            'difficulty': 'Medium'
        })
        
        # Sort by priority
        recommendations.sort(key=lambda x: x['priority'])
        
        return recommendations
    
    def generate_ai_insights(self, user_features):
        """Generate AI-powered insights based on pattern analysis"""
        insights = []
        
        savings_ratio = user_features.get('savings_ratio', 0)
        dti = user_features.get('debt_to_income_ratio', 0)
        health_score = user_features.get('financial_health_score', 0)
        emergency_months = user_features.get('emergency_fund_months', 0)
        income = user_features.get('total_income', 0)
        investment_ratio = user_features.get('investment_ratio', 0)
        age = user_features.get('age', 30)
        
        # Pattern 1: High earner, low saver
        if income > 7000 and savings_ratio < 0.15:
            insights.append({
                'type': 'warning',
                'title': '⚠️ Lifestyle Inflation Detected',
                'message': f'High income (${income:,.0f}) but low savings rate ({savings_ratio*100:.1f}%). Track expenses for 30 days to identify spending leaks.'
            })
        
        # Pattern 2: Good savings but no investments
        if savings_ratio > 0.20 and investment_ratio < 0.05:
            insights.append({
                'type': 'opportunity',
                'title': '📈 Investment Opportunity Identified',
                'message': f'Excellent {savings_ratio*100:.1f}% savings rate! Time to put money to work - start with index funds for compound growth.'
            })
        
        # Pattern 3: Emergency fund ready for growth
        if emergency_months >= 6 and dti < 0.30:
            insights.append({
                'type': 'success',
                'title': '🚀 Ready for Aggressive Wealth Building',
                'message': f'Strong foundation with {emergency_months:.1f} months emergency fund and low debt. Focus on wealth multiplication strategies.'
            })
        
        # Pattern 4: Debt-savings spiral
        if dti > 0.40 and savings_ratio < 0.10:
            insights.append({
                'type': 'critical',
                'title': '🚨 Critical: Debt-Savings Imbalance',
                'message': f'DTI {dti*100:.1f}% + {savings_ratio*100:.1f}% savings creates vulnerability. Immediate action required on debt reduction.'
            })
        
        # Pattern 5: Retirement readiness
        expected_multiple = {30: 1, 40: 3, 50: 6, 60: 8}.get((age // 10) * 10, 1)
        expected_retirement_savings = income * 12 * expected_multiple
        actual_net_worth = user_features.get('emergency_fund', 0) + user_features.get('investments', 0)
        
        if actual_net_worth < expected_retirement_savings * 0.5:
            insights.append({
                'type': 'warning',
                'title': '⏰ Retirement Savings Behind Schedule',
                'message': f'At age {age}, target net worth is ${expected_retirement_savings:,.0f}. Current: ${actual_net_worth:,.0f}. Need to accelerate by ${(expected_retirement_savings - actual_net_worth)/12:.0f}/month.'
            })
        elif actual_net_worth >= expected_retirement_savings:
            insights.append({
                'type': 'success',
                'title': '🎯 Retirement On Track or Ahead',
                'message': f'Excellent! Your net worth (${actual_net_worth:,.0f}) meets or exceeds age {age} target (${expected_retirement_savings:,.0f}).'
            })
        
        # Pattern 6: Young high saver
        if age < 35 and savings_ratio > 0.30:
            years_to_retirement = 65 - age
            potential_wealth = (income * savings_ratio * 12) * ((1.07 ** years_to_retirement - 1) / 0.07)
            insights.append({
                'type': 'success',
                'title': '⚡ Compound Interest Superpower Activated',
                'message': f'At {age} with {savings_ratio*100:.0f}% savings rate, you could accumulate ${potential_wealth/1000000:.1f}M by retirement (7% annual return)!'
            })
        
        # Pattern 7: High expense ratio
        expense_ratio = user_features.get('expense_ratio', 0)
        if expense_ratio > 0.85:
            potential_monthly_savings = income * (expense_ratio - 0.70)
            insights.append({
                'type': 'warning',
                'title': '💸 Expense Ratio Critical',
                'message': f'{expense_ratio*100:.0f}% expense ratio leaves no buffer. Reducing to 70% would free up ${potential_monthly_savings:,.0f}/month.'
            })
        
        return insights
    
    def get_country_specific_recommendations(self, country):
        """Get country-specific financial recommendations"""
        if country in self.recommendation_database['country_specific']:
            return self.recommendation_database['country_specific'][country]
        return []


if __name__ == "__main__":
    print("✅ Enhanced AI Recommender loaded")