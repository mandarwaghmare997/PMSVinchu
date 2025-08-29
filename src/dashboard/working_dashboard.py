"""
PMS Intelligence Hub - Working Advanced Analytics Dashboard
Complete version with all features and professional logo
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

class WorkingAdvancedDashboard:
    """Working Advanced Analytics Dashboard with comprehensive features"""
    
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
        
        conn.commit()
        conn.close()
    
    def render_professional_css(self):
        """Apply professional CSS styling with logo"""
        st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .main {
            font-family: 'Inter', sans-serif;
        }
        
        /* Header with Logo */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .logo-container {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .logo-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            color: white;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
        }
        
        .header-text {
            flex: 1;
        }
        
        .header-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .header-subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
            margin: 0.5rem 0 0 0;
            font-weight: 400;
        }
        
        /* Fixed Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
            margin-bottom: 1rem;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            word-wrap: break-word;
            overflow: hidden;
        }
        
        .metric-value {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
            line-height: 1.1;
            word-break: break-word;
        }
        
        .metric-unit {
            font-size: 1.2rem;
            font-weight: 500;
            opacity: 0.9;
            margin-bottom: 0.3rem;
        }
        
        .metric-label {
            font-size: 0.9rem;
            opacity: 0.8;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            line-height: 1.2;
        }
        
        .advanced-metric {
            background: linear-gradient(135deg, #4facfe, #00f2fe);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(79, 172, 254, 0.3);
            margin-bottom: 1rem;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            word-wrap: break-word;
            overflow: hidden;
        }
        
        .advanced-metric .metric-value {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
            line-height: 1.1;
            word-break: break-word;
        }
        
        .advanced-metric .metric-label {
            font-size: 0.9rem;
            opacity: 0.8;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            line-height: 1.2;
        }
        
        /* Chart Containers */
        .chart-container {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: 1px solid #e1e5e9;
        }
        
        /* Notes Cards */
        .note-card {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding-left: 20px;
            padding-right: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
            color: #495057;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .header-title {
                font-size: 1.8rem;
            }
            
            .header-subtitle {
                font-size: 1rem;
            }
            
            .logo-icon {
                width: 50px;
                height: 50px;
                font-size: 1.5rem;
            }
            
            .metric-value {
                font-size: 1.8rem;
            }
            
            .metric-label {
                font-size: 0.8rem;
            }
        }
        </style>
        """, unsafe_allow_html=True)
    
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
    
    def load_enhanced_sample_data(self) -> pd.DataFrame:
        """Generate comprehensive sample data with Indian context"""
        np.random.seed(42)
        
        # Indian names and cities
        indian_names = [
            "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sunita Singh", "Vikash Gupta",
            "Meera Agarwal", "Suresh Reddy", "Kavita Joshi", "Ravi Verma", "Pooja Mehta",
            "Arjun Nair", "Deepika Rao", "Manoj Tiwari", "Sneha Kapoor", "Rohit Malhotra",
            "Anita Desai", "Kiran Kumar", "Shweta Bansal", "Ajay Sinha", "Rekha Pandey"
        ] * 13  # 260 names
        
        indian_cities = [
            "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", 
            "Ahmedabad", "Jaipur", "Surat", "Lucknow", "Kanpur", "Nagpur", "Indore",
            "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara"
        ]
        
        portfolio_types = ["Equity", "Hybrid", "Debt", "Multi-Asset", "Sectoral"]
        risk_profiles = ["Conservative", "Moderate", "Aggressive", "Balanced"]
        rm_names = ["Rahul Agarwal", "Priya Jain", "Amit Sharma", "Neha Gupta", "Vikram Singh"]
        occupations = ["Business", "Service", "Professional", "Retired", "Self-Employed"]
        
        data = []
        for i in range(250):
            # Generate realistic financial data
            initial_corpus = np.random.uniform(5, 500)  # 5L to 5Cr
            additions = np.random.uniform(0, initial_corpus * 0.5)
            withdrawals = -np.random.uniform(0, initial_corpus * 0.2)
            
            # Calculate returns based on portfolio type and risk
            portfolio_type = np.random.choice(portfolio_types)
            risk_profile = np.random.choice(risk_profiles)
            
            base_return = {
                "Equity": 15, "Hybrid": 12, "Debt": 8, 
                "Multi-Asset": 13, "Sectoral": 18
            }[portfolio_type]
            
            risk_adjustment = {
                "Conservative": -2, "Moderate": 0, 
                "Aggressive": 3, "Balanced": 1
            }[risk_profile]
            
            annualised_returns = base_return + risk_adjustment + np.random.normal(0, 3)
            current_aum = initial_corpus + additions + withdrawals + (initial_corpus * annualised_returns / 100)
            
            data.append({
                'client_id': f'PMS{1000 + i:04d}',
                'client_name': indian_names[i],
                'current_aum': round(current_aum, 2),
                'initial_corpus': round(initial_corpus, 2),
                'additions': round(additions, 2),
                'withdrawals': round(withdrawals, 2),
                'annualised_returns': round(annualised_returns, 2),
                'bse_500_benchmark_returns': round(np.random.uniform(10, 14), 2),
                'portfolio_type': portfolio_type,
                'risk_profile': risk_profile,
                'rm_name': np.random.choice(rm_names),
                'city': np.random.choice(indian_cities),
                'age_of_client': np.random.randint(25, 70),
                'client_since': round(np.random.uniform(0.5, 10), 1),
                'occupation': np.random.choice(occupations),
                'annual_income': round(np.random.uniform(5, 200), 1),
                'mobile': f'+91 {np.random.randint(7000000000, 9999999999)}',
                'email': f'{indian_names[i].lower().replace(" ", ".")}@email.com'
            })
        
        return pd.DataFrame(data)
    
    def calculate_comprehensive_metrics(self, data: pd.DataFrame) -> Dict:
        """Calculate comprehensive portfolio metrics"""
        total_aum = data['current_aum'].sum()
        total_clients = len(data)
        avg_returns = data['annualised_returns'].mean()
        avg_benchmark = data['bse_500_benchmark_returns'].mean()
        alpha = avg_returns - avg_benchmark
        
        # Calculate Sharpe ratio (simplified)
        risk_free_rate = 6.5  # Assume 6.5% risk-free rate
        returns_std = data['annualised_returns'].std()
        sharpe_ratio = (avg_returns - risk_free_rate) / returns_std if returns_std > 0 else 0
        
        # Calculate Beta (simplified)
        beta = np.corrcoef(data['annualised_returns'], data['bse_500_benchmark_returns'])[0, 1]
        if np.isnan(beta):
            beta = 1.0
        
        return {
            'total_aum': total_aum,
            'total_clients': total_clients,
            'avg_returns': avg_returns,
            'alpha': alpha,
            'sharpe_ratio': sharpe_ratio,
            'beta': beta
        }
    
    def create_client_overview_charts(self, data: pd.DataFrame, metrics: Dict, view_type: str, theme: str):
        """Create comprehensive client overview charts"""
        charts = {}
        
        if view_type == "Performance Analysis":
            # Performance scatter plot
            fig_performance = px.scatter(
                data, 
                x='annualised_returns', 
                y='current_aum',
                color='portfolio_type',
                size='client_since',
                hover_data=['client_name', 'rm_name', 'risk_profile'],
                title="Client Performance Analysis - Returns vs AUM",
                labels={'annualised_returns': 'Annualised Returns (%)', 'current_aum': 'Current AUM (₹ Cr)'}
            )
            fig_performance.update_layout(template=self.chart_themes[theme], height=500)
            charts['performance_scatter'] = fig_performance
            
            # Returns distribution
            fig_dist = px.histogram(
                data, 
                x='annualised_returns', 
                color='risk_profile',
                title="Returns Distribution by Risk Profile",
                labels={'annualised_returns': 'Annualised Returns (%)'}
            )
            fig_dist.update_layout(template=self.chart_themes[theme], height=400)
            charts['returns_distribution'] = fig_dist
        
        elif view_type == "Portfolio Composition":
            # Portfolio type distribution
            portfolio_summary = data.groupby('portfolio_type').agg({
                'current_aum': 'sum',
                'client_id': 'count'
            }).reset_index()
            
            fig_portfolio = px.pie(
                portfolio_summary, 
                values='current_aum', 
                names='portfolio_type',
                title="AUM Distribution by Portfolio Type"
            )
            fig_portfolio.update_layout(template=self.chart_themes[theme], height=500)
            charts['portfolio_pie'] = fig_portfolio
            
            # Risk profile analysis
            fig_risk = px.bar(
                data.groupby(['portfolio_type', 'risk_profile']).size().reset_index(name='count'),
                x='portfolio_type',
                y='count',
                color='risk_profile',
                title="Client Distribution by Portfolio Type and Risk Profile"
            )
            fig_risk.update_layout(template=self.chart_themes[theme], height=400)
            charts['risk_analysis'] = fig_risk
        
        elif view_type == "Geographic Analysis":
            # City-wise analysis
            city_summary = data.groupby('city').agg({
                'current_aum': 'sum',
                'annualised_returns': 'mean',
                'client_id': 'count'
            }).reset_index().sort_values('current_aum', ascending=False).head(10)
            
            fig_city = px.bar(
                city_summary,
                x='city',
                y='current_aum',
                title="Top 10 Cities by AUM",
                labels={'current_aum': 'Total AUM (₹ Cr)', 'city': 'City'}
            )
            fig_city.update_layout(template=self.chart_themes[theme], height=500)
            charts['city_analysis'] = fig_city
        
        elif view_type == "Demographic Analysis":
            # Age vs Returns
            fig_age = px.scatter(
                data,
                x='age_of_client',
                y='annualised_returns',
                color='risk_profile',
                size='current_aum',
                title="Age vs Returns Analysis",
                labels={'age_of_client': 'Client Age', 'annualised_returns': 'Returns (%)'}
            )
            fig_age.update_layout(template=self.chart_themes[theme], height=500)
            charts['age_analysis'] = fig_age
        
        elif view_type == "RM Performance":
            # RM performance analysis
            rm_summary = data.groupby('rm_name').agg({
                'current_aum': 'sum',
                'annualised_returns': 'mean',
                'client_id': 'count'
            }).reset_index()
            
            fig_rm = px.bar(
                rm_summary,
                x='rm_name',
                y='current_aum',
                title="RM Performance - Total AUM Managed",
                labels={'current_aum': 'Total AUM (₹ Cr)', 'rm_name': 'Relationship Manager'}
            )
            fig_rm.update_layout(template=self.chart_themes[theme], height=500)
            charts['rm_performance'] = fig_rm
        
        return charts
    
    def create_client_flows_charts(self, flows_data: pd.DataFrame, view_type: str, theme: str):
        """Create client flows analysis charts"""
        charts = {}
        
        if len(flows_data) == 0:
            return charts
        
        if view_type == "Transaction Trends":
            # Monthly transaction trends
            flows_data['transaction_date'] = pd.to_datetime(flows_data['transaction_date'])
            flows_data['month'] = flows_data['transaction_date'].dt.to_period('M')
            
            monthly_flows = flows_data.groupby(['month', 'transaction_label']).agg({
                'amount': 'sum'
            }).reset_index()
            monthly_flows['month'] = monthly_flows['month'].astype(str)
            
            fig_trends = px.line(
                monthly_flows,
                x='month',
                y='amount',
                color='transaction_label',
                title="Monthly Transaction Trends",
                labels={'amount': 'Amount (₹ Cr)', 'month': 'Month'}
            )
            fig_trends.update_layout(template=self.chart_themes[theme], height=500)
            charts['transaction_trends'] = fig_trends
        
        elif view_type == "Client Flow Patterns":
            # Client-wise flow analysis
            client_flows = flows_data.groupby(['client_id', 'transaction_label']).agg({
                'amount': 'sum'
            }).reset_index()
            
            fig_patterns = px.bar(
                client_flows.head(20),  # Top 20 for readability
                x='client_id',
                y='amount',
                color='transaction_label',
                title="Client Flow Patterns (Top 20 Clients)",
                labels={'amount': 'Amount (₹ Cr)', 'client_id': 'Client ID'}
            )
            fig_patterns.update_layout(template=self.chart_themes[theme], height=500)
            charts['client_patterns'] = fig_patterns
        
        elif view_type == "Seasonal Analysis":
            # Seasonal flow analysis
            flows_data['quarter'] = flows_data['transaction_date'].dt.quarter
            quarterly_flows = flows_data.groupby(['quarter', 'transaction_label']).agg({
                'amount': 'sum'
            }).reset_index()
            
            fig_seasonal = px.bar(
                quarterly_flows,
                x='quarter',
                y='amount',
                color='transaction_label',
                title="Quarterly Flow Analysis",
                labels={'amount': 'Amount (₹ Cr)', 'quarter': 'Quarter'}
            )
            fig_seasonal.update_layout(template=self.chart_themes[theme], height=500)
            charts['seasonal_patterns'] = fig_seasonal
        
        return charts
    
    def render_client_overview(self, data: pd.DataFrame):
        """Render comprehensive client overview"""
        st.markdown("## 📊 Client Overview - Comprehensive Analytics")
        
        # Control panel
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            view_type = st.selectbox(
                "Select Analysis View",
                ["Performance Analysis", "Portfolio Composition", "Geographic Analysis", 
                 "Demographic Analysis", "RM Performance"]
            )
        
        with col2:
            chart_theme = st.selectbox("Chart Theme", ["default", "dark", "minimal", "presentation"])
        
        with col3:
            show_filters = st.checkbox("Show Filters", value=True)
        
        # Apply basic filters if enabled
        filtered_data = data
        if show_filters:
            with st.expander("🔍 Filters", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    rm_filter = st.multiselect("RM", data['rm_name'].unique())
                    if rm_filter:
                        filtered_data = filtered_data[filtered_data['rm_name'].isin(rm_filter)]
                
                with col2:
                    portfolio_filter = st.multiselect("Portfolio Type", data['portfolio_type'].unique())
                    if portfolio_filter:
                        filtered_data = filtered_data[filtered_data['portfolio_type'].isin(portfolio_filter)]
        
        # Calculate metrics
        metrics = self.calculate_comprehensive_metrics(filtered_data)
        
        # Display metrics
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">₹{metrics['total_aum']:.1f}</div>
                <div class="metric-unit">Cr</div>
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
                <div class="metric-label">Alpha</div>
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
        
        # Create and display charts
        charts = self.create_client_overview_charts(filtered_data, metrics, view_type, chart_theme)
        
        for chart_name, chart in charts.items():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Client details table
        st.markdown("## 📋 Client Details")
        st.dataframe(filtered_data, use_container_width=True, height=400)
    
    def render_client_flows(self, data: pd.DataFrame):
        """Render client flows analysis"""
        st.markdown("## 💰 Client Flows - Transaction Analysis")
        
        # Load flows data
        flows_data = self.flows_tracker.load_flows_data()
        
        if len(flows_data) > 0:
            # Flow controls
            col1, col2 = st.columns(2)
            
            with col1:
                flow_view_type = st.selectbox(
                    "Flow Analysis View",
                    ["Transaction Trends", "Client Flow Patterns", "Seasonal Analysis"]
                )
            
            with col2:
                flow_theme = st.selectbox("Flow Chart Theme", ["default", "dark", "minimal", "presentation"], key="flow_theme")
            
            # Create and display flow charts
            flow_charts = self.create_client_flows_charts(flows_data, flow_view_type, flow_theme)
            
            for chart_name, chart in flow_charts.items():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(chart, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Flow summary
            st.markdown("## 📋 Transaction Summary")
            st.dataframe(flows_data.head(100), use_container_width=True, height=400)
        
        else:
            st.info("No flow data available. Generate sample data to see analysis.")
            if st.button("Generate Sample Flow Data"):
                self.flows_tracker.generate_sample_flows()
                st.success("Sample flow data generated!")
                st.rerun()
    
    def render_individual_client_analysis(self, data: pd.DataFrame):
        """Render individual client analysis with comparison"""
        st.markdown("## 👤 Individual Client Analysis & Comparison")
        
        # Client selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            client_options = [f"{row['client_name']} ({row['client_id']})" for _, row in data.iterrows()]
            selected_clients = st.multiselect(
                "Select Clients for Analysis (up to 5)",
                client_options,
                max_selections=5
            )
        
        with col2:
            analysis_theme = st.selectbox("Theme", ["default", "dark", "minimal", "presentation"], key="individual_theme")
        
        if not selected_clients:
            st.info("Please select clients from the dropdown above.")
            
            # Show sample clients
            st.markdown("### Sample Clients Available")
            sample_clients = data.head(6)
            cols = st.columns(3)
            
            for i, (_, client) in enumerate(sample_clients.iterrows()):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="note-card">
                        <strong>{client['client_name']}</strong><br>
                        ID: {client['client_id']}<br>
                        AUM: ₹{client['current_aum']:.2f} Cr<br>
                        Returns: {client['annualised_returns']:.2f}%<br>
                        Type: {client['portfolio_type']}
                    </div>
                    """, unsafe_allow_html=True)
            return
        
        # Extract client IDs
        selected_client_ids = [option.split('(')[-1].replace(')', '') for option in selected_clients]
        selected_data = data[data['client_id'].isin(selected_client_ids)]
        
        # Display selected client summary
        st.markdown("### Selected Clients Summary")
        cols = st.columns(len(selected_client_ids))
        
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
                </div>
                """, unsafe_allow_html=True)
        
        # Performance comparison chart
        if len(selected_data) > 1:
            fig_comparison = go.Figure()
            
            for _, client in selected_data.iterrows():
                fig_comparison.add_trace(go.Bar(
                    name=client['client_name'],
                    x=['Returns', 'Benchmark', 'Alpha'],
                    y=[
                        client['annualised_returns'],
                        client['bse_500_benchmark_returns'],
                        client['annualised_returns'] - client['bse_500_benchmark_returns']
                    ]
                ))
            
            fig_comparison.update_layout(
                title="Performance Comparison",
                xaxis_title="Metrics",
                yaxis_title="Returns (%)",
                template=self.chart_themes[analysis_theme],
                height=500,
                barmode='group'
            )
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_comparison, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed comparison table
        st.markdown("### Detailed Comparison")
        comparison_data = selected_data[[
            'client_id', 'client_name', 'current_aum', 'annualised_returns', 
            'portfolio_type', 'risk_profile', 'rm_name', 'city'
        ]].copy()
        
        st.dataframe(comparison_data, use_container_width=True)
    
    def render_client_notes_section(self):
        """Render client notes management"""
        st.markdown("## 📝 Notes Management")
        
        # Add new note
        with st.expander("Add New Note", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                note_client_id = st.text_input("Client ID")
                note_type = st.selectbox("Note Type", ["General", "Meeting", "Follow-up", "Important"])
            
            with col2:
                note_date = st.date_input("Note Date", datetime.now().date())
                priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            
            note_text = st.text_area("Note Text")
            
            if st.button("Add Note"):
                if note_client_id and note_text:
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        INSERT INTO client_notes (client_id, note_date, note_text, note_type, priority)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (note_client_id, note_date, note_text, note_type, priority))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("Note added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in Client ID and Note Text.")
        
        # Display existing notes
        st.markdown("### Recent Notes")
        
        conn = sqlite3.connect(self.db_path)
        try:
            notes_df = pd.read_sql_query('''
                SELECT * FROM client_notes 
                ORDER BY created_at DESC 
                LIMIT 20
            ''', conn)
            
            if len(notes_df) > 0:
                for _, note in notes_df.iterrows():
                    priority_color = {"Low": "#28a745", "Medium": "#ffc107", "High": "#dc3545"}[note['priority']]
                    st.markdown(f"""
                    <div class="note-card" style="border-left-color: {priority_color};">
                        <strong>{note['client_id']}</strong> - {note['note_type']} 
                        <span style="color: {priority_color}; font-weight: bold;">({note['priority']})</span><br>
                        <small>{note['note_date']}</small><br>
                        {note['note_text']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No notes available. Add some notes to see them here.")
        
        except Exception as e:
            st.error(f"Error loading notes: {e}")
        
        finally:
            conn.close()

def main():
    """Main application function"""
    dashboard = WorkingAdvancedDashboard()
    
    # Apply CSS
    dashboard.render_professional_css()
    
    # Load data
    data = dashboard.load_data()
    
    # Professional Header with Logo
    st.markdown("""
    <div class="main-header">
        <div class="logo-container">
            <div class="logo-icon">📊</div>
            <div class="header-text">
                <h1 class="header-title">PMS Intelligence Hub</h1>
                <p class="header-subtitle">Advanced Analytics | Powered by Vulnuris | Comprehensive Portfolio Management System</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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

