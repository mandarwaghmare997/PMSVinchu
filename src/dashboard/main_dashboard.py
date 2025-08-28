"""
PMS Intelligence Hub - Main Dashboard
Optimized single dashboard combining all features with zero redundancy
Author: Vulnuris Development Team
"""

from typing import Dict, List, Optional
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import json
import io
import base64
from flows_tracker import ClientFlowsTracker

# Page configuration
st.set_page_config(
    page_title="PMS Intelligence Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class PMSIntelligenceHub:
    """
    Unified PMS Intelligence Hub Dashboard
    Combines all features in a single optimized interface
    """
    
    def __init__(self):
        self.db_path = "pms_client_data.db"
        self.flows_tracker = ClientFlowsTracker(self.db_path)
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database with optimized schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Optimized clients table with proper indexing
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                client_id TEXT PRIMARY KEY,
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create optimized indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_rm ON clients(rm_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_type ON clients(portfolio_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_aum ON clients(current_aum)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clients_risk ON clients(risk_profile)')
        
        # Notes table for client notes functionality
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT,
                note_text TEXT,
                created_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (client_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def load_sample_data(self) -> pd.DataFrame:
        """Generate comprehensive sample data"""
        np.random.seed(42)
        
        # Indian cities and states for realistic data
        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Surat', 'Jaipur']
        rms = ['Rajesh Kumar', 'Priya Sharma', 'Amit Patel', 'Sneha Gupta', 'Vikram Singh']
        portfolio_types = ['Equity', 'Debt', 'Hybrid', 'Multi-Asset']
        risk_profiles = ['Conservative', 'Moderate', 'Aggressive']
        
        data = []
        for i in range(150):
            client_id = f"CL{str(i+1).zfill(4)}"
            inception_date = datetime.now() - timedelta(days=np.random.randint(365, 2555))
            age = np.random.randint(25, 75)
            client_since = (datetime.now() - inception_date).days / 365.25
            
            initial_corpus = np.random.uniform(10, 500)  # in Crores
            additions = np.random.uniform(0, initial_corpus * 0.5)
            withdrawals = np.random.uniform(0, initial_corpus * 0.3)
            net_corpus = initial_corpus + additions - withdrawals
            
            # Realistic returns based on portfolio type
            portfolio_type = np.random.choice(portfolio_types)
            if portfolio_type == 'Equity':
                base_return = np.random.uniform(8, 18)
            elif portfolio_type == 'Debt':
                base_return = np.random.uniform(6, 12)
            else:
                base_return = np.random.uniform(7, 15)
                
            annualised_returns = base_return + np.random.normal(0, 2)
            bse_benchmark = np.random.uniform(10, 14)
            current_aum = net_corpus * (1 + annualised_returns/100) ** client_since
            
            data.append({
                'client_id': client_id,
                'client_name': f"Client {i+1}",
                'nav_bucket': round(current_aum, 2),
                'inception_date': inception_date.strftime('%Y-%m-%d'),
                'age_of_client': age,
                'client_since': round(client_since, 1),
                'mobile': f"{np.random.randint(7000000000, 9999999999, dtype=np.int64)}",
                'email': f"client{i+1}@example.com",
                'distributor_name': f"Distributor {np.random.randint(1, 20)}",
                'current_aum': round(current_aum, 2),
                'initial_corpus': round(initial_corpus, 2),
                'additions': round(additions, 2),
                'withdrawals': round(withdrawals, 2),
                'net_corpus': round(net_corpus, 2),
                'annualised_returns': round(annualised_returns, 2),
                'bse_500_benchmark_returns': round(bse_benchmark, 2),
                'rm_name': np.random.choice(rms),
                'portfolio_type': portfolio_type,
                'risk_profile': np.random.choice(risk_profiles)
            })
            
        return pd.DataFrame(data)
    
    @st.cache_data(ttl=300)
    def load_data(_self) -> pd.DataFrame:
        """Load data with caching for performance"""
        conn = sqlite3.connect(_self.db_path)
        
        try:
            data = pd.read_sql_query("SELECT * FROM clients", conn)
            if data.empty:
                # Generate and insert sample data
                sample_data = _self.load_sample_data()
                sample_data.to_sql('clients', conn, if_exists='replace', index=False)
                data = sample_data
        except Exception:
            # If table doesn't exist, create sample data
            data = _self.load_sample_data()
            data.to_sql('clients', conn, if_exists='replace', index=False)
        finally:
            conn.close()
            
        return data
    
    def render_custom_css(self):
        """Render optimized CSS styling"""
        st.markdown("""
        <style>
            /* Main header styling */
            .main-header {
                font-size: 2.5rem;
                font-weight: bold;
                background: linear-gradient(90deg, #1e3a8a, #059669);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                margin-bottom: 2rem;
                padding: 1rem 0;
            }
            
            /* Enhanced metric cards */
            .metric-card {
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                padding: 1.5rem;
                border-radius: 12px;
                border-left: 4px solid #1e3a8a;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s ease;
            }
            
            .metric-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
            }
            
            .metric-value {
                font-size: 2.5rem;
                font-weight: bold;
                color: #1e3a8a;
                margin: 0;
            }
            
            .metric-label {
                font-size: 0.9rem;
                color: #64748b;
                margin-top: 0.5rem;
            }
            
            /* Success/Warning/Danger variants */
            .success-metric { border-left-color: #059669; }
            .success-metric .metric-value { color: #059669; }
            
            .warning-metric { border-left-color: #f59e0b; }
            .warning-metric .metric-value { color: #f59e0b; }
            
            .danger-metric { border-left-color: #dc2626; }
            .danger-metric .metric-value { color: #dc2626; }
            
            /* Sidebar styling */
            .css-1d391kg { padding-top: 1rem; }
            
            /* Hide Streamlit elements */
            #MainMenu { visibility: hidden; }
            footer { visibility: hidden; }
            header { visibility: hidden; }
            
            /* Responsive design */
            @media (max-width: 768px) {
                .main-header { font-size: 2rem; }
                .metric-value { font-size: 2rem; }
                .metric-card { padding: 1rem; }
            }
        </style>
        """, unsafe_allow_html=True)
    
    def render_sidebar_filters(self, data: pd.DataFrame) -> Dict:
        """Render sidebar filters and return filter values"""
        st.sidebar.header("🔍 Filters")
        
        # RM filter
        rm_options = ['All'] + sorted(data['rm_name'].unique().tolist())
        selected_rm = st.sidebar.selectbox("Relationship Manager", rm_options)
        
        # Portfolio type filter
        portfolio_options = ['All'] + sorted(data['portfolio_type'].unique().tolist())
        selected_portfolio = st.sidebar.selectbox("Portfolio Type", portfolio_options)
        
        # Risk profile filter
        risk_options = ['All'] + sorted(data['risk_profile'].unique().tolist())
        selected_risk = st.sidebar.selectbox("Risk Profile", risk_options)
        
        # AUM range filter
        min_aum, max_aum = float(data['current_aum'].min()), float(data['current_aum'].max())
        aum_range = st.sidebar.slider(
            "AUM Range (₹ Cr)", 
            min_value=min_aum, 
            max_value=max_aum, 
            value=(min_aum, max_aum),
            step=1.0
        )
        
        return {
            'rm': selected_rm,
            'portfolio_type': selected_portfolio,
            'risk_profile': selected_risk,
            'aum_range': aum_range
        }
    
    def apply_filters(self, data: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """Apply filters to data"""
        filtered_data = data.copy()
        
        if filters['rm'] != 'All':
            filtered_data = filtered_data[filtered_data['rm_name'] == filters['rm']]
            
        if filters['portfolio_type'] != 'All':
            filtered_data = filtered_data[filtered_data['portfolio_type'] == filters['portfolio_type']]
            
        if filters['risk_profile'] != 'All':
            filtered_data = filtered_data[filtered_data['risk_profile'] == filters['risk_profile']]
            
        # AUM range filter
        filtered_data = filtered_data[
            (filtered_data['current_aum'] >= filters['aum_range'][0]) &
            (filtered_data['current_aum'] <= filters['aum_range'][1])
        ]
        
        return filtered_data
    
    def render_key_metrics(self, data: pd.DataFrame):
        """Render key metrics cards"""
        col1, col2, col3, col4 = st.columns(4)
        
        total_aum = data['current_aum'].sum()
        total_clients = len(data)
        avg_aum = data['current_aum'].mean()
        avg_returns = data['annualised_returns'].mean()
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">₹{total_aum:.1f} Cr</div>
                <div class="metric-label">Total AUM</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card success-metric">
                <div class="metric-value">{total_clients}</div>
                <div class="metric-label">Total Clients</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-card warning-metric">
                <div class="metric-value">₹{avg_aum:.1f} Cr</div>
                <div class="metric-label">Average AUM</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            alpha = avg_returns - data['bse_500_benchmark_returns'].mean()
            st.markdown(f"""
            <div class="metric-card {'success-metric' if alpha > 0 else 'danger-metric'}">
                <div class="metric-value">{alpha:.2f}%</div>
                <div class="metric-label">Alpha vs BSE 500</div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_charts(self, data: pd.DataFrame):
        """Render interactive charts"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 AUM Distribution by Portfolio Type")
            aum_by_type = data.groupby('portfolio_type')['current_aum'].sum().reset_index()
            fig_pie = px.pie(
                aum_by_type, 
                values='current_aum', 
                names='portfolio_type',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col2:
            st.subheader("📈 Returns vs AUM Analysis")
            fig_scatter = px.scatter(
                data, 
                x='current_aum', 
                y='annualised_returns',
                color='risk_profile',
                size='client_since',
                hover_data=['client_name', 'rm_name'],
                title="Portfolio Performance Analysis"
            )
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Performance trend chart
        st.subheader("📊 RM Performance Comparison")
        rm_performance = data.groupby('rm_name').agg({
            'current_aum': 'sum',
            'annualised_returns': 'mean',
            'client_id': 'count'
        }).reset_index()
        rm_performance.columns = ['RM Name', 'Total AUM', 'Avg Returns', 'Client Count']
        
        fig_bar = px.bar(
            rm_performance, 
            x='RM Name', 
            y='Total AUM',
            color='Avg Returns',
            title="RM Performance - AUM vs Returns"
        )
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    def render_client_details(self, data: pd.DataFrame):
        """Render detailed client information table"""
        st.subheader("👥 Client Details")
        
        # Search functionality
        search_term = st.text_input("🔍 Search clients (name, ID, email, RM)")
        if search_term:
            mask = (
                data['client_name'].str.contains(search_term, case=False, na=False) |
                data['client_id'].str.contains(search_term, case=False, na=False) |
                data['email'].str.contains(search_term, case=False, na=False) |
                data['rm_name'].str.contains(search_term, case=False, na=False)
            )
            data = data[mask]
        
        # Display table with formatting
        display_data = data[[
            'client_id', 'client_name', 'current_aum', 'annualised_returns', 
            'bse_500_benchmark_returns', 'rm_name', 'portfolio_type', 'risk_profile'
        ]].copy()
        
        # Format columns
        display_data['current_aum'] = display_data['current_aum'].apply(lambda x: f"₹{x:.2f} Cr")
        display_data['annualised_returns'] = display_data['annualised_returns'].apply(lambda x: f"{x:.2f}%")
        display_data['bse_500_benchmark_returns'] = display_data['bse_500_benchmark_returns'].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(
            display_data,
            use_container_width=True,
            height=400
        )
    
    def render_data_management(self, data: pd.DataFrame):
        """Render data management options"""
        st.subheader("📁 Data Management")
        
        # Template download section
        st.markdown("### 📋 Data Template")
        col_template1, col_template2 = st.columns(2)
        
        with col_template1:
            # Create template data
            template_data = {
                'client_id': ['CL0001', 'CL0002', 'CL0003'],
                'client_name': ['Sample Client 1', 'Sample Client 2', 'Sample Client 3'],
                'nav_bucket': [25.50, 50.75, 15.25],
                'inception_date': ['2022-01-15', '2021-06-10', '2023-03-20'],
                'age_of_client': [45, 38, 52],
                'client_since': [2.5, 3.2, 1.4],
                'mobile': ['9876543210', '9876543211', '9876543212'],
                'email': ['client1@example.com', 'client2@example.com', 'client3@example.com'],
                'distributor_name': ['Distributor ABC', 'Distributor XYZ', 'Distributor PQR'],
                'current_aum': [25.50, 50.75, 15.25],
                'initial_corpus': [20.00, 40.00, 15.00],
                'additions': [5.00, 12.00, 2.00],
                'withdrawals': [0.50, 1.25, 1.75],
                'net_corpus': [24.50, 50.75, 15.25],
                'annualised_returns': [12.50, 15.20, 8.50],
                'bse_500_benchmark_returns': [11.20, 11.20, 11.20],
                'rm_name': ['Rajesh Kumar', 'Priya Sharma', 'Amit Patel'],
                'portfolio_type': ['Equity', 'Hybrid', 'Debt'],
                'risk_profile': ['Moderate', 'Aggressive', 'Conservative']
            }
            template_df = pd.DataFrame(template_data)
            
            # CSV template download
            csv_template = template_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV Template",
                data=csv_template,
                file_name="pms_data_template.csv",
                mime="text/csv",
                help="Download CSV template with sample data format"
            )
        
        with col_template2:
            # Excel template download
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                template_df.to_excel(writer, sheet_name='Client Data', index=False)
            
            st.download_button(
                label="📥 Download Excel Template",
                data=buffer.getvalue(),
                file_name="pms_data_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download Excel template with sample data format"
            )
        
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📤 Upload Data")
            # File upload
            uploaded_file = st.file_uploader(
                "Upload Excel/CSV file", 
                type=['xlsx', 'xls', 'csv'],
                help="Upload client data in Excel or CSV format using the template above"
            )
            
            if uploaded_file is not None:
                if st.button("Process Upload"):
                    try:
                        # Read uploaded file
                        if uploaded_file.name.endswith('.csv'):
                            new_data = pd.read_csv(uploaded_file)
                        else:
                            new_data = pd.read_excel(uploaded_file)
                        
                        # Basic validation and cleaning
                        required_columns = ['client_id', 'client_name', 'current_aum']
                        if all(col in new_data.columns for col in required_columns):
                            # Insert into database
                            conn = sqlite3.connect(self.db_path)
                            new_data.to_sql('clients', conn, if_exists='append', index=False)
                            conn.close()
                            
                            st.success(f"Successfully uploaded {len(new_data)} records!")
                            st.rerun()
                        else:
                            st.error(f"Missing required columns: {required_columns}")
                    except Exception as e:
                        st.error(f"Error processing file: {str(e)}")
        
        with col2:
            st.markdown("### 📥 Export Data")
            # Export options
            if st.button("📥 Export to CSV"):
                csv = data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"pms_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            if st.button("📥 Export to Excel"):
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    data.to_excel(writer, sheet_name='Client Data', index=False)
                
                st.download_button(
                    label="Download Excel",
                    data=buffer.getvalue(),
                    file_name=f"pms_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col3:
            st.markdown("### 🗑️ Clear Data")
            # Clear data option
            if st.button("🗑️ Clear All Data", type="secondary"):
                if st.checkbox("I confirm I want to delete all data"):
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM clients")
                    cursor.execute("DELETE FROM client_notes")
                    cursor.execute("DELETE FROM client_flows")
                    conn.commit()
                    conn.close()
                    st.success("All data cleared successfully!")
                    st.rerun()
    
    def run(self):
        """Main dashboard execution"""
        # Apply custom CSS
        self.render_custom_css()
        
        # Main header
        st.markdown('<h1 class="main-header">PMS Intelligence Hub</h1>', unsafe_allow_html=True)
        st.markdown("**Powered by Vulnuris** | Advanced Portfolio Management Analytics")
        
        # Load data
        data = self.load_data()
        
        # Sidebar filters
        filters = self.render_sidebar_filters(data)
        filtered_data = self.apply_filters(data, filters)
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💰 Client Flows", "📁 Data Management"])
        
        with tab1:
            if not filtered_data.empty:
                # Key metrics
                self.render_key_metrics(filtered_data)
                st.divider()
                
                # Charts
                self.render_charts(filtered_data)
                st.divider()
                
                # Client details
                self.render_client_details(filtered_data)
            else:
                st.warning("No data matches the current filters.")
                if not data.empty:
                    st.info(f"Total clients in database: {len(data)}")
        
        with tab2:
            # Client flows tracking
            self.flows_tracker.render_flows_dashboard()
        
        with tab3:
            # Data management
            self.render_data_management(data)

# Run the dashboard
if __name__ == "__main__":
    dashboard = PMSIntelligenceHub()
    dashboard.run()

