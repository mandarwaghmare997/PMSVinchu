"""
PMS Intelligence Hub - Comprehensive Dashboard
Complete version with all charts, analysis, and advanced features
Author: Vulnuris Development Team
"""

from typing import Dict, List, Optional
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3
import json
import io
from flows_tracker import ClientFlowsTracker

# Page configuration
st.set_page_config(
    page_title="PMS Intelligence Hub - Comprehensive",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ComprehensivePMSHub:
    """Comprehensive PMS Intelligence Hub with all advanced features"""
    
    def __init__(self):
        self.db_path = "pms_client_data.db"
        self.flows_tracker = ClientFlowsTracker(self.db_path)
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database with comprehensive schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create clients table with all fields
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create client notes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT NOT NULL,
                note_date DATE NOT NULL,
                note_text TEXT NOT NULL,
                created_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (client_id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_rm ON clients(rm_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_portfolio ON clients(portfolio_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_aum ON clients(current_aum)')
        
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
            background: linear-gradient(90deg, #1e3a8a, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
            animation: gradient 3s ease-in-out infinite;
        }
        
        @keyframes gradient {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0,0,0,0.2);
        }
        
        .metric-value {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .metric-label {
            font-size: 1.1rem;
            opacity: 0.9;
            font-weight: 500;
        }
        
        .chart-container {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            border: 1px solid #e2e8f0;
        }
        
        .advanced-metric {
            background: linear-gradient(135deg, #ff6b6b, #feca57);
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .performance-indicator {
            background: linear-gradient(135deg, #48cae4, #023e8a);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
        }
        
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        }
        
        .stSelectbox > div > div {
            background-color: #f8fafc;
            border-radius: 12px;
            border: 2px solid #e2e8f0;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            color: white;
            border-radius: 12px;
            border: none;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #1e40af, #2563eb);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        }
        
        .dataframe {
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: #f8fafc;
            padding: 1rem;
            border-radius: 15px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: white;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            border: 2px solid #e2e8f0;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            color: white;
            border-color: #3b82f6;
        }
        
        .top-performer {
            background: linear-gradient(135deg, #10b981, #059669);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 0.5rem;
        }
        
        .risk-indicator {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            text-align: center;
            margin: 0.25rem;
        }
        
        .risk-conservative { background: #10b981; color: white; }
        .risk-moderate { background: #f59e0b; color: white; }
        .risk-aggressive { background: #ef4444; color: white; }
        </style>
        """, unsafe_allow_html=True)
    
    @st.cache_data
    def load_comprehensive_sample_data(_self) -> pd.DataFrame:
        """Load comprehensive sample data with realistic Indian financial data"""
        np.random.seed(42)
        
        # Comprehensive Indian names
        indian_names = [
            "Rajesh Sharma", "Priya Patel", "Amit Kumar", "Sunita Singh", "Vikram Gupta",
            "Anita Joshi", "Suresh Reddy", "Kavita Nair", "Arjun Mehta", "Deepika Iyer",
            "Rohit Agarwal", "Meera Jain", "Sanjay Verma", "Pooja Bansal", "Kiran Rao",
            "Neha Chopra", "Ravi Tiwari", "Shweta Malhotra", "Ajay Saxena", "Ritu Bhatt",
            "Manish Agrawal", "Sneha Kulkarni", "Rahul Desai", "Divya Menon", "Ashok Pandey",
            "Rekha Sinha", "Nitin Jha", "Swati Mishra", "Gaurav Bhardwaj", "Nisha Yadav"
        ]
        
        rm_names = ["Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sunita Gupta", "Vikram Singh", "Neha Agarwal"]
        portfolio_types = ["Equity", "Debt", "Hybrid", "Multi-Asset", "ELSS", "Sectoral"]
        risk_profiles = ["Conservative", "Moderate", "Aggressive", "Very Aggressive"]
        distributors = ["HDFC Securities", "ICICI Direct", "Zerodha", "Angel Broking", "Kotak Securities", "Motilal Oswal"]
        
        data = []
        for i in range(200):  # Increased to 200 clients for better analysis
            client_id = f"CL{i+1:04d}"
            
            # Realistic AUM distribution (in Crores)
            if i < 40:  # Ultra high net worth clients
                current_aum = np.random.uniform(100, 500)
            elif i < 80:  # High net worth clients
                current_aum = np.random.uniform(25, 100)
            elif i < 140:  # Mid-tier clients
                current_aum = np.random.uniform(5, 25)
            else:  # Regular clients
                current_aum = np.random.uniform(0.5, 5)
            
            # Calculate other financial metrics
            initial_corpus = current_aum * np.random.uniform(0.5, 0.8)
            additions = current_aum * np.random.uniform(0.1, 0.5)
            withdrawals = current_aum * np.random.uniform(0.02, 0.15)
            net_corpus = initial_corpus + additions - withdrawals
            
            # Realistic returns based on portfolio type and market conditions
            portfolio_type = np.random.choice(portfolio_types)
            base_return = {
                "Equity": np.random.uniform(8, 28),
                "Debt": np.random.uniform(4, 12),
                "Hybrid": np.random.uniform(6, 20),
                "Multi-Asset": np.random.uniform(7, 22),
                "ELSS": np.random.uniform(10, 30),
                "Sectoral": np.random.uniform(5, 35)
            }[portfolio_type]
            
            # Add some volatility and outliers
            if np.random.random() < 0.1:  # 10% chance of exceptional performance
                annualised_returns = base_return * np.random.uniform(1.2, 1.8)
            elif np.random.random() < 0.1:  # 10% chance of poor performance
                annualised_returns = base_return * np.random.uniform(0.3, 0.7)
            else:
                annualised_returns = base_return
            
            # Benchmark returns with some correlation to market
            bse_500_benchmark = np.random.uniform(8, 16)
            
            # Client demographics
            age = np.random.randint(25, 80)
            client_since = np.random.uniform(0.25, 15)
            inception_date = (datetime.now() - timedelta(days=int(client_since * 365))).strftime('%Y-%m-%d')
            
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
                'risk_profile': np.random.choice(risk_profiles)
            })
        
        return pd.DataFrame(data)
    
    @st.cache_data
    def load_data(_self) -> pd.DataFrame:
        """Load data from database or create comprehensive sample data"""
        conn = sqlite3.connect(_self.db_path)
        
        try:
            # Try to load from database
            data = pd.read_sql_query("SELECT * FROM clients", conn)
            if len(data) == 0:
                raise ValueError("No data in database")
        except:
            # Create and insert comprehensive sample data
            sample_data = _self.load_comprehensive_sample_data()
            sample_data.to_sql('clients', conn, if_exists='replace', index=False)
            data = sample_data
        
        conn.close()
        return data
    
    def calculate_comprehensive_metrics(self, data: pd.DataFrame) -> Dict:
        """Calculate comprehensive portfolio metrics and analytics"""
        total_aum = data['current_aum'].sum()
        total_clients = len(data)
        avg_returns = data['annualised_returns'].mean()
        avg_benchmark = data['bse_500_benchmark_returns'].mean()
        
        # Advanced metrics
        alpha = avg_returns - avg_benchmark
        returns_std = data['annualised_returns'].std()
        sharpe_ratio = (avg_returns - 6) / returns_std if returns_std > 0 else 0  # Assuming 6% risk-free rate
        
        # Beta calculation (simplified)
        beta = np.corrcoef(data['annualised_returns'], data['bse_500_benchmark_returns'])[0, 1] * (returns_std / data['bse_500_benchmark_returns'].std())
        
        # Information ratio
        tracking_error = (data['annualised_returns'] - data['bse_500_benchmark_returns']).std()
        information_ratio = alpha / tracking_error if tracking_error > 0 else 0
        
        # Portfolio composition and distributions
        portfolio_composition = data['portfolio_type'].value_counts().to_dict()
        risk_distribution = data['risk_profile'].value_counts().to_dict()
        rm_distribution = data['rm_name'].value_counts().to_dict()
        
        # Performance quartiles
        returns_quartiles = data['annualised_returns'].quantile([0.25, 0.5, 0.75]).to_dict()
        
        # Top and bottom performers
        top_performers = data.nlargest(10, 'annualised_returns')[['client_name', 'annualised_returns', 'current_aum', 'portfolio_type']]
        bottom_performers = data.nsmallest(5, 'annualised_returns')[['client_name', 'annualised_returns', 'current_aum', 'portfolio_type']]
        
        # AUM distribution analysis
        aum_ranges = {
            '₹0.5-1 Cr': len(data[(data['current_aum'] >= 0.5) & (data['current_aum'] < 1)]),
            '₹1-5 Cr': len(data[(data['current_aum'] >= 1) & (data['current_aum'] < 5)]),
            '₹5-10 Cr': len(data[(data['current_aum'] >= 5) & (data['current_aum'] < 10)]),
            '₹10-25 Cr': len(data[(data['current_aum'] >= 10) & (data['current_aum'] < 25)]),
            '₹25-50 Cr': len(data[(data['current_aum'] >= 25) & (data['current_aum'] < 50)]),
            '₹50-100 Cr': len(data[(data['current_aum'] >= 50) & (data['current_aum'] < 100)]),
            '₹100+ Cr': len(data[data['current_aum'] >= 100])
        }
        
        # Age demographics
        age_ranges = {
            '25-35': len(data[(data['age_of_client'] >= 25) & (data['age_of_client'] < 35)]),
            '35-45': len(data[(data['age_of_client'] >= 35) & (data['age_of_client'] < 45)]),
            '45-55': len(data[(data['age_of_client'] >= 45) & (data['age_of_client'] < 55)]),
            '55-65': len(data[(data['age_of_client'] >= 55) & (data['age_of_client'] < 65)]),
            '65+': len(data[data['age_of_client'] >= 65])
        }
        
        # Client tenure analysis
        tenure_ranges = {
            '< 1 Year': len(data[data['client_since'] < 1]),
            '1-3 Years': len(data[(data['client_since'] >= 1) & (data['client_since'] < 3)]),
            '3-5 Years': len(data[(data['client_since'] >= 3) & (data['client_since'] < 5)]),
            '5-10 Years': len(data[(data['client_since'] >= 5) & (data['client_since'] < 10)]),
            '10+ Years': len(data[data['client_since'] >= 10])
        }
        
        return {
            'total_aum': total_aum,
            'total_clients': total_clients,
            'avg_returns': avg_returns,
            'avg_benchmark': avg_benchmark,
            'alpha': alpha,
            'beta': beta,
            'sharpe_ratio': sharpe_ratio,
            'information_ratio': information_ratio,
            'returns_std': returns_std,
            'tracking_error': tracking_error,
            'portfolio_composition': portfolio_composition,
            'risk_distribution': risk_distribution,
            'rm_distribution': rm_distribution,
            'returns_quartiles': returns_quartiles,
            'top_performers': top_performers,
            'bottom_performers': bottom_performers,
            'aum_ranges': aum_ranges,
            'age_ranges': age_ranges,
            'tenure_ranges': tenure_ranges
        }
    
    def create_advanced_visualizations(self, data: pd.DataFrame, metrics: Dict):
        """Create comprehensive charts and advanced visualizations"""
        
        # 1. Advanced Portfolio Performance Dashboard
        fig_performance = go.Figure()
        
        # Scatter plot with multiple dimensions
        fig_performance.add_trace(go.Scatter(
            x=data['current_aum'],
            y=data['annualised_returns'],
            mode='markers',
            marker=dict(
                size=np.sqrt(data['client_since']) * 3,  # Size based on tenure
                color=data['annualised_returns'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Returns %", x=1.02),
                line=dict(width=1, color='white')
            ),
            text=[f"<b>{name}</b><br>AUM: ₹{aum:.2f} Cr<br>Returns: {ret:.2f}%<br>Tenure: {tenure:.1f} years<br>Type: {ptype}" 
                  for name, aum, ret, tenure, ptype in zip(data['client_name'], data['current_aum'], 
                                                          data['annualised_returns'], data['client_since'], data['portfolio_type'])],
            hovertemplate='%{text}<extra></extra>',
            name='Client Performance'
        ))
        
        # Add benchmark and alpha lines
        fig_performance.add_hline(
            y=metrics['avg_benchmark'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"BSE 500 Benchmark: {metrics['avg_benchmark']:.2f}%",
            annotation_position="top right"
        )
        
        fig_performance.add_hline(
            y=metrics['avg_returns'],
            line_dash="dot",
            line_color="blue",
            annotation_text=f"Portfolio Average: {metrics['avg_returns']:.2f}%",
            annotation_position="bottom right"
        )
        
        fig_performance.update_layout(
            title="Advanced Portfolio Performance Analysis",
            xaxis_title="Assets Under Management (₹ Crores)",
            yaxis_title="Annualised Returns (%)",
            height=600,
            showlegend=True,
            template="plotly_white"
        )
        
        # 2. Multi-dimensional Portfolio Composition
        fig_composition = go.Figure()
        
        # Sunburst chart for hierarchical composition
        portfolio_risk_data = data.groupby(['portfolio_type', 'risk_profile']).size().reset_index(name='count')
        
        fig_composition = px.sunburst(
            portfolio_risk_data,
            path=['portfolio_type', 'risk_profile'],
            values='count',
            title="Portfolio Composition by Type and Risk Profile",
            color='count',
            color_continuous_scale='Blues'
        )
        
        # 3. Risk-Return Scatter with Quadrant Analysis
        fig_risk_return = go.Figure()
        
        # Calculate risk (std dev) for each portfolio type
        portfolio_stats = data.groupby('portfolio_type').agg({
            'annualised_returns': ['mean', 'std'],
            'current_aum': 'sum',
            'client_id': 'count'
        }).round(2)
        
        portfolio_stats.columns = ['avg_return', 'risk', 'total_aum', 'client_count']
        
        fig_risk_return.add_trace(go.Scatter(
            x=portfolio_stats['risk'],
            y=portfolio_stats['avg_return'],
            mode='markers+text',
            marker=dict(
                size=portfolio_stats['client_count'] * 2,
                color=portfolio_stats['avg_return'],
                colorscale='RdYlGn',
                showscale=True,
                line=dict(width=2, color='white')
            ),
            text=portfolio_stats.index,
            textposition="middle center",
            hovertemplate='<b>%{text}</b><br>Risk: %{x:.2f}%<br>Return: %{y:.2f}%<br>Clients: ' + 
                         portfolio_stats['client_count'].astype(str) + '<extra></extra>',
            name='Portfolio Types'
        ))
        
        # Add quadrant lines
        avg_risk = portfolio_stats['risk'].mean()
        avg_return = portfolio_stats['avg_return'].mean()
        
        fig_risk_return.add_vline(x=avg_risk, line_dash="dash", line_color="gray", opacity=0.5)
        fig_risk_return.add_hline(y=avg_return, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig_risk_return.update_layout(
            title="Risk-Return Analysis by Portfolio Type",
            xaxis_title="Risk (Standard Deviation %)",
            yaxis_title="Average Returns (%)",
            height=500,
            template="plotly_white"
        )
        
        # 4. RM Performance Heatmap
        rm_performance = data.groupby(['rm_name', 'portfolio_type']).agg({
            'annualised_returns': 'mean',
            'current_aum': 'sum',
            'client_id': 'count'
        }).round(2)
        
        # Pivot for heatmap
        rm_returns_pivot = rm_performance['annualised_returns'].unstack(fill_value=0)
        
        fig_rm_heatmap = px.imshow(
            rm_returns_pivot.values,
            x=rm_returns_pivot.columns,
            y=rm_returns_pivot.index,
            color_continuous_scale='RdYlGn',
            title="RM Performance Heatmap (Average Returns by Portfolio Type)",
            labels=dict(x="Portfolio Type", y="Relationship Manager", color="Avg Returns %")
        )
        
        # 5. Client Distribution Analysis
        fig_distribution = go.Figure()
        
        # Multiple distribution plots
        fig_distribution.add_trace(go.Histogram(
            x=data['annualised_returns'],
            name='Returns Distribution',
            opacity=0.7,
            nbinsx=30,
            marker_color='blue'
        ))
        
        fig_distribution.add_vline(
            x=metrics['avg_returns'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: {metrics['avg_returns']:.2f}%"
        )
        
        fig_distribution.add_vline(
            x=metrics['returns_quartiles'][0.25],
            line_dash="dot",
            line_color="orange",
            annotation_text=f"Q1: {metrics['returns_quartiles'][0.25]:.2f}%"
        )
        
        fig_distribution.add_vline(
            x=metrics['returns_quartiles'][0.75],
            line_dash="dot",
            line_color="orange",
            annotation_text=f"Q3: {metrics['returns_quartiles'][0.75]:.2f}%"
        )
        
        fig_distribution.update_layout(
            title="Returns Distribution with Quartile Analysis",
            xaxis_title="Annualised Returns (%)",
            yaxis_title="Number of Clients",
            height=400,
            template="plotly_white"
        )
        
        # 6. AUM Growth Trend (Simulated)
        # Create simulated monthly data for trend analysis
        months = pd.date_range(start='2023-01-01', end='2024-08-01', freq='M')
        aum_trend = []
        base_aum = metrics['total_aum'] * 0.8
        
        for i, month in enumerate(months):
            # Simulate growth with some volatility
            growth_rate = np.random.normal(0.02, 0.05)  # 2% monthly growth with volatility
            base_aum *= (1 + growth_rate)
            aum_trend.append(base_aum)
        
        fig_aum_trend = go.Figure()
        fig_aum_trend.add_trace(go.Scatter(
            x=months,
            y=aum_trend,
            mode='lines+markers',
            name='Total AUM',
            line=dict(color='blue', width=3),
            marker=dict(size=6)
        ))
        
        fig_aum_trend.update_layout(
            title="AUM Growth Trend (Simulated)",
            xaxis_title="Month",
            yaxis_title="Total AUM (₹ Crores)",
            height=400,
            template="plotly_white"
        )
        
        return {
            'performance': fig_performance,
            'composition': fig_composition,
            'risk_return': fig_risk_return,
            'rm_heatmap': fig_rm_heatmap,
            'distribution': fig_distribution,
            'aum_trend': fig_aum_trend,
            'portfolio_stats': portfolio_stats
        }
    
    def apply_advanced_filters(self, data: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """Apply comprehensive filters to data"""
        filtered_data = data.copy()
        
        if filters['rm'] != 'All':
            filtered_data = filtered_data[filtered_data['rm_name'] == filters['rm']]
        
        if filters['portfolio_type'] != 'All':
            filtered_data = filtered_data[filtered_data['portfolio_type'] == filters['portfolio_type']]
        
        if filters['risk_profile'] != 'All':
            filtered_data = filtered_data[filtered_data['risk_profile'] == filters['risk_profile']]
        
        # AUM range filter
        aum_min, aum_max = filters['aum_range']
        filtered_data = filtered_data[
            (filtered_data['current_aum'] >= aum_min) & 
            (filtered_data['current_aum'] <= aum_max)
        ]
        
        # Returns range filter
        returns_min, returns_max = filters['returns_range']
        filtered_data = filtered_data[
            (filtered_data['annualised_returns'] >= returns_min) & 
            (filtered_data['annualised_returns'] <= returns_max)
        ]
        
        # Age range filter
        age_min, age_max = filters['age_range']
        filtered_data = filtered_data[
            (filtered_data['age_of_client'] >= age_min) & 
            (filtered_data['age_of_client'] <= age_max)
        ]
        
        # Tenure filter
        tenure_min, tenure_max = filters['tenure_range']
        filtered_data = filtered_data[
            (filtered_data['client_since'] >= tenure_min) & 
            (filtered_data['client_since'] <= tenure_max)
        ]
        
        return filtered_data
    
    def render_comprehensive_dashboard(self, data: pd.DataFrame):
        """Render the comprehensive main dashboard with all advanced features"""
        
        # Apply advanced CSS
        self.render_advanced_css()
        
        st.markdown('<h1 class="main-header">📊 PMS Intelligence Hub - Comprehensive Analytics</h1>', unsafe_allow_html=True)
        st.markdown("**Powered by Vulnuris** | Advanced Portfolio Management Analytics with Complete Feature Set")
        
        # Advanced Sidebar filters
        st.sidebar.header("🔍 Advanced Filters & Controls")
        
        # Get unique values for filters
        rm_options = ['All'] + sorted(data['rm_name'].unique().tolist())
        portfolio_options = ['All'] + sorted(data['portfolio_type'].unique().tolist())
        risk_options = ['All'] + sorted(data['risk_profile'].unique().tolist())
        
        filters = {
            'rm': st.sidebar.selectbox("Relationship Manager", rm_options),
            'portfolio_type': st.sidebar.selectbox("Portfolio Type", portfolio_options),
            'risk_profile': st.sidebar.selectbox("Risk Profile", risk_options),
            'aum_range': st.sidebar.slider(
                "AUM Range (₹ Crores)", 
                float(data['current_aum'].min()), 
                float(data['current_aum'].max()), 
                (float(data['current_aum'].min()), float(data['current_aum'].max())),
                step=0.5
            ),
            'returns_range': st.sidebar.slider(
                "Returns Range (%)", 
                float(data['annualised_returns'].min()), 
                float(data['annualised_returns'].max()), 
                (float(data['annualised_returns'].min()), float(data['annualised_returns'].max())),
                step=0.5
            ),
            'age_range': st.sidebar.slider(
                "Client Age Range", 
                int(data['age_of_client'].min()), 
                int(data['age_of_client'].max()), 
                (int(data['age_of_client'].min()), int(data['age_of_client'].max()))
            ),
            'tenure_range': st.sidebar.slider(
                "Client Tenure (Years)", 
                float(data['client_since'].min()), 
                float(data['client_since'].max()), 
                (float(data['client_since'].min()), float(data['client_since'].max())),
                step=0.1
            )
        }
        
        # Apply filters
        filtered_data = self.apply_advanced_filters(data, filters)
        
        if len(filtered_data) == 0:
            st.warning("⚠️ No data matches the selected filters. Please adjust your criteria.")
            return
        
        # Calculate comprehensive metrics
        metrics = self.calculate_comprehensive_metrics(filtered_data)
        
        # Advanced Key Metrics Row
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">₹{metrics['total_aum']:.1f} Cr</div>
                <div class="metric-label">Total AUM</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{metrics['total_clients']}</div>
                <div class="metric-label">Total Clients</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{metrics['avg_returns']:.2f}%</div>
                <div class="metric-label">Avg Returns</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="advanced-metric">
                <div class="metric-value">{metrics['alpha']:.2f}%</div>
                <div class="metric-label">Alpha vs Benchmark</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
            <div class="advanced-metric">
                <div class="metric-value">{metrics['sharpe_ratio']:.2f}</div>
                <div class="metric-label">Sharpe Ratio</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown(f"""
            <div class="advanced-metric">
                <div class="metric-value">{metrics['beta']:.2f}</div>
                <div class="metric-label">Beta</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional Performance Indicators
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="performance-indicator">
                <strong>Information Ratio:</strong> {metrics['information_ratio']:.2f}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="performance-indicator">
                <strong>Tracking Error:</strong> {metrics['tracking_error']:.2f}%
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="performance-indicator">
                <strong>Volatility:</strong> {metrics['returns_std']:.2f}%
            </div>
            """, unsafe_allow_html=True)
        
        # Create comprehensive charts
        charts = self.create_advanced_visualizations(filtered_data, metrics)
        
        # Advanced Charts Layout
        st.markdown("## 📈 Advanced Portfolio Analytics")
        
        # Row 1: Performance Analysis and Composition
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(charts['performance'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(charts['composition'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Row 2: Risk Analysis and RM Performance
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(charts['risk_return'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(charts['rm_heatmap'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Row 3: Distribution Analysis and Trend
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(charts['distribution'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(charts['aum_trend'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Top Performers Section
        st.markdown("## 🏆 Performance Leaders")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🥇 Top Performing Clients")
            for idx, row in metrics['top_performers'].head(5).iterrows():
                st.markdown(f"""
                <div class="top-performer">
                    <strong>{row['client_name']}</strong><br>
                    Returns: {row['annualised_returns']:.2f}% | AUM: ₹{row['current_aum']:.2f} Cr<br>
                    Type: {row['portfolio_type']}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📊 Portfolio Statistics by Type")
            st.dataframe(
                charts['portfolio_stats'].style.format({
                    'avg_return': '{:.2f}%',
                    'risk': '{:.2f}%',
                    'total_aum': '₹{:.2f} Cr'
                }),
                use_container_width=True
            )
        
        # Detailed Analytics Tables
        st.markdown("## 📋 Detailed Analytics")
        
        # Search functionality
        search_term = st.text_input("🔍 Search clients by name, ID, or RM:")
        if search_term:
            mask = (
                filtered_data['client_name'].str.contains(search_term, case=False, na=False) |
                filtered_data['client_id'].str.contains(search_term, case=False, na=False) |
                filtered_data['rm_name'].str.contains(search_term, case=False, na=False)
            )
            filtered_data = filtered_data[mask]
        
        # Display comprehensive table with formatting
        display_data = filtered_data[[
            'client_id', 'client_name', 'current_aum', 'annualised_returns', 
            'bse_500_benchmark_returns', 'rm_name', 'portfolio_type', 'risk_profile',
            'age_of_client', 'client_since'
        ]].copy()
        
        # Format columns for better display
        display_data['current_aum'] = display_data['current_aum'].apply(lambda x: f"₹{x:.2f} Cr")
        display_data['annualised_returns'] = display_data['annualised_returns'].apply(lambda x: f"{x:.2f}%")
        display_data['bse_500_benchmark_returns'] = display_data['bse_500_benchmark_returns'].apply(lambda x: f"{x:.2f}%")
        display_data['client_since'] = display_data['client_since'].apply(lambda x: f"{x:.1f} years")
        
        # Rename columns for better presentation
        display_data.columns = [
            'Client ID', 'Client Name', 'AUM', 'Returns', 'Benchmark', 
            'RM', 'Portfolio Type', 'Risk Profile', 'Age', 'Tenure'
        ]
        
        st.dataframe(
            display_data,
            use_container_width=True,
            height=500
        )
        
        # Summary Statistics
        st.markdown("## 📈 Summary Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### AUM Distribution")
            aum_df = pd.DataFrame(list(metrics['aum_ranges'].items()), columns=['Range', 'Count'])
            st.dataframe(aum_df, use_container_width=True)
        
        with col2:
            st.markdown("### Age Demographics")
            age_df = pd.DataFrame(list(metrics['age_ranges'].items()), columns=['Age Group', 'Count'])
            st.dataframe(age_df, use_container_width=True)
        
        with col3:
            st.markdown("### Client Tenure")
            tenure_df = pd.DataFrame(list(metrics['tenure_ranges'].items()), columns=['Tenure', 'Count'])
            st.dataframe(tenure_df, use_container_width=True)

def main():
    """Main application function"""
    hub = ComprehensivePMSHub()
    
    # Load data
    data = hub.load_data()
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💰 Client Flows", "📁 Data Management"])
    
    with tab1:
        hub.render_comprehensive_dashboard(data)
    
    with tab2:
        hub.flows_tracker.render_flows_dashboard()
    
    with tab3:
        st.markdown("## 📁 Data Management")
        st.markdown("Upload, export, and manage your portfolio data")
        
        # File upload
        uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx', 'xls'])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    new_data = pd.read_csv(uploaded_file)
                else:
                    new_data = pd.read_excel(uploaded_file)
                
                st.success(f"File uploaded successfully! {len(new_data)} records found.")
                st.dataframe(new_data.head())
                
                if st.button("Import Data"):
                    # Save to database
                    conn = sqlite3.connect(hub.db_path)
                    new_data.to_sql('clients', conn, if_exists='replace', index=False)
                    conn.close()
                    st.success("Data imported successfully!")
                    st.experimental_rerun()
                    
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
        
        # Export functionality
        if st.button("Export Current Data as CSV"):
            csv = data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"pms_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()

