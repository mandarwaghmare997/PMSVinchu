"""
PMS Intelligence Hub - Advanced Analytics Dashboard
Comprehensive graphical overviews with multiple view options
Author: Vulnuris Development Team
"""

from typing import Dict, List, Optional, Tuple
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta, date
import sqlite3
import json
import io
import base64
from flows_tracker import ClientFlowsTracker

# Page configuration
st.set_page_config(
    page_title="PMS Intelligence Hub - Advanced Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class AdvancedAnalyticsDashboard:
    """Advanced Analytics Dashboard with comprehensive graphical overviews"""
    
    def __init__(self):
        self.db_path = "pms_client_data.db"
        self.flows_tracker = ClientFlowsTracker(self.db_path)
        self.init_database()
        self.chart_themes = {
            'default': 'plotly_white',
            'dark': 'plotly_dark',
            'minimal': 'simple_white',
            'presentation': 'presentation'
        }
        
    def init_database(self):
        """Initialize comprehensive database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enhanced clients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT UNIQUE NOT NULL,
                client_name TEXT NOT NULL,
                nav_bucket REAL,
                inception_date DATE,
                age_of_client INTEGER,
                client_since REAL,
                mobile TEXT,
                email TEXT,
                distributor_name TEXT,
                current_aum REAL,
                initial_corpus REAL,
                additions REAL,
                withdrawals REAL,
                net_corpus REAL,
                annualised_returns REAL,
                bse_500_benchmark_returns REAL,
                rm_name TEXT,
                portfolio_type TEXT,
                risk_profile TEXT,
                city TEXT,
                state TEXT,
                occupation TEXT,
                annual_income REAL,
                investment_objective TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Enhanced client notes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT NOT NULL,
                note_date DATE NOT NULL,
                note_text TEXT NOT NULL,
                note_type TEXT DEFAULT 'General',
                priority TEXT DEFAULT 'Medium',
                created_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (client_id)
            )
        ''')
        
        # Performance tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT NOT NULL,
                date DATE NOT NULL,
                aum_value REAL,
                returns_value REAL,
                benchmark_value REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (client_id)
            )
        ''')
        
        # Create comprehensive indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_rm ON clients(rm_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_portfolio ON clients(portfolio_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_aum ON clients(current_aum)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_risk ON clients(risk_profile)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_city ON clients(city)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_notes_client ON client_notes(client_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_notes_date ON client_notes(note_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_client ON performance_history(client_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_date ON performance_history(date)')
        
        conn.commit()
        conn.close()
    
    def render_advanced_css(self):
        """Apply comprehensive CSS styling"""
        st.markdown("""
        <style>
        .main-header {
            font-size: 3.5rem;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #1e3a8a, #3b82f6, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
            animation: gradient 4s ease-in-out infinite;
            background-size: 400% 400%;
        }
        
        @keyframes gradient {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.1);
            min-height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            overflow: hidden;
        }
        
        .metric-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 60px rgba(0,0,0,0.25);
        }
        
        .metric-value {
            font-size: 2.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            word-wrap: break-word;
            line-height: 1.1;
        }
        
        .metric-label {
            font-size: 1rem;
            opacity: 0.9;
            font-weight: 500;
            word-wrap: break-word;
        }
        
        .chart-container {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        
        .chart-container:hover {
            box-shadow: 0 12px 40px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        
        .advanced-metric {
            background: linear-gradient(135deg, #ff6b6b, #feca57);
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 1rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }
        
        .performance-indicator {
            background: linear-gradient(135deg, #48cae4, #023e8a);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
            font-weight: 600;
        }
        
        .view-selector {
            background: #f8fafc;
            padding: 1rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            border: 2px solid #e2e8f0;
        }
        
        .filter-section {
            background: linear-gradient(135deg, #f8fafc, #e2e8f0);
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            border: 1px solid #cbd5e1;
        }
        
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        }
        
        .stSelectbox > div > div {
            background-color: #f8fafc;
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        
        .stSelectbox > div > div:hover {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            color: white;
            border-radius: 12px;
            border: none;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #1e40af, #2563eb);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
        }
        
        .dataframe {
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: linear-gradient(135deg, #f8fafc, #e2e8f0);
            padding: 1rem;
            border-radius: 15px;
            border: 1px solid #cbd5e1;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: white;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            border: 2px solid #e2e8f0;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            border-color: #3b82f6;
            transform: translateY(-1px);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            color: white;
            border-color: #3b82f6;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        .top-performer {
            background: linear-gradient(135deg, #10b981, #059669);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 0.5rem;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        }
        
        .risk-indicator {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            text-align: center;
            margin: 0.25rem;
            transition: all 0.3s ease;
        }
        
        .risk-indicator:hover {
            transform: scale(1.05);
        }
        
        .risk-conservative { background: #10b981; color: white; }
        .risk-moderate { background: #f59e0b; color: white; }
        .risk-aggressive { background: #ef4444; color: white; }
        .risk-very-aggressive { background: #dc2626; color: white; }
        
        .note-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #3b82f6;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .note-priority-high { border-left-color: #ef4444; }
        .note-priority-medium { border-left-color: #f59e0b; }
        .note-priority-low { border-left-color: #10b981; }
        
        .chart-controls {
            background: #f1f5f9;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border: 1px solid #cbd5e1;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @st.cache_data
    def load_enhanced_sample_data(_self) -> pd.DataFrame:
        """Load enhanced sample data with comprehensive client information"""
        np.random.seed(42)
        
        # Enhanced Indian data
        indian_names = [
            "Rajesh Sharma", "Priya Patel", "Amit Kumar", "Sunita Singh", "Vikram Gupta",
            "Anita Joshi", "Suresh Reddy", "Kavita Nair", "Arjun Mehta", "Deepika Iyer",
            "Rohit Agarwal", "Meera Jain", "Sanjay Verma", "Pooja Bansal", "Kiran Rao",
            "Neha Chopra", "Ravi Tiwari", "Shweta Malhotra", "Ajay Saxena", "Ritu Bhatt",
            "Manish Agrawal", "Sneha Kulkarni", "Rahul Desai", "Divya Menon", "Ashok Pandey",
            "Rekha Sinha", "Nitin Jha", "Swati Mishra", "Gaurav Bhardwaj", "Nisha Yadav",
            "Arun Krishnan", "Lakshmi Pillai", "Harish Chand", "Geeta Agarwal", "Mohan Lal"
        ]
        
        cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad", "Surat", "Jaipur"]
        states = ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "West Bengal", "Telangana", "Gujarat", "Rajasthan"]
        rm_names = ["Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sunita Gupta", "Vikram Singh", "Neha Agarwal", "Rohit Jain"]
        portfolio_types = ["Equity", "Debt", "Hybrid", "Multi-Asset", "ELSS", "Sectoral", "International"]
        risk_profiles = ["Conservative", "Moderate", "Aggressive", "Very Aggressive"]
        distributors = ["HDFC Securities", "ICICI Direct", "Zerodha", "Angel Broking", "Kotak Securities", "Motilal Oswal", "Sharekhan"]
        occupations = ["Business", "Service", "Professional", "Retired", "Government", "Self-Employed"]
        investment_objectives = ["Growth", "Income", "Balanced", "Capital Protection", "Tax Saving", "Retirement Planning"]
        
        data = []
        for i in range(250):  # Increased to 250 clients for better analysis
            client_id = f"CL{i+1:04d}"
            
            # Enhanced AUM distribution
            if i < 25:  # Ultra high net worth
                current_aum = np.random.uniform(200, 1000)
            elif i < 75:  # High net worth
                current_aum = np.random.uniform(50, 200)
            elif i < 150:  # Affluent
                current_aum = np.random.uniform(10, 50)
            elif i < 200:  # Mid-tier
                current_aum = np.random.uniform(2, 10)
            else:  # Regular
                current_aum = np.random.uniform(0.5, 2)
            
            # Calculate financial metrics
            initial_corpus = current_aum * np.random.uniform(0.4, 0.8)
            additions = current_aum * np.random.uniform(0.1, 0.6)
            withdrawals = current_aum * np.random.uniform(0.02, 0.2)
            net_corpus = initial_corpus + additions - withdrawals
            
            # Enhanced returns based on multiple factors
            portfolio_type = np.random.choice(portfolio_types)
            risk_profile = np.random.choice(risk_profiles)
            
            # Base returns by portfolio type
            base_returns = {
                "Equity": np.random.uniform(8, 30),
                "Debt": np.random.uniform(4, 12),
                "Hybrid": np.random.uniform(6, 22),
                "Multi-Asset": np.random.uniform(7, 25),
                "ELSS": np.random.uniform(10, 32),
                "Sectoral": np.random.uniform(5, 40),
                "International": np.random.uniform(6, 28)
            }[portfolio_type]
            
            # Risk adjustment
            risk_multiplier = {
                "Conservative": np.random.uniform(0.7, 1.0),
                "Moderate": np.random.uniform(0.9, 1.2),
                "Aggressive": np.random.uniform(1.1, 1.5),
                "Very Aggressive": np.random.uniform(1.3, 1.8)
            }[risk_profile]
            
            annualised_returns = base_returns * risk_multiplier
            
            # Add market volatility
            if np.random.random() < 0.15:  # 15% exceptional performers
                annualised_returns *= np.random.uniform(1.3, 2.0)
            elif np.random.random() < 0.15:  # 15% poor performers
                annualised_returns *= np.random.uniform(0.2, 0.6)
            
            # Benchmark and demographics
            bse_500_benchmark = np.random.uniform(8, 18)
            age = np.random.randint(25, 80)
            client_since = np.random.uniform(0.25, 20)
            inception_date = (datetime.now() - timedelta(days=int(client_since * 365))).strftime('%Y-%m-%d')
            
            # Income based on AUM
            if current_aum > 100:
                annual_income = np.random.uniform(50, 500)  # Lakhs
            elif current_aum > 25:
                annual_income = np.random.uniform(20, 100)
            elif current_aum > 5:
                annual_income = np.random.uniform(8, 50)
            else:
                annual_income = np.random.uniform(3, 20)
            
            data.append({
                'client_id': client_id,
                'client_name': np.random.choice(indian_names) + f" {i+1}",
                'nav_bucket': current_aum,
                'inception_date': inception_date,
                'age_of_client': age,
                'client_since': round(client_since, 1),
                'mobile': f"9{np.random.randint(100000000, 999999999)}",
                'email': f"client{i+1}@example.com",
                'distributor_name': np.random.choice(distributors),
                'current_aum': round(current_aum, 2),
                'initial_corpus': round(initial_corpus, 2),
                'additions': round(additions, 2),
                'withdrawals': round(withdrawals, 2),
                'net_corpus': round(net_corpus, 2),
                'annualised_returns': round(annualised_returns, 2),
                'bse_500_benchmark_returns': round(bse_500_benchmark, 2),
                'rm_name': np.random.choice(rm_names),
                'portfolio_type': portfolio_type,
                'risk_profile': risk_profile,
                'city': np.random.choice(cities),
                'state': np.random.choice(states),
                'occupation': np.random.choice(occupations),
                'annual_income': round(annual_income, 2),
                'investment_objective': np.random.choice(investment_objectives)
            })
        
        return pd.DataFrame(data)
    
    @st.cache_data
    def load_data(_self) -> pd.DataFrame:
        """Load data from database or create enhanced sample data"""
        conn = sqlite3.connect(_self.db_path)
        
        try:
            data = pd.read_sql_query("SELECT * FROM clients", conn)
            if len(data) == 0:
                raise ValueError("No data in database")
        except:
            sample_data = _self.load_enhanced_sample_data()
            sample_data.to_sql('clients', conn, if_exists='replace', index=False)
            data = sample_data
        
        conn.close()
        return data
    
    def generate_sample_notes(self, client_ids: List[str]) -> pd.DataFrame:
        """Generate sample client notes"""
        note_types = ["Meeting", "Call", "Email", "Review", "Alert", "Follow-up"]
        priorities = ["High", "Medium", "Low"]
        
        notes_data = []
        for client_id in client_ids[:50]:  # Generate notes for first 50 clients
            num_notes = np.random.randint(1, 6)
            for _ in range(num_notes):
                note_date = datetime.now() - timedelta(days=np.random.randint(1, 365))
                note_type = np.random.choice(note_types)
                priority = np.random.choice(priorities)
                
                note_texts = {
                    "Meeting": f"Client meeting scheduled for portfolio review. Discussed investment strategy and risk tolerance.",
                    "Call": f"Follow-up call regarding recent market volatility. Client expressed satisfaction with performance.",
                    "Email": f"Sent quarterly performance report. Client requested additional information on tax implications.",
                    "Review": f"Annual portfolio review completed. Recommended rebalancing based on changed risk profile.",
                    "Alert": f"Market alert: Significant movement in client's portfolio. Monitoring closely.",
                    "Follow-up": f"Following up on previous recommendations. Client agreed to increase SIP amount."
                }
                
                notes_data.append({
                    'client_id': client_id,
                    'note_date': note_date.strftime('%Y-%m-%d'),
                    'note_text': note_texts[note_type],
                    'note_type': note_type,
                    'priority': priority,
                    'created_by': f"RM_{np.random.randint(1, 5)}"
                })
        
        return pd.DataFrame(notes_data)
    
    def calculate_comprehensive_metrics(self, data: pd.DataFrame) -> Dict:
        """Calculate comprehensive portfolio metrics"""
        total_aum = data['current_aum'].sum()
        total_clients = len(data)
        avg_returns = data['annualised_returns'].mean()
        avg_benchmark = data['bse_500_benchmark_returns'].mean()
        
        # Advanced risk metrics
        alpha = avg_returns - avg_benchmark
        returns_std = data['annualised_returns'].std()
        sharpe_ratio = (avg_returns - 6) / returns_std if returns_std > 0 else 0
        
        # Beta calculation
        correlation = np.corrcoef(data['annualised_returns'], data['bse_500_benchmark_returns'])[0, 1]
        beta = correlation * (returns_std / data['bse_500_benchmark_returns'].std()) if data['bse_500_benchmark_returns'].std() > 0 else 1
        
        # Information ratio
        tracking_error = (data['annualised_returns'] - data['bse_500_benchmark_returns']).std()
        information_ratio = alpha / tracking_error if tracking_error > 0 else 0
        
        # Sortino ratio (downside deviation)
        downside_returns = data['annualised_returns'][data['annualised_returns'] < avg_returns]
        downside_deviation = downside_returns.std() if len(downside_returns) > 0 else returns_std
        sortino_ratio = (avg_returns - 6) / downside_deviation if downside_deviation > 0 else 0
        
        # Portfolio distributions
        portfolio_composition = data['portfolio_type'].value_counts().to_dict()
        risk_distribution = data['risk_profile'].value_counts().to_dict()
        rm_distribution = data['rm_name'].value_counts().to_dict()
        city_distribution = data['city'].value_counts().to_dict()
        occupation_distribution = data['occupation'].value_counts().to_dict()
        
        # Performance quartiles
        returns_quartiles = data['annualised_returns'].quantile([0.25, 0.5, 0.75]).to_dict()
        aum_quartiles = data['current_aum'].quantile([0.25, 0.5, 0.75]).to_dict()
        
        # Top performers
        top_performers = data.nlargest(15, 'annualised_returns')[['client_name', 'annualised_returns', 'current_aum', 'portfolio_type', 'rm_name']]
        bottom_performers = data.nsmallest(10, 'annualised_returns')[['client_name', 'annualised_returns', 'current_aum', 'portfolio_type', 'rm_name']]
        
        # AUM analysis
        aum_ranges = {
            '₹0.5-2 Cr': len(data[(data['current_aum'] >= 0.5) & (data['current_aum'] < 2)]),
            '₹2-5 Cr': len(data[(data['current_aum'] >= 2) & (data['current_aum'] < 5)]),
            '₹5-10 Cr': len(data[(data['current_aum'] >= 5) & (data['current_aum'] < 10)]),
            '₹10-25 Cr': len(data[(data['current_aum'] >= 10) & (data['current_aum'] < 25)]),
            '₹25-50 Cr': len(data[(data['current_aum'] >= 25) & (data['current_aum'] < 50)]),
            '₹50-100 Cr': len(data[(data['current_aum'] >= 50) & (data['current_aum'] < 100)]),
            '₹100-200 Cr': len(data[(data['current_aum'] >= 100) & (data['current_aum'] < 200)]),
            '₹200+ Cr': len(data[data['current_aum'] >= 200])
        }
        
        # Age demographics
        age_ranges = {
            '25-35': len(data[(data['age_of_client'] >= 25) & (data['age_of_client'] < 35)]),
            '35-45': len(data[(data['age_of_client'] >= 35) & (data['age_of_client'] < 45)]),
            '45-55': len(data[(data['age_of_client'] >= 45) & (data['age_of_client'] < 55)]),
            '55-65': len(data[(data['age_of_client'] >= 55) & (data['age_of_client'] < 65)]),
            '65+': len(data[data['age_of_client'] >= 65])
        }
        
        # Tenure analysis
        tenure_ranges = {
            '< 1 Year': len(data[data['client_since'] < 1]),
            '1-3 Years': len(data[(data['client_since'] >= 1) & (data['client_since'] < 3)]),
            '3-5 Years': len(data[(data['client_since'] >= 3) & (data['client_since'] < 5)]),
            '5-10 Years': len(data[(data['client_since'] >= 5) & (data['client_since'] < 10)]),
            '10-15 Years': len(data[(data['client_since'] >= 10) & (data['client_since'] < 15)]),
            '15+ Years': len(data[data['client_since'] >= 15])
        }
        
        # Income analysis
        income_ranges = {
            '₹3-10 L': len(data[(data['annual_income'] >= 3) & (data['annual_income'] < 10)]),
            '₹10-25 L': len(data[(data['annual_income'] >= 10) & (data['annual_income'] < 25)]),
            '₹25-50 L': len(data[(data['annual_income'] >= 25) & (data['annual_income'] < 50)]),
            '₹50-100 L': len(data[(data['annual_income'] >= 50) & (data['annual_income'] < 100)]),
            '₹100+ L': len(data[data['annual_income'] >= 100])
        }
        
        return {
            'total_aum': total_aum,
            'total_clients': total_clients,
            'avg_returns': avg_returns,
            'avg_benchmark': avg_benchmark,
            'alpha': alpha,
            'beta': beta,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'information_ratio': information_ratio,
            'returns_std': returns_std,
            'tracking_error': tracking_error,
            'correlation': correlation,
            'portfolio_composition': portfolio_composition,
            'risk_distribution': risk_distribution,
            'rm_distribution': rm_distribution,
            'city_distribution': city_distribution,
            'occupation_distribution': occupation_distribution,
            'returns_quartiles': returns_quartiles,
            'aum_quartiles': aum_quartiles,
            'top_performers': top_performers,
            'bottom_performers': bottom_performers,
            'aum_ranges': aum_ranges,
            'age_ranges': age_ranges,
            'tenure_ranges': tenure_ranges,
            'income_ranges': income_ranges
        }
    
    def create_client_overview_charts(self, data: pd.DataFrame, metrics: Dict, view_type: str, theme: str):
        """Create comprehensive client overview charts with multiple perspectives"""
        
        charts = {}
        
        if view_type == "Performance Analysis":
            # 1. Multi-dimensional Performance Scatter
            fig_performance = go.Figure()
            
            # Create color mapping for portfolio types
            portfolio_colors = px.colors.qualitative.Set3
            portfolio_types = data['portfolio_type'].unique()
            color_map = {pt: portfolio_colors[i % len(portfolio_colors)] for i, pt in enumerate(portfolio_types)}
            
            for portfolio_type in portfolio_types:
                subset = data[data['portfolio_type'] == portfolio_type]
                fig_performance.add_trace(go.Scatter(
                    x=subset['current_aum'],
                    y=subset['annualised_returns'],
                    mode='markers',
                    marker=dict(
                        size=np.sqrt(subset['client_since']) * 4,
                        color=color_map[portfolio_type],
                        opacity=0.7,
                        line=dict(width=1, color='white')
                    ),
                    text=[f"<b>{name}</b><br>AUM: ₹{aum:.2f} Cr<br>Returns: {ret:.2f}%<br>Tenure: {tenure:.1f} years<br>Age: {age}<br>RM: {rm}" 
                          for name, aum, ret, tenure, age, rm in zip(subset['client_name'], subset['current_aum'], 
                                                                    subset['annualised_returns'], subset['client_since'], 
                                                                    subset['age_of_client'], subset['rm_name'])],
                    hovertemplate='%{text}<extra></extra>',
                    name=portfolio_type
                ))
            
            # Add benchmark and average lines
            fig_performance.add_hline(
                y=metrics['avg_benchmark'],
                line_dash="dash",
                line_color="red",
                annotation_text=f"BSE 500 Benchmark: {metrics['avg_benchmark']:.2f}%"
            )
            
            fig_performance.add_hline(
                y=metrics['avg_returns'],
                line_dash="dot",
                line_color="blue",
                annotation_text=f"Portfolio Average: {metrics['avg_returns']:.2f}%"
            )
            
            fig_performance.update_layout(
                title="Portfolio Performance Analysis (Bubble size = Client Tenure)",
                xaxis_title="Assets Under Management (₹ Crores)",
                yaxis_title="Annualised Returns (%)",
                height=600,
                template=self.chart_themes[theme],
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            charts['performance'] = fig_performance
            
            # 2. Risk-Return Efficiency Frontier
            portfolio_stats = data.groupby('portfolio_type').agg({
                'annualised_returns': ['mean', 'std'],
                'current_aum': 'sum',
                'client_id': 'count'
            }).round(2)
            
            portfolio_stats.columns = ['avg_return', 'risk', 'total_aum', 'client_count']
            
            fig_risk_return = go.Figure()
            
            fig_risk_return.add_trace(go.Scatter(
                x=portfolio_stats['risk'],
                y=portfolio_stats['avg_return'],
                mode='markers+text',
                marker=dict(
                    size=portfolio_stats['client_count'] * 3,
                    color=portfolio_stats['avg_return'],
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="Avg Returns %"),
                    line=dict(width=2, color='white')
                ),
                text=portfolio_stats.index,
                textposition="middle center",
                textfont=dict(size=10, color='white'),
                hovertemplate='<b>%{text}</b><br>Risk: %{x:.2f}%<br>Return: %{y:.2f}%<br>Clients: ' + 
                             portfolio_stats['client_count'].astype(str) + '<br>Total AUM: ₹' + 
                             portfolio_stats['total_aum'].round(1).astype(str) + ' Cr<extra></extra>',
                name='Portfolio Types'
            ))
            
            # Add quadrant lines
            avg_risk = portfolio_stats['risk'].mean()
            avg_return = portfolio_stats['avg_return'].mean()
            
            fig_risk_return.add_vline(x=avg_risk, line_dash="dash", line_color="gray", opacity=0.5)
            fig_risk_return.add_hline(y=avg_return, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Add quadrant labels
            fig_risk_return.add_annotation(x=avg_risk*0.5, y=avg_return*1.2, text="Low Risk<br>High Return", 
                                         showarrow=False, font=dict(size=10, color="green"))
            fig_risk_return.add_annotation(x=avg_risk*1.5, y=avg_return*1.2, text="High Risk<br>High Return", 
                                         showarrow=False, font=dict(size=10, color="orange"))
            fig_risk_return.add_annotation(x=avg_risk*0.5, y=avg_return*0.8, text="Low Risk<br>Low Return", 
                                         showarrow=False, font=dict(size=10, color="blue"))
            fig_risk_return.add_annotation(x=avg_risk*1.5, y=avg_return*0.8, text="High Risk<br>Low Return", 
                                         showarrow=False, font=dict(size=10, color="red"))
            
            fig_risk_return.update_layout(
                title="Risk-Return Efficiency Analysis (Bubble size = Client Count)",
                xaxis_title="Risk (Standard Deviation %)",
                yaxis_title="Average Returns (%)",
                height=500,
                template=self.chart_themes[theme]
            )
            
            charts['risk_return'] = fig_risk_return
            
        elif view_type == "Portfolio Composition":
            # 1. Hierarchical Sunburst Chart
            portfolio_risk_data = data.groupby(['portfolio_type', 'risk_profile']).agg({
                'current_aum': 'sum',
                'client_id': 'count'
            }).reset_index()
            portfolio_risk_data.columns = ['portfolio_type', 'risk_profile', 'total_aum', 'client_count']
            
            fig_sunburst = px.sunburst(
                portfolio_risk_data,
                path=['portfolio_type', 'risk_profile'],
                values='total_aum',
                title="Portfolio Composition by Type and Risk Profile (AUM Weighted)",
                color='total_aum',
                color_continuous_scale='Blues',
                height=500
            )
            fig_sunburst.update_layout(template=self.chart_themes[theme])
            
            charts['sunburst'] = fig_sunburst
            
            # 2. Treemap Visualization
            fig_treemap = px.treemap(
                portfolio_risk_data,
                path=[px.Constant("Portfolio"), 'portfolio_type', 'risk_profile'],
                values='total_aum',
                color='client_count',
                color_continuous_scale='Viridis',
                title="Portfolio Treemap (Size = AUM, Color = Client Count)",
                height=500
            )
            fig_treemap.update_layout(template=self.chart_themes[theme])
            
            charts['treemap'] = fig_treemap
            
        elif view_type == "Geographic Analysis":
            # 1. City-wise Distribution
            city_stats = data.groupby('city').agg({
                'current_aum': 'sum',
                'annualised_returns': 'mean',
                'client_id': 'count'
            }).round(2)
            city_stats.columns = ['total_aum', 'avg_returns', 'client_count']
            city_stats = city_stats.sort_values('total_aum', ascending=False)
            
            fig_city = go.Figure()
            
            fig_city.add_trace(go.Bar(
                x=city_stats.index,
                y=city_stats['total_aum'],
                name='Total AUM (₹ Cr)',
                marker_color='lightblue',
                yaxis='y',
                hovertemplate='<b>%{x}</b><br>Total AUM: ₹%{y:.1f} Cr<br>Clients: ' + 
                             city_stats['client_count'].astype(str) + '<extra></extra>'
            ))
            
            fig_city.add_trace(go.Scatter(
                x=city_stats.index,
                y=city_stats['avg_returns'],
                mode='lines+markers',
                name='Avg Returns (%)',
                marker_color='red',
                yaxis='y2',
                hovertemplate='<b>%{x}</b><br>Avg Returns: %{y:.2f}%<extra></extra>'
            ))
            
            fig_city.update_layout(
                title="City-wise AUM and Performance Analysis",
                xaxis_title="City",
                yaxis=dict(title="Total AUM (₹ Crores)", side="left"),
                yaxis2=dict(title="Average Returns (%)", side="right", overlaying="y"),
                height=500,
                template=self.chart_themes[theme],
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            charts['city_analysis'] = fig_city
            
            # 2. Occupation-wise Analysis
            occupation_stats = data.groupby('occupation').agg({
                'current_aum': ['sum', 'mean'],
                'annualised_returns': 'mean',
                'annual_income': 'mean',
                'client_id': 'count'
            }).round(2)
            
            occupation_stats.columns = ['total_aum', 'avg_aum', 'avg_returns', 'avg_income', 'client_count']
            
            fig_occupation = px.scatter(
                occupation_stats.reset_index(),
                x='avg_income',
                y='avg_returns',
                size='client_count',
                color='total_aum',
                hover_name='occupation',
                title="Occupation Analysis (Income vs Returns)",
                labels={'avg_income': 'Average Income (₹ Lakhs)', 'avg_returns': 'Average Returns (%)'},
                color_continuous_scale='Plasma',
                height=500
            )
            fig_occupation.update_layout(template=self.chart_themes[theme])
            
            charts['occupation_analysis'] = fig_occupation
            
        elif view_type == "Demographic Analysis":
            # 1. Age vs Performance Analysis
            fig_age_performance = px.scatter(
                data,
                x='age_of_client',
                y='annualised_returns',
                color='risk_profile',
                size='current_aum',
                hover_data=['client_name', 'portfolio_type', 'rm_name'],
                title="Age vs Performance Analysis (Bubble size = AUM)",
                labels={'age_of_client': 'Client Age', 'annualised_returns': 'Annualised Returns (%)'},
                height=500
            )
            fig_age_performance.update_layout(template=self.chart_themes[theme])
            
            charts['age_performance'] = fig_age_performance
            
            # 2. Tenure vs Loyalty Analysis
            fig_tenure = px.histogram(
                data,
                x='client_since',
                color='portfolio_type',
                title="Client Tenure Distribution by Portfolio Type",
                labels={'client_since': 'Client Tenure (Years)', 'count': 'Number of Clients'},
                nbins=20,
                height=400
            )
            fig_tenure.update_layout(template=self.chart_themes[theme])
            
            charts['tenure_analysis'] = fig_tenure
            
        elif view_type == "RM Performance":
            # 1. RM Performance Heatmap
            rm_performance = data.groupby(['rm_name', 'portfolio_type']).agg({
                'annualised_returns': 'mean',
                'current_aum': 'sum',
                'client_id': 'count'
            }).round(2)
            
            # Pivot for heatmap
            rm_returns_pivot = rm_performance['annualised_returns'].unstack(fill_value=0)
            rm_aum_pivot = rm_performance['current_aum'].unstack(fill_value=0)
            
            fig_rm_heatmap = px.imshow(
                rm_returns_pivot.values,
                x=rm_returns_pivot.columns,
                y=rm_returns_pivot.index,
                color_continuous_scale='RdYlGn',
                title="RM Performance Heatmap (Average Returns by Portfolio Type)",
                labels=dict(x="Portfolio Type", y="Relationship Manager", color="Avg Returns %"),
                height=400
            )
            fig_rm_heatmap.update_layout(template=self.chart_themes[theme])
            
            charts['rm_heatmap'] = fig_rm_heatmap
            
            # 2. RM Efficiency Analysis
            rm_stats = data.groupby('rm_name').agg({
                'current_aum': ['sum', 'mean'],
                'annualised_returns': 'mean',
                'client_id': 'count'
            }).round(2)
            
            rm_stats.columns = ['total_aum', 'avg_aum_per_client', 'avg_returns', 'client_count']
            
            fig_rm_efficiency = go.Figure()
            
            fig_rm_efficiency.add_trace(go.Scatter(
                x=rm_stats['client_count'],
                y=rm_stats['avg_returns'],
                mode='markers+text',
                marker=dict(
                    size=rm_stats['total_aum'] / 10,  # Scale down for visibility
                    color=rm_stats['avg_aum_per_client'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Avg AUM per Client"),
                    line=dict(width=2, color='white')
                ),
                text=rm_stats.index,
                textposition="top center",
                hovertemplate='<b>%{text}</b><br>Clients: %{x}<br>Avg Returns: %{y:.2f}%<br>Total AUM: ₹' + 
                             rm_stats['total_aum'].round(1).astype(str) + ' Cr<extra></extra>',
                name='RM Performance'
            ))
            
            fig_rm_efficiency.update_layout(
                title="RM Efficiency Analysis (Bubble size = Total AUM)",
                xaxis_title="Number of Clients",
                yaxis_title="Average Returns (%)",
                height=500,
                template=self.chart_themes[theme]
            )
            
            charts['rm_efficiency'] = fig_rm_efficiency
        
        return charts
    
    def create_client_flows_charts(self, flows_data: pd.DataFrame, view_type: str, theme: str):
        """Create comprehensive client flows charts"""
        
        charts = {}
        
        if view_type == "Transaction Trends":
            # 1. Monthly Flow Trends
            flows_data['transaction_date'] = pd.to_datetime(flows_data['transaction_date'])
            flows_data['month_year'] = flows_data['transaction_date'].dt.to_period('M')
            
            monthly_flows = flows_data.groupby(['month_year', 'transaction_label']).agg({
                'amount': 'sum'
            }).reset_index()
            monthly_flows['month_year_str'] = monthly_flows['month_year'].astype(str)
            
            fig_monthly_trends = px.line(
                monthly_flows,
                x='month_year_str',
                y='amount',
                color='transaction_label',
                title="Monthly Transaction Trends by Type",
                labels={'month_year_str': 'Month', 'amount': 'Amount (₹ Crores)'},
                height=500
            )
            fig_monthly_trends.update_layout(template=self.chart_themes[theme])
            
            charts['monthly_trends'] = fig_monthly_trends
            
            # 2. Transaction Volume Analysis
            transaction_summary = flows_data.groupby('transaction_label').agg({
                'amount': ['sum', 'mean', 'count'],
                'client_id': 'nunique'
            }).round(2)
            
            transaction_summary.columns = ['total_amount', 'avg_amount', 'transaction_count', 'unique_clients']
            
            fig_volume = go.Figure()
            
            fig_volume.add_trace(go.Bar(
                x=transaction_summary.index,
                y=transaction_summary['total_amount'],
                name='Total Amount',
                marker_color='lightblue',
                yaxis='y'
            ))
            
            fig_volume.add_trace(go.Scatter(
                x=transaction_summary.index,
                y=transaction_summary['transaction_count'],
                mode='lines+markers',
                name='Transaction Count',
                marker_color='red',
                yaxis='y2'
            ))
            
            fig_volume.update_layout(
                title="Transaction Volume Analysis",
                xaxis_title="Transaction Type",
                yaxis=dict(title="Total Amount (₹ Crores)", side="left"),
                yaxis2=dict(title="Transaction Count", side="right", overlaying="y"),
                height=500,
                template=self.chart_themes[theme]
            )
            
            charts['volume_analysis'] = fig_volume
            
        elif view_type == "Client Flow Patterns":
            # 1. Client-wise Flow Analysis
            client_flows = flows_data.groupby(['client_id', 'transaction_label']).agg({
                'amount': 'sum'
            }).reset_index()
            
            # Pivot to get inflows vs outflows
            client_pivot = client_flows.pivot(index='client_id', columns='transaction_label', values='amount').fillna(0)
            
            # Calculate net flows
            inflow_cols = [col for col in client_pivot.columns if any(term in col.lower() for term in ['investment', 'deposit', 'addition'])]
            outflow_cols = [col for col in client_pivot.columns if any(term in col.lower() for term in ['withdrawal', 'redemption', 'fees'])]
            
            if inflow_cols:
                client_pivot['total_inflows'] = client_pivot[inflow_cols].sum(axis=1)
            else:
                client_pivot['total_inflows'] = 0
                
            if outflow_cols:
                client_pivot['total_outflows'] = client_pivot[outflow_cols].sum(axis=1)
            else:
                client_pivot['total_outflows'] = 0
            
            client_pivot['net_flows'] = client_pivot['total_inflows'] - client_pivot['total_outflows']
            
            fig_client_flows = px.scatter(
                client_pivot.reset_index(),
                x='total_inflows',
                y='total_outflows',
                color='net_flows',
                hover_data=['client_id'],
                title="Client Flow Patterns (Inflows vs Outflows)",
                labels={'total_inflows': 'Total Inflows (₹ Crores)', 'total_outflows': 'Total Outflows (₹ Crores)'},
                color_continuous_scale='RdYlGn',
                height=500
            )
            fig_client_flows.update_layout(template=self.chart_themes[theme])
            
            charts['client_patterns'] = fig_client_flows
            
        elif view_type == "Seasonal Analysis":
            # 1. Seasonal Patterns
            flows_data['month'] = flows_data['transaction_date'].dt.month
            flows_data['quarter'] = flows_data['transaction_date'].dt.quarter
            
            seasonal_flows = flows_data.groupby(['quarter', 'transaction_label']).agg({
                'amount': 'sum'
            }).reset_index()
            
            fig_seasonal = px.bar(
                seasonal_flows,
                x='quarter',
                y='amount',
                color='transaction_label',
                title="Quarterly Transaction Patterns",
                labels={'quarter': 'Quarter', 'amount': 'Amount (₹ Crores)'},
                height=500
            )
            fig_seasonal.update_layout(template=self.chart_themes[theme])
            
            charts['seasonal_patterns'] = fig_seasonal
        
        return charts
    
    def create_individual_client_analysis(self, data: pd.DataFrame, selected_clients: List[str], theme: str):
        """Create comprehensive individual client analysis charts"""
        
        if not selected_clients:
            return {}
        
        # Filter data for selected clients
        client_data = data[data['client_id'].isin(selected_clients)]
        
        charts = {}
        
        # 1. Client Performance Comparison
        fig_performance = go.Figure()
        
        colors = px.colors.qualitative.Set3
        
        for i, client_id in enumerate(selected_clients):
            client_info = client_data[client_data['client_id'] == client_id].iloc[0]
            
            fig_performance.add_trace(go.Bar(
                name=f"{client_info['client_name']} ({client_id})",
                x=['Returns', 'Benchmark', 'Alpha'],
                y=[
                    client_info['annualised_returns'],
                    client_info['bse_500_benchmark_returns'],
                    client_info['annualised_returns'] - client_info['bse_500_benchmark_returns']
                ],
                marker_color=colors[i % len(colors)],
                text=[
                    f"{client_info['annualised_returns']:.2f}%",
                    f"{client_info['bse_500_benchmark_returns']:.2f}%",
                    f"{client_info['annualised_returns'] - client_info['bse_500_benchmark_returns']:.2f}%"
                ],
                textposition='auto'
            ))
        
        fig_performance.update_layout(
            title="Client Performance Comparison",
            xaxis_title="Metrics",
            yaxis_title="Returns (%)",
            height=500,
            template=self.chart_themes[theme],
            barmode='group'
        )
        
        charts['performance_comparison'] = fig_performance
        
        # 2. AUM and Portfolio Composition
        fig_aum = go.Figure()
        
        for i, client_id in enumerate(selected_clients):
            client_info = client_data[client_data['client_id'] == client_id].iloc[0]
            
            fig_aum.add_trace(go.Bar(
                name=f"{client_info['client_name']}",
                x=['Current AUM', 'Initial Corpus', 'Additions', 'Withdrawals'],
                y=[
                    client_info['current_aum'],
                    client_info['initial_corpus'],
                    client_info['additions'],
                    abs(client_info['withdrawals'])
                ],
                marker_color=colors[i % len(colors)],
                text=[
                    f"₹{client_info['current_aum']:.2f} Cr",
                    f"₹{client_info['initial_corpus']:.2f} Cr",
                    f"₹{client_info['additions']:.2f} Cr",
                    f"₹{abs(client_info['withdrawals']):.2f} Cr"
                ],
                textposition='auto'
            ))
        
        fig_aum.update_layout(
            title="AUM and Investment Flow Comparison",
            xaxis_title="Investment Components",
            yaxis_title="Amount (₹ Crores)",
            height=500,
            template=self.chart_themes[theme],
            barmode='group'
        )
        
        charts['aum_comparison'] = fig_aum
        
        # 3. Risk-Return Scatter for Selected Clients
        fig_risk_return = go.Figure()
        
        # Add all clients as background
        fig_risk_return.add_trace(go.Scatter(
            x=data['annualised_returns'],
            y=data['current_aum'],
            mode='markers',
            marker=dict(
                size=8,
                color='lightgray',
                opacity=0.3
            ),
            name='All Clients',
            hovertemplate='<b>%{text}</b><br>Returns: %{x:.2f}%<br>AUM: ₹%{y:.2f} Cr<extra></extra>',
            text=data['client_name']
        ))
        
        # Highlight selected clients
        for i, client_id in enumerate(selected_clients):
            client_info = client_data[client_data['client_id'] == client_id].iloc[0]
            
            fig_risk_return.add_trace(go.Scatter(
                x=[client_info['annualised_returns']],
                y=[client_info['current_aum']],
                mode='markers+text',
                marker=dict(
                    size=15,
                    color=colors[i % len(colors)],
                    line=dict(width=2, color='white')
                ),
                text=[client_info['client_name']],
                textposition="top center",
                name=f"{client_info['client_name']}",
                hovertemplate=f'<b>{client_info["client_name"]}</b><br>Returns: {client_info["annualised_returns"]:.2f}%<br>AUM: ₹{client_info["current_aum"]:.2f} Cr<br>Portfolio: {client_info["portfolio_type"]}<br>Risk: {client_info["risk_profile"]}<extra></extra>'
            ))
        
        fig_risk_return.update_layout(
            title="Selected Clients vs All Clients (Returns vs AUM)",
            xaxis_title="Annualised Returns (%)",
            yaxis_title="Current AUM (₹ Crores)",
            height=500,
            template=self.chart_themes[theme]
        )
        
        charts['risk_return_comparison'] = fig_risk_return
        
        return charts
    
    def render_individual_client_analysis(self, data: pd.DataFrame):
        """Render individual client analysis tab"""
        
        st.markdown("## 👤 Individual Client Analysis & Comparison")
        st.markdown("Select clients to analyze their performance, portfolio composition, and compare against peers.")
        
        # Client selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create client options with names and IDs
            client_options = []
            for _, row in data.iterrows():
                client_options.append(f"{row['client_name']} ({row['client_id']})")
            
            selected_client_options = st.multiselect(
                "Select Clients for Analysis (up to 5 recommended)",
                client_options,
                max_selections=5,
                help="Choose clients to analyze and compare their performance"
            )
            
            # Extract client IDs from selections
            selected_clients = []
            for option in selected_client_options:
                client_id = option.split('(')[-1].replace(')', '')
                selected_clients.append(client_id)
        
        with col2:
            analysis_theme = st.selectbox(
                "Chart Theme",
                ["default", "dark", "minimal", "presentation"],
                key="individual_theme"
            )
        
        if not selected_clients:
            st.info("👆 Please select one or more clients from the dropdown above to begin analysis.")
            
            # Show sample client cards for selection help
            st.markdown("### 📋 Sample Clients Available for Analysis")
            
            sample_clients = data.head(6)
            cols = st.columns(3)
            
            for i, (_, client) in enumerate(sample_clients.iterrows()):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="note-card">
                        <strong>{client['client_name']}</strong><br>
                        <small>ID: {client['client_id']}</small><br>
                        AUM: ₹{client['current_aum']:.2f} Cr<br>
                        Returns: {client['annualised_returns']:.2f}%<br>
                        Type: {client['portfolio_type']}<br>
                        RM: {client['rm_name']}
                    </div>
                    """, unsafe_allow_html=True)
            
            return
        
        # Filter data for selected clients
        selected_data = data[data['client_id'].isin(selected_clients)]
        
        # Display selected client summary
        st.markdown("### 📊 Selected Clients Summary")
        
        cols = st.columns(len(selected_clients))
        for i, (_, client) in enumerate(selected_data.iterrows()):
            with cols[i]:
                performance_color = "green" if client['annualised_returns'] > client['bse_500_benchmark_returns'] else "red"
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, {'#10b981' if performance_color == 'green' else '#ef4444'}, {'#059669' if performance_color == 'green' else '#dc2626'});">
                    <div class="metric-value">{client['client_name']}</div>
                    <div class="metric-label">{client['client_id']}</div>
                    <hr style="margin: 0.5rem 0; border-color: rgba(255,255,255,0.3);">
                    <div style="font-size: 1.2rem; font-weight: bold;">₹{client['current_aum']:.2f} Cr</div>
                    <div style="font-size: 1rem;">{client['annualised_returns']:.2f}% Returns</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">{client['portfolio_type']} | {client['risk_profile']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Create and display individual client charts
        charts = self.create_individual_client_analysis(data, selected_clients, analysis_theme)
        
        # Display charts
        for chart_name, chart in charts.items():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed comparison table
        st.markdown("### 📋 Detailed Client Comparison")
        
        comparison_data = selected_data[[
            'client_id', 'client_name', 'current_aum', 'annualised_returns', 
            'bse_500_benchmark_returns', 'portfolio_type', 'risk_profile', 
            'rm_name', 'age_of_client', 'client_since', 'city'
        ]].copy()
        
        # Add calculated fields
        comparison_data['alpha'] = comparison_data['annualised_returns'] - comparison_data['bse_500_benchmark_returns']
        comparison_data['aum_rank'] = comparison_data['current_aum'].rank(ascending=False, method='min').astype(int)
        comparison_data['returns_rank'] = comparison_data['annualised_returns'].rank(ascending=False, method='min').astype(int)
        
        # Format for display
        display_comparison = comparison_data.copy()
        display_comparison['current_aum'] = display_comparison['current_aum'].apply(lambda x: f"₹{x:.2f} Cr")
        display_comparison['annualised_returns'] = display_comparison['annualised_returns'].apply(lambda x: f"{x:.2f}%")
        display_comparison['bse_500_benchmark_returns'] = display_comparison['bse_500_benchmark_returns'].apply(lambda x: f"{x:.2f}%")
        display_comparison['alpha'] = display_comparison['alpha'].apply(lambda x: f"{x:.2f}%")
        display_comparison['client_since'] = display_comparison['client_since'].apply(lambda x: f"{x:.1f} years")
        
        # Rename columns
        display_comparison.columns = [
            'Client ID', 'Client Name', 'AUM', 'Returns', 'Benchmark', 
            'Portfolio Type', 'Risk Profile', 'RM', 'Age', 'Tenure', 'City',
            'Alpha', 'AUM Rank', 'Returns Rank'
        ]
        
        st.dataframe(display_comparison, use_container_width=True)
        
        # Individual client flows if available
        flows_data = self.flows_tracker.load_flows_data()
        if len(flows_data) > 0:
            client_flows = flows_data[flows_data['client_id'].isin(selected_clients)]
            
            if len(client_flows) > 0:
                st.markdown("### 💰 Transaction History for Selected Clients")
                
                # Flow summary by client
                flow_summary = client_flows.groupby(['client_id', 'transaction_label']).agg({
                    'amount': 'sum'
                }).reset_index()
                
                fig_flows = px.bar(
                    flow_summary,
                    x='client_id',
                    y='amount',
                    color='transaction_label',
                    title="Transaction Summary by Client",
                    labels={'amount': 'Amount (₹ Crores)', 'client_id': 'Client ID'},
                    height=400
                )
                fig_flows.update_layout(template=self.chart_themes[analysis_theme])
                
                st.plotly_chart(fig_flows, use_container_width=True)
                
                # Recent transactions table
                recent_flows = client_flows.sort_values('transaction_date', ascending=False).head(20)
                st.markdown("#### Recent Transactions")
                st.dataframe(
                    recent_flows[['client_id', 'client_name', 'transaction_date', 'transaction_label', 'amount', 'description']],
                    use_container_width=True
                )
        
        # Export selected client data
        if st.button("📥 Export Selected Client Analysis"):
            export_data = selected_data.copy()
            csv = export_data.to_csv(index=False)
            st.download_button(
                label="Download Selected Clients CSV",
                data=csv,
                file_name=f"selected_clients_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    def render_client_notes_section(self, client_id: str = None):
        """Render client notes management section"""
        st.markdown("### 📝 Client Notes Management")
        
        # Generate sample notes if not exists
        conn = sqlite3.connect(self.db_path)
        
        try:
            notes_data = pd.read_sql_query("SELECT * FROM client_notes ORDER BY note_date DESC", conn)
            if len(notes_data) == 0:
                raise ValueError("No notes found")
        except:
            # Generate sample notes
            client_ids = pd.read_sql_query("SELECT client_id FROM clients LIMIT 50", conn)['client_id'].tolist()
            sample_notes = self.generate_sample_notes(client_ids)
            sample_notes.to_sql('client_notes', conn, if_exists='replace', index=False)
            notes_data = sample_notes
        
        conn.close()
        
        # Filter by client if specified
        if client_id:
            notes_data = notes_data[notes_data['client_id'] == client_id]
        
        # Notes filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            note_type_filter = st.selectbox("Note Type", ['All'] + list(notes_data['note_type'].unique()))
        
        with col2:
            priority_filter = st.selectbox("Priority", ['All'] + list(notes_data['priority'].unique()))
        
        with col3:
            date_range = st.date_input(
                "Date Range",
                value=(datetime.now() - timedelta(days=30), datetime.now()),
                max_value=datetime.now()
            )
        
        # Apply filters
        filtered_notes = notes_data.copy()
        
        if note_type_filter != 'All':
            filtered_notes = filtered_notes[filtered_notes['note_type'] == note_type_filter]
        
        if priority_filter != 'All':
            filtered_notes = filtered_notes[filtered_notes['priority'] == priority_filter]
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_notes = filtered_notes[
                (pd.to_datetime(filtered_notes['note_date']).dt.date >= start_date) &
                (pd.to_datetime(filtered_notes['note_date']).dt.date <= end_date)
            ]
        
        # Display notes
        if len(filtered_notes) > 0:
            for _, note in filtered_notes.head(10).iterrows():
                priority_class = f"note-priority-{note['priority'].lower()}"
                st.markdown(f"""
                <div class="note-card {priority_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <strong>{note['client_id']} - {note['note_type']}</strong>
                        <span style="font-size: 0.9rem; opacity: 0.8;">{note['note_date']} | {note['priority']} Priority</span>
                    </div>
                    <p style="margin: 0;">{note['note_text']}</p>
                    <div style="margin-top: 0.5rem; font-size: 0.8rem; opacity: 0.7;">
                        Created by: {note['created_by']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No notes found for the selected criteria.")
        
        # Add new note section
        with st.expander("➕ Add New Note"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_client_id = st.text_input("Client ID")
                new_note_type = st.selectbox("Note Type", ["Meeting", "Call", "Email", "Review", "Alert", "Follow-up"])
            
            with col2:
                new_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
                new_created_by = st.text_input("Created By", value="Current User")
            
            new_note_text = st.text_area("Note Text")
            
            if st.button("Add Note"):
                if new_client_id and new_note_text:
                    # Add note to database
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        INSERT INTO client_notes (client_id, note_date, note_text, note_type, priority, created_by)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (new_client_id, datetime.now().strftime('%Y-%m-%d'), new_note_text, 
                          new_note_type, new_priority, new_created_by))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("Note added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in Client ID and Note Text.")

def main():
    """Main application function"""
    dashboard = AdvancedAnalyticsDashboard()
    
    # Apply CSS
    dashboard.render_advanced_css()
    
    # Load data
    data = dashboard.load_data()
    
    # Header
    st.markdown('<h1 class="main-header">📊 PMS Intelligence Hub - Advanced Analytics</h1>', unsafe_allow_html=True)
    st.markdown("**Powered by Vulnuris** | Comprehensive Graphical Overviews with Multiple Perspectives")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Client Overview", "💰 Client Flows", "👤 Individual Analysis", "📝 Notes Management"])
    
    with tab1:
        dashboard.render_client_overview(data)
    
    with tab2:
        dashboard.render_client_flows(data)
    
    with tab3:
        dashboard.render_individual_client_analysis(data)
    
    with tab4:
        dashboard.render_client_notes_section()

if __name__ == "__main__":
    main()

