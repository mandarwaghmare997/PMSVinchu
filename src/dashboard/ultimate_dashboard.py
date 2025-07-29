"""
Ultimate PMS Intelligence Hub Dashboard
Comprehensive dashboard with all advanced features and optimizations
Author: Vulnuris Development Team
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import io
import base64
from datetime import datetime, timedelta
import json
import hashlib
from typing import Dict, List, Optional, Tuple, Union
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from analytics.financial_metrics import AdvancedFinancialMetrics, PortfolioAttributionAnalysis
    from dashboard.components.advanced_charts import OptimizedChartGenerator, ChartOptimizer
    from dashboard.styles.enhanced_styles import EnhancedUIStyles
    from integrations.api_connectors import create_api_connectors, IntegratedDataManager
except ImportError as e:
    st.error(f"Import error: {e}. Some advanced features may not be available.")

# Page configuration
st.set_page_config(
    page_title="PMS Intelligence Hub - Ultimate Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class UltimateDataManager:
    """
    Ultimate data manager with all optimizations and features
    """
    
    def __init__(self, db_path: str = "pms_data.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database with optimized schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create optimized tables with proper indexing
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id TEXT PRIMARY KEY,
            client_name TEXT NOT NULL,
            inception_date DATE,
            age_years INTEGER,
            client_since_years REAL,
            mobile TEXT,
            email TEXT,
            distributor_name TEXT,
            current_aum REAL,
            initial_corpus REAL,
            additions REAL,
            withdrawals REAL,
            net_corpus REAL,
            annualized_returns REAL,
            benchmark_returns REAL,
            rm_name TEXT,
            portfolio_type TEXT,
            risk_profile TEXT,
            city TEXT,
            state TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT,
            date DATE,
            portfolio_value REAL,
            benchmark_value REAL,
            returns REAL,
            benchmark_returns REAL,
            FOREIGN KEY (client_id) REFERENCES clients (client_id)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS upload_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            records_count INTEGER,
            status TEXT,
            file_hash TEXT UNIQUE
        )
        """)
        
        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_clients_rm ON clients(rm_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_clients_type ON clients(portfolio_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_clients_aum ON clients(current_aum)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_performance_client ON performance_history(client_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_performance_date ON performance_history(date)")
        
        conn.commit()
        conn.close()
    
    @st.cache_data(ttl=300)
    def load_data(_self) -> pd.DataFrame:
        """Load data from database with caching"""
        try:
            conn = sqlite3.connect(_self.db_path)
            df = pd.read_sql_query("SELECT * FROM clients ORDER BY current_aum DESC", conn)
            conn.close()
            
            if df.empty:
                return _self.generate_comprehensive_sample_data()
            
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return _self.generate_comprehensive_sample_data()
    
    def generate_comprehensive_sample_data(self, num_records: int = 150) -> pd.DataFrame:
        """Generate comprehensive sample data with realistic financial metrics"""
        np.random.seed(42)  # For reproducible results
        
        # Indian cities and states for realistic data
        cities_states = [
            ("Mumbai", "Maharashtra"), ("Delhi", "Delhi"), ("Bangalore", "Karnataka"),
            ("Hyderabad", "Telangana"), ("Chennai", "Tamil Nadu"), ("Kolkata", "West Bengal"),
            ("Pune", "Maharashtra"), ("Ahmedabad", "Gujarat"), ("Jaipur", "Rajasthan"),
            ("Surat", "Gujarat"), ("Lucknow", "Uttar Pradesh"), ("Kanpur", "Uttar Pradesh"),
            ("Nagpur", "Maharashtra"), ("Indore", "Madhya Pradesh"), ("Thane", "Maharashtra"),
            ("Bhopal", "Madhya Pradesh"), ("Visakhapatnam", "Andhra Pradesh"), ("Pimpri", "Maharashtra"),
            ("Patna", "Bihar"), ("Vadodara", "Gujarat"), ("Ghaziabad", "Uttar Pradesh"),
            ("Ludhiana", "Punjab"), ("Agra", "Uttar Pradesh"), ("Nashik", "Maharashtra"),
            ("Faridabad", "Haryana"), ("Meerut", "Uttar Pradesh"), ("Rajkot", "Gujarat"),
            ("Kalyan", "Maharashtra"), ("Vasai", "Maharashtra"), ("Varanasi", "Uttar Pradesh"),
            ("Srinagar", "Jammu and Kashmir"), ("Aurangabad", "Maharashtra"), ("Dhanbad", "Jharkhand"),
            ("Amritsar", "Punjab"), ("Navi Mumbai", "Maharashtra"), ("Allahabad", "Uttar Pradesh"),
            ("Ranchi", "Jharkhand"), ("Howrah", "West Bengal"), ("Coimbatore", "Tamil Nadu"),
            ("Jabalpur", "Madhya Pradesh"), ("Gwalior", "Madhya Pradesh"), ("Vijayawada", "Andhra Pradesh"),
            ("Jodhpur", "Rajasthan"), ("Madurai", "Tamil Nadu"), ("Raipur", "Chhattisgarh"),
            ("Kota", "Rajasthan"), ("Chandigarh", "Chandigarh"), ("Guwahati", "Assam"),
            ("Solapur", "Maharashtra"), ("Hubli", "Karnataka"), ("Tiruchirappalli", "Tamil Nadu")
        ]
        
        # Relationship Managers
        rm_names = [
            "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Gupta", "Vikram Singh",
            "Anita Desai", "Rohit Agarwal", "Kavya Nair", "Suresh Reddy", "Meera Joshi",
            "Arjun Mehta", "Pooja Verma", "Kiran Rao", "Deepak Malhotra", "Ritu Bansal"
        ]
        
        # Portfolio types and risk profiles
        portfolio_types = ["Equity Growth", "Balanced", "Conservative", "Aggressive Growth", "Income", "Hybrid"]
        risk_profiles = ["Conservative", "Moderate", "Aggressive", "Very Aggressive"]
        
        # Distributor names
        distributors = [
            "Wealth Advisors Ltd", "Investment Partners", "Capital Growth Associates",
            "Financial Planning Co", "Asset Management Services", "Portfolio Solutions",
            "Investment Consultants", "Wealth Management Group", "Financial Advisors Inc",
            "Capital Investment Partners"
        ]
        
        data = []
        
        for i in range(num_records):
            city, state = cities_states[i % len(cities_states)]
            
            # Generate realistic financial data
            base_aum = np.random.lognormal(mean=2.5, sigma=1.2)  # Log-normal for realistic AUM distribution
            current_aum = max(0.5, base_aum)  # Minimum 0.5 Cr
            
            initial_corpus = current_aum * np.random.uniform(0.3, 0.8)
            additions = current_aum * np.random.uniform(0.1, 0.5)
            withdrawals = current_aum * np.random.uniform(0.0, 0.3)
            net_corpus = initial_corpus + additions - withdrawals
            
            # Realistic returns based on portfolio type
            portfolio_type = np.random.choice(portfolio_types)
            risk_profile = np.random.choice(risk_profiles)
            
            # Returns based on risk profile
            if risk_profile == "Conservative":
                base_return = np.random.normal(8, 3)
                benchmark_return = np.random.normal(7, 2)
            elif risk_profile == "Moderate":
                base_return = np.random.normal(12, 5)
                benchmark_return = np.random.normal(10, 3)
            elif risk_profile == "Aggressive":
                base_return = np.random.normal(16, 8)
                benchmark_return = np.random.normal(13, 5)
            else:  # Very Aggressive
                base_return = np.random.normal(20, 12)
                benchmark_return = np.random.normal(15, 7)
            
            # Ensure reasonable bounds
            annualized_returns = max(-30, min(50, base_return))
            benchmark_returns = max(-25, min(40, benchmark_return))
            
            # Client demographics
            age_years = np.random.randint(25, 75)
            client_since_years = np.random.uniform(0.5, 15)
            inception_date = datetime.now() - timedelta(days=int(client_since_years * 365))
            
            record = {
                'client_id': f"CL{i+1:04d}",
                'client_name': f"Client {i+1:03d}",
                'inception_date': inception_date.strftime('%Y-%m-%d'),
                'age_years': age_years,
                'client_since_years': round(client_since_years, 1),
                'mobile': f"+91{np.random.randint(7000000000, 9999999999)}",
                'email': f"client{i+1:03d}@email.com",
                'distributor_name': np.random.choice(distributors),
                'current_aum': round(current_aum, 2),
                'initial_corpus': round(initial_corpus, 2),
                'additions': round(additions, 2),
                'withdrawals': round(withdrawals, 2),
                'net_corpus': round(net_corpus, 2),
                'annualized_returns': round(annualized_returns, 2),
                'benchmark_returns': round(benchmark_returns, 2),
                'rm_name': np.random.choice(rm_names),
                'portfolio_type': portfolio_type,
                'risk_profile': risk_profile,
                'city': city,
                'state': state
            }
            
            data.append(record)
        
        df = pd.DataFrame(data)
        
        # Save to database
        self.save_data_to_db(df)
        
        return df
    
    def save_data_to_db(self, df: pd.DataFrame):
        """Save data to database with conflict resolution"""
        try:
            conn = sqlite3.connect(self.db_path)
            df.to_sql('clients', conn, if_exists='replace', index=False)
            conn.close()
        except Exception as e:
            st.error(f"Error saving data: {e}")
    
    def upload_file(self, uploaded_file) -> Tuple[bool, str, pd.DataFrame]:
        """Process uploaded file with validation and deduplication"""
        try:
            # Calculate file hash for deduplication
            file_content = uploaded_file.read()
            file_hash = hashlib.md5(file_content).hexdigest()
            uploaded_file.seek(0)  # Reset file pointer
            
            # Check if file already uploaded
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT filename FROM upload_history WHERE file_hash = ?", (file_hash,))
            existing = cursor.fetchone()
            
            if existing:
                conn.close()
                return False, f"File already uploaded: {existing[0]}", pd.DataFrame()
            
            # Read file based on extension
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            else:
                conn.close()
                return False, "Unsupported file format. Please upload CSV or Excel files.", pd.DataFrame()
            
            # Validate and clean data
            df = self.validate_and_clean_data(df)
            
            if df.empty:
                conn.close()
                return False, "No valid data found in file.", pd.DataFrame()
            
            # Merge with existing data
            existing_df = self.load_data()
            merged_df = self.merge_data(existing_df, df)
            
            # Save merged data
            self.save_data_to_db(merged_df)
            
            # Record upload history
            cursor.execute("""
                INSERT INTO upload_history (filename, records_count, status, file_hash)
                VALUES (?, ?, ?, ?)
            """, (uploaded_file.name, len(df), "Success", file_hash))
            
            conn.commit()
            conn.close()
            
            return True, f"Successfully uploaded {len(df)} records", merged_df
            
        except Exception as e:
            return False, f"Error processing file: {str(e)}", pd.DataFrame()
    
    def validate_and_clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and clean uploaded data"""
        # Define required columns and their mappings
        column_mappings = {
            'client_id': ['client_id', 'id', 'client id'],
            'client_name': ['client_name', 'name', 'client name'],
            'current_aum': ['current_aum', 'aum', 'current aum', 'nav bucket'],
            'annualized_returns': ['annualized_returns', 'returns', 'annualized returns'],
            'benchmark_returns': ['benchmark_returns', 'benchmark', 'bse 500 tri benchmark returns']
        }
        
        # Normalize column names
        df.columns = df.columns.str.lower().str.strip()
        
        # Map columns
        for standard_col, possible_names in column_mappings.items():
            for possible_name in possible_names:
                if possible_name in df.columns:
                    df[standard_col] = df[possible_name]
                    break
        
        # Fill missing values with defaults
        if 'client_id' not in df.columns:
            df['client_id'] = [f"UPL{i+1:04d}" for i in range(len(df))]
        
        if 'client_name' not in df.columns:
            df['client_name'] = [f"Uploaded Client {i+1}" for i in range(len(df))]
        
        # Clean numeric columns
        numeric_columns = ['current_aum', 'annualized_returns', 'benchmark_returns']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove rows with invalid data
        df = df.dropna(subset=['client_id', 'client_name'])
        
        return df
    
    def merge_data(self, existing_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
        """Intelligently merge new data with existing data"""
        if existing_df.empty:
            return new_df
        
        if new_df.empty:
            return existing_df
        
        # Merge on client_id, updating existing records and adding new ones
        merged_df = pd.concat([existing_df, new_df], ignore_index=True)
        merged_df = merged_df.drop_duplicates(subset=['client_id'], keep='last')
        
        return merged_df
    
    def clear_all_data(self):
        """Clear all data from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients")
            cursor.execute("DELETE FROM performance_history")
            cursor.execute("DELETE FROM upload_history")
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Error clearing data: {e}")
            return False

class UltimateDashboard:
    """
    Ultimate dashboard class with all features and optimizations
    """
    
    def __init__(self):
        self.data_manager = UltimateDataManager()
        self.financial_metrics = AdvancedFinancialMetrics()
        self.chart_generator = OptimizedChartGenerator()
        self.ui_styles = EnhancedUIStyles()
        self.chart_optimizer = ChartOptimizer()
        
        # Initialize session state
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
        if 'current_data' not in st.session_state:
            st.session_state.current_data = pd.DataFrame()
    
    def run(self):
        """Main dashboard execution"""
        # Inject global styles
        self.ui_styles.inject_global_styles()
        
        # Header
        self.render_header()
        
        # Sidebar
        self.render_sidebar()
        
        # Main content
        self.render_main_content()
    
    def render_header(self):
        """Render enhanced header"""
        st.markdown("""
        <div class="main-header">
            <h1>🏦 PMS Intelligence Hub - Ultimate Dashboard</h1>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render enhanced sidebar with all controls"""
        with st.sidebar:
            st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
            
            # Data Management Section
            st.markdown(self.ui_styles.create_section_header(
                "📁 Data Management", 
                "Upload and manage your portfolio data"
            ), unsafe_allow_html=True)
            
            # File Upload
            uploaded_file = st.file_uploader(
                "Upload Excel/CSV File",
                type=['csv', 'xlsx', 'xls'],
                help="Upload client data in Excel or CSV format"
            )
            
            if uploaded_file:
                with st.spinner("Processing file..."):
                    success, message, new_data = self.data_manager.upload_file(uploaded_file)
                    
                    if success:
                        st.success(message)
                        st.session_state.current_data = new_data
                        st.session_state.data_loaded = True
                        st.rerun()
                    else:
                        st.error(message)
            
            # Data Actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Refresh Data", use_container_width=True):
                    st.cache_data.clear()
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Clear All", use_container_width=True):
                    if st.session_state.get('confirm_clear', False):
                        if self.data_manager.clear_all_data():
                            st.success("All data cleared!")
                            st.session_state.data_loaded = False
                            st.session_state.current_data = pd.DataFrame()
                            st.cache_data.clear()
                            st.rerun()
                        st.session_state.confirm_clear = False
                    else:
                        st.session_state.confirm_clear = True
                        st.warning("Click again to confirm deletion")
            
            st.divider()
            
            # Load current data
            if not st.session_state.data_loaded or st.session_state.current_data.empty:
                st.session_state.current_data = self.data_manager.load_data()
                st.session_state.data_loaded = True
            
            data = st.session_state.current_data
            
            if not data.empty:
                # Filters Section
                st.markdown(self.ui_styles.create_section_header(
                    "🔍 Filters", 
                    "Filter data for analysis"
                ), unsafe_allow_html=True)
                
                # Relationship Manager Filter
                rm_options = ['All'] + sorted(data['rm_name'].dropna().unique().tolist())
                selected_rm = st.selectbox("Relationship Manager", rm_options)
                
                # Portfolio Type Filter
                portfolio_options = ['All'] + sorted(data['portfolio_type'].dropna().unique().tolist())
                selected_portfolio = st.selectbox("Portfolio Type", portfolio_options)
                
                # Risk Profile Filter
                risk_options = ['All'] + sorted(data['risk_profile'].dropna().unique().tolist())
                selected_risk = st.selectbox("Risk Profile", risk_options)
                
                # AUM Range Filter
                if 'current_aum' in data.columns:
                    min_aum, max_aum = float(data['current_aum'].min()), float(data['current_aum'].max())
                    aum_range = st.slider(
                        "AUM Range (Cr)",
                        min_value=min_aum,
                        max_value=max_aum,
                        value=(min_aum, max_aum),
                        step=0.1
                    )
                else:
                    aum_range = (0, 100)
                
                # Apply filters
                filtered_data = self.apply_filters(
                    data, selected_rm, selected_portfolio, 
                    selected_risk, aum_range
                )
                
                st.session_state.filtered_data = filtered_data
                
                # Display filter summary
                st.markdown(self.ui_styles.create_info_box(
                    "Filter Summary",
                    f"Showing {len(filtered_data)} of {len(data)} records",
                    "info"
                ), unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def apply_filters(self, data: pd.DataFrame, rm: str, portfolio: str, 
                     risk: str, aum_range: Tuple[float, float]) -> pd.DataFrame:
        """Apply filters to data"""
        filtered = data.copy()
        
        if rm != 'All':
            filtered = filtered[filtered['rm_name'] == rm]
        
        if portfolio != 'All':
            filtered = filtered[filtered['portfolio_type'] == portfolio]
        
        if risk != 'All':
            filtered = filtered[filtered['risk_profile'] == risk]
        
        if 'current_aum' in filtered.columns:
            filtered = filtered[
                (filtered['current_aum'] >= aum_range[0]) & 
                (filtered['current_aum'] <= aum_range[1])
            ]
        
        return filtered
    
    def render_main_content(self):
        """Render main dashboard content"""
        if 'filtered_data' not in st.session_state:
            st.session_state.filtered_data = st.session_state.current_data
        
        data = st.session_state.filtered_data
        
        if data.empty:
            st.markdown(self.ui_styles.create_info_box(
                "No Data Available",
                "Please upload data or adjust your filters to see results.",
                "warning"
            ), unsafe_allow_html=True)
            return
        
        # Key Metrics
        self.render_key_metrics(data)
        
        # Charts Section
        self.render_charts_section(data)
        
        # Data Table
        self.render_data_table(data)
        
        # Export Options
        self.render_export_options(data)
    
    def render_key_metrics(self, data: pd.DataFrame):
        """Render key metrics cards"""
        st.markdown(self.ui_styles.create_section_header(
            "📊 Key Metrics", 
            "Overview of portfolio performance and client metrics"
        ), unsafe_allow_html=True)
        
        # Calculate metrics
        total_aum = data['current_aum'].sum() if 'current_aum' in data.columns else 0
        total_clients = len(data)
        avg_aum = data['current_aum'].mean() if 'current_aum' in data.columns else 0
        avg_returns = data['annualized_returns'].mean() if 'annualized_returns' in data.columns else 0
        
        # Create metrics cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(self.ui_styles.create_metric_card(
                "Total AUM",
                f"₹{total_aum:.1f} Cr",
                "+5.2%",
                "positive",
                "💰"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(self.ui_styles.create_metric_card(
                "Total Clients",
                f"{total_clients:,}",
                "+12",
                "positive",
                "👥"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(self.ui_styles.create_metric_card(
                "Average AUM",
                f"₹{avg_aum:.1f} Cr",
                "+2.1%",
                "positive",
                "📈"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(self.ui_styles.create_metric_card(
                "Avg Returns",
                f"{avg_returns:.1f}%",
                "+0.8%",
                "positive",
                "🎯"
            ), unsafe_allow_html=True)
    
    def render_charts_section(self, data: pd.DataFrame):
        """Render charts section with advanced visualizations"""
        st.markdown(self.ui_styles.create_section_header(
            "📈 Analytics & Visualizations", 
            "Advanced charts and performance analysis"
        ), unsafe_allow_html=True)
        
        # Chart tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Portfolio Overview", 
            "🎯 Performance Analysis", 
            "🔍 Risk Analysis", 
            "👥 Client Analysis"
        ])
        
        with tab1:
            self.render_portfolio_overview_charts(data)
        
        with tab2:
            self.render_performance_analysis_charts(data)
        
        with tab3:
            self.render_risk_analysis_charts(data)
        
        with tab4:
            self.render_client_analysis_charts(data)
    
    def render_portfolio_overview_charts(self, data: pd.DataFrame):
        """Render portfolio overview charts"""
        col1, col2 = st.columns(2)
        
        with col1:
            # AUM Distribution by Portfolio Type
            if 'portfolio_type' in data.columns and 'current_aum' in data.columns:
                aum_by_type = data.groupby('portfolio_type')['current_aum'].sum()
                fig = self.chart_generator.create_sector_allocation_chart(
                    aum_by_type, "AUM Distribution by Portfolio Type"
                )
                st.plotly_chart(fig, use_container_width=True, config=self.chart_generator.chart_config)
        
        with col2:
            # Risk Profile Distribution
            if 'risk_profile' in data.columns:
                risk_dist = data['risk_profile'].value_counts()
                fig = px.pie(
                    values=risk_dist.values,
                    names=risk_dist.index,
                    title="Client Distribution by Risk Profile",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(template="plotly_white", height=400)
                st.plotly_chart(fig, use_container_width=True, config=self.chart_generator.chart_config)
        
        # AUM Trend (simulated)
        if 'current_aum' in data.columns:
            # Generate simulated time series data
            dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='M')
            base_aum = data['current_aum'].sum()
            trend_data = []
            
            for i, date in enumerate(dates):
                # Simulate growth with some volatility
                growth_factor = 1 + (i * 0.01) + np.random.normal(0, 0.02)
                aum_value = base_aum * growth_factor
                trend_data.append({'date': date, 'aum': aum_value})
            
            trend_df = pd.DataFrame(trend_data)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=trend_df['date'],
                y=trend_df['aum'],
                mode='lines+markers',
                name='Total AUM',
                line=dict(color=self.ui_styles.color_scheme['primary'], width=3),
                marker=dict(size=6)
            ))
            
            fig.update_layout(
                title="AUM Growth Trend",
                xaxis_title="Date",
                yaxis_title="AUM (Cr)",
                template="plotly_white",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True, config=self.chart_generator.chart_config)
    
    def render_performance_analysis_charts(self, data: pd.DataFrame):
        """Render performance analysis charts"""
        if 'annualized_returns' in data.columns and 'benchmark_returns' in data.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Risk-Return Scatter
                fig = self.chart_generator.create_risk_return_scatter(
                    data, 'current_aum', 'portfolio_type', "Risk-Return Analysis"
                )
                st.plotly_chart(fig, use_container_width=True, config=self.chart_generator.chart_config)
            
            with col2:
                # Performance Distribution
                fig = go.Figure()
                
                fig.add_trace(go.Histogram(
                    x=data['annualized_returns'],
                    name='Portfolio Returns',
                    opacity=0.7,
                    nbinsx=20,
                    marker_color=self.ui_styles.color_scheme['primary']
                ))
                
                fig.add_trace(go.Histogram(
                    x=data['benchmark_returns'],
                    name='Benchmark Returns',
                    opacity=0.7,
                    nbinsx=20,
                    marker_color=self.ui_styles.color_scheme['secondary']
                ))
                
                fig.update_layout(
                    title="Returns Distribution",
                    xaxis_title="Returns (%)",
                    yaxis_title="Frequency",
                    template="plotly_white",
                    height=400,
                    barmode='overlay'
                )
                
                st.plotly_chart(fig, use_container_width=True, config=self.chart_generator.chart_config)
            
            # Alpha Analysis
            data_with_alpha = data.copy()
            data_with_alpha['alpha'] = data_with_alpha['annualized_returns'] - data_with_alpha['benchmark_returns']
            
            fig = px.bar(
                data_with_alpha.head(20),
                x='client_name',
                y='alpha',
                color='alpha',
                title="Top 20 Clients - Alpha Analysis",
                color_continuous_scale='RdYlGn',
                labels={'alpha': 'Alpha (%)', 'client_name': 'Client'}
            )
            
            fig.update_layout(
                template="plotly_white",
                height=400,
                xaxis={'tickangle': 45}
            )
            
            st.plotly_chart(fig, use_container_width=True, config=self.chart_generator.chart_config)
    
    def render_risk_analysis_charts(self, data: pd.DataFrame):
        """Render risk analysis charts"""
        # Calculate risk metrics
        if 'annualized_returns' in data.columns:
            returns_data = data['annualized_returns'].dropna()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Risk Metrics Summary
                risk_metrics = {
                    'Volatility': returns_data.std(),
                    'VaR (95%)': np.percentile(returns_data, 5),
                    'Max Return': returns_data.max(),
                    'Min Return': returns_data.min()
                }
                
                metrics_df = pd.DataFrame(list(risk_metrics.items()), columns=['Metric', 'Value'])
                
                fig = px.bar(
                    metrics_df,
                    x='Metric',
                    y='Value',
                    title="Risk Metrics Summary",
                    color='Value',
                    color_continuous_scale='Viridis'
                )
                
                fig.update_layout(template="plotly_white", height=400)
                st.plotly_chart(fig, use_container_width=True, config=self.chart_generator.chart_config)
            
            with col2:
                # Risk vs AUM
                if 'current_aum' in data.columns:
                    fig = px.scatter(
                        data,
                        x='current_aum',
                        y='annualized_returns',
                        size='current_aum',
                        color='risk_profile',
                        title="Risk vs AUM Analysis",
                        labels={
                            'current_aum': 'AUM (Cr)',
                            'annualized_returns': 'Returns (%)'
                        }
                    )
                    
                    fig.update_layout(template="plotly_white", height=400)
                    st.plotly_chart(fig, use_container_width=True, config=self.chart_generator.chart_config)
    
    def render_client_analysis_charts(self, data: pd.DataFrame):
        """Render client analysis charts"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Top Clients by AUM
            if 'current_aum' in data.columns:
                top_clients = data.nlargest(10, 'current_aum')
                
                fig = px.bar(
                    top_clients,
                    x='current_aum',
                    y='client_name',
                    orientation='h',
                    title="Top 10 Clients by AUM",
                    labels={'current_aum': 'AUM (Cr)', 'client_name': 'Client'},
                    color='current_aum',
                    color_continuous_scale='Blues'
                )
                
                fig.update_layout(template="plotly_white", height=400)
                st.plotly_chart(fig, use_container_width=True, config=self.chart_generator.chart_config)
        
        with col2:
            # Geographic Distribution
            if 'state' in data.columns:
                state_dist = data['state'].value_counts().head(10)
                
                fig = px.bar(
                    x=state_dist.index,
                    y=state_dist.values,
                    title="Client Distribution by State (Top 10)",
                    labels={'x': 'State', 'y': 'Number of Clients'},
                    color=state_dist.values,
                    color_continuous_scale='Greens'
                )
                
                fig.update_layout(
                    template="plotly_white",
                    height=400,
                    xaxis={'tickangle': 45}
                )
                
                st.plotly_chart(fig, use_container_width=True, config=self.chart_generator.chart_config)
        
        # RM Performance Analysis
        if 'rm_name' in data.columns and 'current_aum' in data.columns:
            rm_performance = data.groupby('rm_name').agg({
                'current_aum': ['sum', 'count', 'mean'],
                'annualized_returns': 'mean'
            }).round(2)
            
            rm_performance.columns = ['Total AUM', 'Client Count', 'Avg AUM', 'Avg Returns']
            rm_performance = rm_performance.reset_index()
            
            fig = px.scatter(
                rm_performance,
                x='Total AUM',
                y='Avg Returns',
                size='Client Count',
                hover_data=['rm_name', 'Avg AUM'],
                title="Relationship Manager Performance",
                labels={
                    'Total AUM': 'Total AUM (Cr)',
                    'Avg Returns': 'Average Returns (%)'
                }
            )
            
            fig.update_layout(template="plotly_white", height=400)
            st.plotly_chart(fig, use_container_width=True, config=self.chart_generator.chart_config)
    
    def render_data_table(self, data: pd.DataFrame):
        """Render enhanced data table"""
        st.markdown(self.ui_styles.create_section_header(
            "📋 Client Data Table", 
            "Detailed view of all client records"
        ), unsafe_allow_html=True)
        
        # Display options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            show_rows = st.selectbox("Rows to show", [10, 25, 50, 100], index=1)
        
        with col2:
            sort_column = st.selectbox("Sort by", data.columns.tolist())
        
        with col3:
            sort_order = st.selectbox("Sort order", ["Ascending", "Descending"])
        
        # Sort data
        ascending = sort_order == "Ascending"
        sorted_data = data.sort_values(sort_column, ascending=ascending)
        
        # Display table
        st.dataframe(
            sorted_data.head(show_rows),
            use_container_width=True,
            height=400
        )
        
        # Table summary
        st.markdown(self.ui_styles.create_info_box(
            "Table Summary",
            f"Showing {min(show_rows, len(data))} of {len(data)} records, sorted by {sort_column} ({sort_order.lower()})",
            "info"
        ), unsafe_allow_html=True)
    
    def render_export_options(self, data: pd.DataFrame):
        """Render export options"""
        st.markdown(self.ui_styles.create_section_header(
            "📤 Export Options", 
            "Download your data in various formats"
        ), unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # CSV Export
            csv_data = data.to_csv(index=False)
            st.download_button(
                label="📄 Download CSV",
                data=csv_data,
                file_name=f"pms_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Excel Export
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                data.to_excel(writer, sheet_name='Client Data', index=False)
            
            st.download_button(
                label="📊 Download Excel",
                data=excel_buffer.getvalue(),
                file_name=f"pms_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        with col3:
            # JSON Export
            json_data = data.to_json(orient='records', indent=2)
            st.download_button(
                label="🔗 Download JSON",
                data=json_data,
                file_name=f"pms_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

# Main execution
if __name__ == "__main__":
    dashboard = UltimateDashboard()
    dashboard.run()

