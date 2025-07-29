"""
PMS Intelligence Hub - Enhanced Dashboard
Advanced Streamlit dashboard with data upload, comprehensive analytics, and professional UI
Author: Vulnuris Development Team
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta, date
import json
import base64
import io
import sqlite3
import hashlib
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="PMS Intelligence Hub - Enhanced",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for professional styling
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem 0;
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .success-metric { border-left-color: #28a745; }
    .warning-metric { border-left-color: #ffc107; }
    .danger-metric { border-left-color: #dc3545; }
    .info-metric { border-left-color: #17a2b8; }
    
    /* Upload area styling */
    .upload-area {
        border: 2px dashed #1f77b4;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
        margin: 1rem 0;
    }
    
    /* Data management buttons */
    .data-management {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    
    /* Enhanced sidebar */
    .sidebar-content {
        background: linear-gradient(180deg, #1f77b4 0%, #2ca02c 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* Professional tables */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Status indicators */
    .status-success { color: #28a745; font-weight: bold; }
    .status-warning { color: #ffc107; font-weight: bold; }
    .status-error { color: #dc3545; font-weight: bold; }
    .status-info { color: #17a2b8; font-weight: bold; }
    
    /* Enhanced charts */
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class DataManager:
    """Enhanced data management with persistence and validation"""
    
    def __init__(self):
        self.db_path = "pms_data.db"
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with comprehensive schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create clients table with comprehensive fields
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT UNIQUE,
                client_name TEXT NOT NULL,
                email TEXT,
                mobile TEXT,
                city TEXT,
                state TEXT,
                country TEXT,
                nationality TEXT,
                occupation TEXT,
                inception_date DATE,
                age_of_client INTEGER,
                client_since_years REAL,
                distributor_name TEXT,
                current_aum REAL,
                initial_corpus REAL,
                additions REAL,
                withdrawals REAL,
                net_corpus REAL,
                annualized_returns REAL,
                benchmark_returns REAL,
                portfolio_type TEXT,
                risk_profile TEXT,
                rm_name TEXT,
                nav_bucket REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_hash TEXT
            )
        """)
        
        # Create performance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT,
                date DATE,
                portfolio_value REAL,
                benchmark_value REAL,
                alpha REAL,
                beta REAL,
                sharpe_ratio REAL,
                max_drawdown REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (client_id)
            )
        """)
        
        # Create data_uploads table for tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                file_hash TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                records_processed INTEGER,
                records_new INTEGER,
                records_updated INTEGER,
                status TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def calculate_file_hash(self, file_content):
        """Calculate hash of file content for duplicate detection"""
        return hashlib.md5(file_content).hexdigest()
    
    def process_uploaded_file(self, uploaded_file):
        """Process uploaded Excel/CSV file with validation and merging"""
        try:
            # Read file content
            file_content = uploaded_file.read()
            file_hash = self.calculate_file_hash(file_content)
            
            # Check if file already processed
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM data_uploads WHERE file_hash = ?", (file_hash,))
            existing_upload = cursor.fetchone()
            
            if existing_upload:
                conn.close()
                return {
                    'status': 'duplicate',
                    'message': f'File already processed on {existing_upload[3]}',
                    'records_processed': existing_upload[4]
                }
            
            # Reset file pointer
            uploaded_file.seek(0)
            
            # Read data based on file type
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Validate and clean data
            df = self.validate_and_clean_data(df)
            
            # Process records
            records_new = 0
            records_updated = 0
            
            for _, row in df.iterrows():
                result = self.upsert_client_record(row)
                if result == 'new':
                    records_new += 1
                elif result == 'updated':
                    records_updated += 1
            
            # Record upload
            cursor.execute("""
                INSERT INTO data_uploads 
                (filename, file_hash, records_processed, records_new, records_updated, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (uploaded_file.name, file_hash, len(df), records_new, records_updated, 'success'))
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'message': f'Successfully processed {len(df)} records',
                'records_processed': len(df),
                'records_new': records_new,
                'records_updated': records_updated
            }
            
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            return {
                'status': 'error',
                'message': f'Error processing file: {str(e)}',
                'records_processed': 0
            }
    
    def validate_and_clean_data(self, df):
        """Validate and clean uploaded data"""
        # Standardize column names
        column_mapping = {
            'CLIENTNAME': 'client_name',
            'CLIENT NAME': 'client_name',
            'CLIENT_NAME': 'client_name',
            'EMAIL': 'email',
            'MOBILE': 'mobile',
            'CITY': 'city',
            'STATE': 'state',
            'COUNTRY': 'country',
            'NATIONALITY': 'nationality',
            'OCCUPATION': 'occupation',
            'CURRENT AUM (in crs.)': 'current_aum',
            'CURRENT_AUM': 'current_aum',
            'AUM (Cr)': 'current_aum',
            'PORTFOLIO TYPE': 'portfolio_type',
            'PORTFOLIO_TYPE': 'portfolio_type',
            'RM NAME': 'rm_name',
            'RM_NAME': 'rm_name',
            'RISK PROFILE': 'risk_profile',
            'RISK_PROFILE': 'risk_profile'
        }
        
        # Rename columns
        df = df.rename(columns=column_mapping)
        
        # Generate client_id if not present
        if 'client_id' not in df.columns:
            df['client_id'] = df.apply(lambda row: f"CLI_{hash(str(row.get('client_name', '')) + str(row.get('email', ''))) % 100000:05d}", axis=1)
        
        # Fill missing values
        df = df.fillna('')
        
        # Convert numeric columns
        numeric_columns = ['current_aum', 'initial_corpus', 'additions', 'withdrawals', 'net_corpus', 
                          'annualized_returns', 'benchmark_returns', 'age_of_client', 'client_since_years', 'nav_bucket']
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    
    def upsert_client_record(self, row):
        """Insert or update client record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if client exists
        cursor.execute("SELECT id FROM clients WHERE client_id = ?", (row.get('client_id'),))
        existing = cursor.fetchone()
        
        # Prepare data
        data = {
            'client_id': row.get('client_id', ''),
            'client_name': row.get('client_name', ''),
            'email': row.get('email', ''),
            'mobile': row.get('mobile', ''),
            'city': row.get('city', ''),
            'state': row.get('state', ''),
            'country': row.get('country', ''),
            'nationality': row.get('nationality', ''),
            'occupation': row.get('occupation', ''),
            'current_aum': row.get('current_aum', 0),
            'portfolio_type': row.get('portfolio_type', 'Equity'),
            'risk_profile': row.get('risk_profile', 'Medium'),
            'rm_name': row.get('rm_name', 'Unassigned'),
            'updated_at': datetime.now().isoformat()
        }
        
        if existing:
            # Update existing record
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            values = list(data.values()) + [row.get('client_id')]
            cursor.execute(f"UPDATE clients SET {set_clause} WHERE client_id = ?", values)
            result = 'updated'
        else:
            # Insert new record
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            cursor.execute(f"INSERT INTO clients ({columns}) VALUES ({placeholders})", list(data.values()))
            result = 'new'
        
        conn.commit()
        conn.close()
        return result
    
    def get_all_clients(self):
        """Retrieve all client data"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM clients ORDER BY updated_at DESC", conn)
        conn.close()
        return df
    
    def clear_all_data(self):
        """Clear all data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients")
        cursor.execute("DELETE FROM performance")
        cursor.execute("DELETE FROM data_uploads")
        conn.commit()
        conn.close()
        return True

def generate_enhanced_sample_data(num_records=100):
    """Generate comprehensive sample data with 100+ records"""
    np.random.seed(42)  # For reproducible data
    
    # Enhanced data generation
    client_names = [
        "Aditya Enterprises", "Bharat Industries", "Chandra Holdings", "Deepak Ventures", "Ekta Corp",
        "Falcon Investments", "Ganesh Trading", "Himalaya Group", "Indus Capital", "Jyoti Enterprises",
        "Kiran Holdings", "Lotus Ventures", "Manoj Industries", "Nanda Corp", "Om Enterprises",
        "Priya Holdings", "Quantum Ventures", "Raj Industries", "Sita Enterprises", "Tata Holdings",
        "Uma Ventures", "Vijay Corp", "Waman Industries", "Xerxes Holdings", "Yash Enterprises",
        "Zara Ventures", "Alpha Holdings", "Beta Corp", "Gamma Industries", "Delta Ventures",
        "Epsilon Holdings", "Zeta Corp", "Eta Industries", "Theta Ventures", "Iota Holdings",
        "Kappa Corp", "Lambda Industries", "Mu Ventures", "Nu Holdings", "Xi Corp",
        "Omicron Industries", "Pi Ventures", "Rho Holdings", "Sigma Corp", "Tau Industries",
        "Upsilon Ventures", "Phi Holdings", "Chi Corp", "Psi Industries", "Omega Ventures"
    ]
    
    cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Pune", "Hyderabad", "Ahmedabad", 
              "Surat", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", 
              "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara", "Ghaziabad", "Ludhiana",
              "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivali", "Vasai-Virar",
              "Varanasi", "Srinagar", "Dhanbad", "Jodhpur", "Amritsar", "Raipur", "Allahabad",
              "Coimbatore", "Jabalpur", "Gwalior", "Vijayawada", "Madurai", "Guwahati", "Chandigarh",
              "Hubli-Dharwad", "Mysore", "Tiruchirappalli", "Bareilly", "Aligarh", "Tiruppur", "Moradabad"]
    
    states = ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "West Bengal", "Gujarat", "Telangana",
              "Rajasthan", "Uttar Pradesh", "Madhya Pradesh", "Bihar", "Punjab", "Haryana", "Kerala",
              "Odisha", "Jharkhand", "Assam", "Chhattisgarh", "Uttarakhand", "Himachal Pradesh"]
    
    occupations = ["Business Owner", "Private Sector", "Government Service", "Professional", "Retired",
                   "Consultant", "Entrepreneur", "Doctor", "Engineer", "Lawyer", "Chartered Accountant",
                   "Investment Banker", "Real Estate", "Manufacturing", "Trading", "IT Professional"]
    
    portfolio_types = ["Equity", "Balanced", "Debt", "Hybrid", "Multi-Asset"]
    risk_profiles = ["Conservative", "Moderate", "Aggressive", "Very Aggressive", "Balanced"]
    rm_names = ["Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sunita Gupta", "Vikram Singh",
                "Meera Joshi", "Arjun Reddy", "Kavita Nair", "Rohit Agarwal", "Sneha Desai",
                "Manish Verma", "Pooja Malhotra", "Sanjay Yadav", "Ritu Bansal", "Deepak Mehta"]
    
    distributors = ["Alpha Wealth", "Beta Capital", "Gamma Advisors", "Delta Finance", "Epsilon Wealth",
                    "Zeta Capital", "Eta Advisors", "Theta Finance", "Iota Wealth", "Kappa Capital"]
    
    # Generate 100+ records
    data = []
    for i in range(num_records):
        inception_date = datetime.now() - timedelta(days=np.random.randint(365, 3650))
        client_since = (datetime.now() - inception_date).days / 365.25
        
        initial_corpus = np.random.uniform(10, 500)
        additions = np.random.uniform(0, initial_corpus * 0.5)
        withdrawals = np.random.uniform(0, initial_corpus * 0.2)
        net_corpus = initial_corpus + additions - withdrawals
        
        # Generate realistic returns
        market_return = np.random.normal(12, 8)  # Market return with volatility
        alpha = np.random.normal(2, 3)  # Alpha generation
        portfolio_return = market_return + alpha
        
        current_aum = net_corpus * (1 + portfolio_return/100) ** client_since
        
        record = {
            'client_id': f"CLI_{i+1:05d}",
            'client_name': f"{np.random.choice(client_names)} {i+1}",
            'email': f"client{i+1}@{np.random.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'company.com'])}",
            'mobile': f"+91{np.random.randint(7000000000, 9999999999)}",
            'city': np.random.choice(cities),
            'state': np.random.choice(states),
            'country': "India",
            'nationality': "Indian",
            'occupation': np.random.choice(occupations),
            'inception_date': inception_date.strftime('%Y-%m-%d'),
            'age_of_client': np.random.randint(25, 75),
            'client_since_years': round(client_since, 2),
            'distributor_name': np.random.choice(distributors),
            'current_aum': round(current_aum, 2),
            'initial_corpus': round(initial_corpus, 2),
            'additions': round(additions, 2),
            'withdrawals': round(withdrawals, 2),
            'net_corpus': round(net_corpus, 2),
            'annualized_returns': round(portfolio_return, 2),
            'benchmark_returns': round(market_return, 2),
            'portfolio_type': np.random.choice(portfolio_types),
            'risk_profile': np.random.choice(risk_profiles),
            'rm_name': np.random.choice(rm_names),
            'nav_bucket': round(current_aum / 10, 1)  # NAV bucket in tens
        }
        data.append(record)
    
    return pd.DataFrame(data)

def calculate_advanced_metrics(df):
    """Calculate advanced financial metrics"""
    if df.empty:
        return {}
    
    total_aum = df['current_aum'].sum()
    total_clients = len(df)
    avg_aum = df['current_aum'].mean()
    
    # Advanced calculations
    weighted_returns = (df['current_aum'] * df['annualized_returns']).sum() / total_aum if total_aum > 0 else 0
    weighted_benchmark = (df['current_aum'] * df['benchmark_returns']).sum() / total_aum if total_aum > 0 else 0
    alpha = weighted_returns - weighted_benchmark
    
    # Risk metrics
    returns_std = df['annualized_returns'].std()
    sharpe_ratio = (weighted_returns - 6) / returns_std if returns_std > 0 else 0  # Assuming 6% risk-free rate
    
    # High water mark calculation (simplified)
    high_water_mark = df['current_aum'].max()
    
    # Additional metrics
    total_corpus = df['net_corpus'].sum()
    total_additions = df['additions'].sum()
    total_withdrawals = df['withdrawals'].sum()
    
    return {
        'total_aum': total_aum,
        'total_clients': total_clients,
        'avg_aum': avg_aum,
        'weighted_returns': weighted_returns,
        'weighted_benchmark': weighted_benchmark,
        'alpha': alpha,
        'sharpe_ratio': sharpe_ratio,
        'high_water_mark': high_water_mark,
        'total_corpus': total_corpus,
        'total_additions': total_additions,
        'total_withdrawals': total_withdrawals,
        'returns_std': returns_std
    }

def main():
    """Enhanced main dashboard function"""
    
    # Initialize data manager
    data_manager = DataManager()
    
    # Header with enhanced styling
    st.markdown('<h1 class="main-header">📊 PMS Intelligence Hub - Enhanced</h1>', unsafe_allow_html=True)
    st.markdown("**Professional Portfolio Management Services Dashboard**")
    st.markdown("---")
    
    # Sidebar with enhanced controls
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.title("🔧 Dashboard Controls")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Data Management Section
        st.subheader("📁 Data Management")
        
        # File upload
        st.markdown('<div class="upload-area">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload Client Data",
            type=['csv', 'xlsx', 'xls'],
            help="Upload Excel or CSV file with client data"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            if st.button("🔄 Process Upload", type="primary"):
                with st.spinner("Processing file..."):
                    result = data_manager.process_uploaded_file(uploaded_file)
                    
                    if result['status'] == 'success':
                        st.success(f"✅ {result['message']}")
                        st.info(f"📊 New records: {result['records_new']}, Updated: {result['records_updated']}")
                    elif result['status'] == 'duplicate':
                        st.warning(f"⚠️ {result['message']}")
                    else:
                        st.error(f"❌ {result['message']}")
                    
                    st.rerun()
        
        # Data management buttons
        st.markdown('<div class="data-management">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎲 Load Sample Data", help="Load 100+ sample records"):
                with st.spinner("Generating sample data..."):
                    sample_df = generate_enhanced_sample_data(100)
                    for _, row in sample_df.iterrows():
                        data_manager.upsert_client_record(row)
                    st.success("✅ Sample data loaded!")
                    st.rerun()
        
        with col2:
            if st.button("🗑️ Clear All Data", help="Remove all existing data"):
                if st.session_state.get('confirm_clear', False):
                    data_manager.clear_all_data()
                    st.success("✅ All data cleared!")
                    st.session_state.confirm_clear = False
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("⚠️ Click again to confirm")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Filters
        st.subheader("🔍 Filters")
        
        # Get current data for filters
        current_data = data_manager.get_all_clients()
        
        if not current_data.empty:
            rm_options = ["All"] + sorted(current_data['rm_name'].dropna().unique().tolist())
            portfolio_options = ["All"] + sorted(current_data['portfolio_type'].dropna().unique().tolist())
            risk_options = ["All"] + sorted(current_data['risk_profile'].dropna().unique().tolist())
            
            selected_rm = st.selectbox("Relationship Manager", rm_options)
            selected_portfolio = st.selectbox("Portfolio Type", portfolio_options)
            selected_risk = st.selectbox("Risk Profile", risk_options)
            
            # AUM range filter
            if current_data['current_aum'].max() > 0:
                aum_range = st.slider(
                    "AUM Range (Cr)",
                    min_value=0.0,
                    max_value=float(current_data['current_aum'].max()),
                    value=(0.0, float(current_data['current_aum'].max())),
                    step=0.1
                )
            else:
                aum_range = (0.0, 0.0)
        else:
            selected_rm = "All"
            selected_portfolio = "All"
            selected_risk = "All"
            aum_range = (0.0, 0.0)
    
    # Main content area
    if current_data.empty:
        st.info("📊 No data available. Please upload data or load sample data from the sidebar.")
        return
    
    # Apply filters
    filtered_data = current_data.copy()
    
    if selected_rm != "All":
        filtered_data = filtered_data[filtered_data['rm_name'] == selected_rm]
    if selected_portfolio != "All":
        filtered_data = filtered_data[filtered_data['portfolio_type'] == selected_portfolio]
    if selected_risk != "All":
        filtered_data = filtered_data[filtered_data['risk_profile'] == selected_risk]
    
    # AUM range filter
    filtered_data = filtered_data[
        (filtered_data['current_aum'] >= aum_range[0]) & 
        (filtered_data['current_aum'] <= aum_range[1])
    ]
    
    # Calculate metrics
    metrics = calculate_advanced_metrics(filtered_data)
    
    # Enhanced Key Metrics Row
    st.subheader("📈 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total AUM",
            value=f"₹{metrics.get('total_aum', 0):.1f} Cr",
            delta=f"+{metrics.get('total_aum', 0)*0.05:.1f} Cr"
        )
    
    with col2:
        st.metric(
            label="Total Clients",
            value=f"{metrics.get('total_clients', 0)}",
            delta="+5"
        )
    
    with col3:
        st.metric(
            label="Average AUM",
            value=f"₹{metrics.get('avg_aum', 0):.1f} Cr",
            delta=f"+{metrics.get('avg_aum', 0)*0.03:.1f} Cr"
        )
    
    with col4:
        st.metric(
            label="Portfolio Alpha",
            value=f"{metrics.get('alpha', 0):.2f}%",
            delta=f"+{metrics.get('alpha', 0)*0.1:.2f}%"
        )
    
    with col5:
        st.metric(
            label="Sharpe Ratio",
            value=f"{metrics.get('sharpe_ratio', 0):.2f}",
            delta=f"+{metrics.get('sharpe_ratio', 0)*0.05:.2f}"
        )
    
    # Second row of metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="High Water Mark",
            value=f"₹{metrics.get('high_water_mark', 0):.1f} Cr",
            delta="New High"
        )
    
    with col2:
        st.metric(
            label="Total Corpus",
            value=f"₹{metrics.get('total_corpus', 0):.1f} Cr",
            delta=f"+{metrics.get('total_additions', 0):.1f} Cr"
        )
    
    with col3:
        st.metric(
            label="Net Additions",
            value=f"₹{metrics.get('total_additions', 0) - metrics.get('total_withdrawals', 0):.1f} Cr",
            delta=f"Withdrawals: ₹{metrics.get('total_withdrawals', 0):.1f} Cr"
        )
    
    with col4:
        st.metric(
            label="Weighted Returns",
            value=f"{metrics.get('weighted_returns', 0):.2f}%",
            delta=f"vs Benchmark: {metrics.get('weighted_benchmark', 0):.2f}%"
        )
    
    with col5:
        st.metric(
            label="Return Volatility",
            value=f"{metrics.get('returns_std', 0):.2f}%",
            delta="Risk Measure"
        )
    
    st.markdown("---")
    
    # Enhanced Charts Section
    st.subheader("📊 Portfolio Analytics")
    
    # First row of charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("AUM Distribution by Portfolio Type")
        if not filtered_data.empty:
            aum_by_type = filtered_data.groupby('portfolio_type')['current_aum'].sum().reset_index()
            fig_pie = px.pie(
                aum_by_type,
                values='current_aum',
                names='portfolio_type',
                title="AUM Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No data available for selected filters")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Returns vs Benchmark Analysis")
        if not filtered_data.empty:
            fig_scatter = px.scatter(
                filtered_data,
                x='benchmark_returns',
                y='annualized_returns',
                size='current_aum',
                color='portfolio_type',
                hover_data=['client_name', 'rm_name'],
                title="Portfolio Returns vs Benchmark",
                labels={'benchmark_returns': 'Benchmark Returns (%)', 'annualized_returns': 'Portfolio Returns (%)'}
            )
            # Add diagonal line for benchmark
            fig_scatter.add_shape(
                type="line",
                x0=filtered_data['benchmark_returns'].min(),
                y0=filtered_data['benchmark_returns'].min(),
                x1=filtered_data['benchmark_returns'].max(),
                y1=filtered_data['benchmark_returns'].max(),
                line=dict(color="red", width=2, dash="dash")
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("No data available for selected filters")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Second row of charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("AUM by Relationship Manager")
        if not filtered_data.empty:
            aum_by_rm = filtered_data.groupby('rm_name').agg({
                'current_aum': 'sum',
                'client_name': 'count'
            }).reset_index()
            aum_by_rm.columns = ['rm_name', 'total_aum', 'client_count']
            
            fig_bar = px.bar(
                aum_by_rm,
                x='rm_name',
                y='total_aum',
                title="AUM by Relationship Manager",
                labels={'total_aum': 'Total AUM (Cr)', 'rm_name': 'Relationship Manager'},
                color='total_aum',
                color_continuous_scale='Blues'
            )
            fig_bar.update_xaxis(tickangle=45)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No data available for selected filters")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Risk-Return Profile")
        if not filtered_data.empty:
            risk_return = filtered_data.groupby('risk_profile').agg({
                'annualized_returns': 'mean',
                'current_aum': 'sum'
            }).reset_index()
            
            fig_bar_risk = px.bar(
                risk_return,
                x='risk_profile',
                y='annualized_returns',
                title="Average Returns by Risk Profile",
                labels={'annualized_returns': 'Average Returns (%)', 'risk_profile': 'Risk Profile'},
                color='annualized_returns',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_bar_risk, use_container_width=True)
        else:
            st.info("No data available for selected filters")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Data Table
    st.subheader("📋 Comprehensive Client Portfolio Details")
    
    if not filtered_data.empty:
        # Prepare display dataframe
        display_df = filtered_data[[
            'client_id', 'client_name', 'rm_name', 'portfolio_type', 'risk_profile',
            'current_aum', 'annualized_returns', 'benchmark_returns', 'city', 'state'
        ]].copy()
        
        # Format numeric columns
        display_df['current_aum'] = display_df['current_aum'].apply(lambda x: f"₹{x:.1f} Cr")
        display_df['annualized_returns'] = display_df['annualized_returns'].apply(lambda x: f"{x:.2f}%")
        display_df['benchmark_returns'] = display_df['benchmark_returns'].apply(lambda x: f"{x:.2f}%")
        
        # Rename columns for display
        display_df.columns = [
            'Client ID', 'Client Name', 'RM Name', 'Portfolio Type', 'Risk Profile',
            'Current AUM', 'Returns (%)', 'Benchmark (%)', 'City', 'State'
        ]
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Download options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"pms_client_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Excel download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                filtered_data.to_excel(writer, sheet_name='Client Data', index=False)
            excel_data = output.getvalue()
            
            st.download_button(
                label="📊 Download as Excel",
                data=excel_data,
                file_name=f"pms_client_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col3:
            st.info(f"📊 Showing {len(filtered_data)} of {len(current_data)} total records")
    
    else:
        st.info("No clients match the selected filters")
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"""
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p><strong>PMS Intelligence Hub - Enhanced Edition</strong></p>
            <p>Developed by Vulnuris | Portfolio Management Services Dashboard</p>
            <p>Data as of {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

