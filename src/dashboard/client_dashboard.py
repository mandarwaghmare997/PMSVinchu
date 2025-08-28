"""
PMS Intelligence Hub - Client Dashboard
Fixed version with client requirements implementation
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
    page_title="PMS Intelligence Hub - Client Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ClientDashboard:
    """Enhanced client dashboard with all requested features"""
    
    def __init__(self):
        self.db_path = "pms_client_data.db"
        self.flows_tracker = ClientFlowsTracker(self.db_path)
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database with client schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create clients table based on Excel structure
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT NOT NULL,
                client_id TEXT UNIQUE,
                account_type TEXT,
                activation_date DATE,
                date_of_birth DATE,
                age INTEGER,
                client_since_years REAL,
                profession TEXT,
                initial_aum REAL,
                additions_withdrawals REAL,
                withdrawals REAL,
                net_corpus REAL,
                current_aum REAL,
                nav_bucket REAL,
                annualized_returns REAL,
                benchmark_returns REAL,
                mobile TEXT,
                email TEXT,
                rm_name TEXT,
                referral TEXT,
                account_contact_person TEXT,
                family TEXT,
                city TEXT,
                sip_status TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create client flows table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_flows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT,
                transaction_date DATE,
                transaction_type TEXT,
                amount REAL,
                transaction_label TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (client_id)
            )
        ''')
        
        # Create notes table
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
    
    def load_sample_data(self):
        """Load sample data matching client Excel structure exactly"""
        sample_clients = []
        
        # Professions from client requirements
        professions = ['Business Owner', 'Doctor', 'Engineer', 'Lawyer', 'Consultant', 'Banker', 'Entrepreneur', 'CA', 'Architect', 'IT Professional']
        account_types = ['Individual', 'Joint', 'Corporate', 'Trust', 'HUF']
        rm_names = ['Aarav Khilnani', 'Aman Pereira', 'Srinath Panchagnula', 'Priya Sharma', 'Rajesh Kumar', 'Neha Gupta']
        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Pune', 'Hyderabad', 'Kolkata', 'Ahmedabad', 'Surat', 'Jaipur']
        
        for i in range(100):  # Generate 100 records as requested
            activation_date = datetime.now() - timedelta(days=np.random.randint(30, 1825))
            birth_date = datetime.now() - timedelta(days=np.random.randint(25*365, 65*365))
            age = int((datetime.now() - birth_date).days / 365.25)
            
            # Calculate client since years
            client_since_years = (datetime.now() - activation_date).days / 365.25
            
            # Financial calculations matching Excel structure
            initial_aum = np.random.uniform(0.5, 50.0)  # NAV BUCKET (in Crs.)
            additions = np.random.uniform(-5.0, 15.0)   # ADDITIONS
            withdrawals = np.random.uniform(0, 8.0)     # WITHDRAWALS
            net_corpus = initial_aum + additions - withdrawals  # NET CORPUS
            current_aum = max(0.1, net_corpus * np.random.uniform(0.9, 1.3))  # Current AUM with market movement
            
            # Returns calculation
            annualized_returns = np.random.uniform(-5.0, 25.0)  # ANNUALISED RETURNS (%)
            benchmark_returns = np.random.uniform(8.0, 15.0)    # BSE 500 TRI BENCHMARK RETURNS (%)
            
            client = {
                'client_name': f'Client {i+1:03d}',
                'client_id': f'BWC{i+1:04d}',
                'account_type': np.random.choice(account_types),
                'activation_date': activation_date.strftime('%Y-%m-%d'),  # INCEPTION DATE
                'date_of_birth': birth_date.strftime('%Y-%m-%d'),
                'age': age,  # AGE OF CLIENT (Years)
                'client_since_years': round(client_since_years, 1),  # CLIENT SINCE (No: of Years)
                'profession': np.random.choice(professions),
                'initial_aum': round(initial_aum, 2),      # INITIAL CORPUS
                'additions_withdrawals': round(additions, 2),  # ADDITIONS
                'withdrawals': round(withdrawals, 2),      # WITHDRAWALS  
                'net_corpus': round(net_corpus, 2),        # NET CORPUS (in Crs.)
                'current_aum': round(current_aum, 2),      # CURRENT AUM (in crs.)
                'annualized_returns': round(annualized_returns, 2),  # ANNUALISED RETURNS (%)
                'benchmark_returns': round(benchmark_returns, 2),    # BSE 500 TRI BENCHMARK RETURNS (%)
                'mobile': f"+91{np.random.randint(7000000000, 9999999999)}",  # MOBILE (with Country Code)
                'email': f'client{i+1:03d}@email.com',
                'rm_name': np.random.choice(rm_names),     # RM/ Wealth Advisor
                'referral': 'Direct' if np.random.random() > 0.3 else f'Referral {np.random.randint(1, 10)}',  # Referral in any
                'account_contact_person': f'Contact Person {i+1}',  # Account Contact Person
                'family': f'{np.random.randint(1, 6)} members',  # Family
                'city': np.random.choice(cities),          # Place of residence
                'sip_status': np.random.choice(['Yes', 'No', 'SIP']),  # SIP
                'notes': f'Sample notes for client {i+1}',  # Notes
                'nav_bucket': round(current_aum, 2)        # NAV BUCKET (in Crs.) - same as current AUM
            }
            sample_clients.append(client)
        
        return pd.DataFrame(sample_clients)
    
    def save_data_to_db(self, df: pd.DataFrame):
        """Save DataFrame to database"""
        conn = sqlite3.connect(self.db_path)
        
        # Clear existing data
        conn.execute('DELETE FROM clients')
        
        # Insert new data
        df.to_sql('clients', conn, if_exists='append', index=False)
        
        conn.commit()
        conn.close()
    
    def load_data_from_db(self) -> pd.DataFrame:
        """Load data from database"""
        conn = sqlite3.connect(self.db_path)
        
        try:
            df = pd.read_sql_query('SELECT * FROM clients', conn)
            if df.empty:
                # Load sample data if database is empty
                df = self.load_sample_data()
                self.save_data_to_db(df)
        except:
            df = self.load_sample_data()
            self.save_data_to_db(df)
        
        conn.close()
        return df
    
    def add_client_note(self, client_id: str, note_text: str, created_by: str = "User"):
        """Add note for a client"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO client_notes (client_id, note_text, created_by)
            VALUES (?, ?, ?)
        ''', (client_id, note_text, created_by))
        
        conn.commit()
        conn.close()
    
    def get_client_notes(self, client_id: str) -> List[Dict]:
        """Get all notes for a client"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT note_text, created_by, created_at
            FROM client_notes
            WHERE client_id = ?
            ORDER BY created_at DESC
        ''', (client_id,))
        
        notes = []
        for row in cursor.fetchall():
            notes.append({
                'text': row[0],
                'created_by': row[1],
                'created_at': row[2]
            })
        
        conn.close()
        return notes
    
    def process_uploaded_file(self, uploaded_file) -> pd.DataFrame:
        """Process uploaded Excel/CSV file"""
        try:
            if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            
            # Clean and standardize column names
            df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('/', '_')
            
            # Map columns to our schema
            column_mapping = {
                'client_name': 'client_name',
                'client_id': 'client_id', 
                'account_type': 'account_type',
                'activation_date': 'activation_date',
                'date_of_birth': 'date_of_birth',
                'age': 'age',
                'profession': 'profession',
                'initial_aum': 'initial_aum',
                'additions_withdrawls': 'additions_withdrawals',
                'aum': 'current_aum',
                'p_l': 'profit_loss',
                'mobile_(with_country_code)': 'mobile',
                'email': 'email',
                'rm__wealth_advisor': 'rm_name',
                'referral_in_any': 'referral',
                'account_contact_person': 'account_contact_person',
                'family': 'family',
                'sip': 'sip_status',
                'notes': 'notes'
            }
            
            # Rename columns
            for old_col, new_col in column_mapping.items():
                if old_col in df.columns:
                    df = df.rename(columns={old_col: new_col})
            
            # Clean data types
            numeric_columns = ['initial_aum', 'additions_withdrawals', 'current_aum', 'profit_loss', 'age']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            return df
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            return pd.DataFrame()
    
    def render_header(self):
        """Render dashboard header"""
        st.markdown("""
        <div style="background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
            <h1 style="color: white; text-align: center; margin: 0;">
                📊 PMS Intelligence Hub - Client Dashboard
            </h1>
            <p style="color: #e8f4f8; text-align: center; margin: 0.5rem 0 0 0;">
                Bellwether Capital - Portfolio Management Services
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self, data: pd.DataFrame):
        """Render sidebar with filters and controls"""
        st.sidebar.header("🔧 Dashboard Controls")
        
        # Data Management Section
        st.sidebar.subheader("📁 Data Management")
        
        # File Upload
        uploaded_file = st.sidebar.file_uploader(
            "Upload Client Data",
            type=['xlsx', 'xls', 'csv'],
            help="Upload Excel or CSV file with client data"
        )
        
        if uploaded_file is not None:
            if st.sidebar.button("Process Upload"):
                new_data = self.process_uploaded_file(uploaded_file)
                if not new_data.empty:
                    # Merge with existing data
                    existing_data = self.load_data_from_db()
                    
                    # Check for duplicates based on client_id
                    if 'client_id' in new_data.columns:
                        merged_data = pd.concat([existing_data, new_data]).drop_duplicates(
                            subset=['client_id'], keep='last'
                        )
                    else:
                        merged_data = pd.concat([existing_data, new_data])
                    
                    self.save_data_to_db(merged_data)
                    st.sidebar.success(f"Uploaded {len(new_data)} records!")
                    st.experimental_rerun()
        
        # Clear Data Option
        if st.sidebar.button("🗑️ Clear All Data", type="secondary"):
            if st.sidebar.checkbox("Confirm deletion"):
                conn = sqlite3.connect(self.db_path)
                conn.execute('DELETE FROM clients')
                conn.execute('DELETE FROM client_notes')
                conn.execute('DELETE FROM client_flows')
                conn.commit()
                conn.close()
                st.sidebar.success("All data cleared!")
                st.experimental_rerun()
        
        st.sidebar.divider()
        
        # Search and Filters
        st.sidebar.subheader("🔍 Search & Filters")
        
        # Search bar
        search_term = st.sidebar.text_input(
            "Search Clients",
            placeholder="Enter client name, ID, or RM name..."
        )
        
        # RM Filter
        rm_options = ['All'] + sorted(data['rm_name'].dropna().unique().tolist())
        selected_rm = st.sidebar.selectbox("Relationship Manager", rm_options)
        
        # Account Type Filter
        account_types = ['All'] + sorted(data['account_type'].dropna().unique().tolist())
        selected_account_type = st.sidebar.selectbox("Account Type", account_types)
        
        # AUM Range Filter
        if 'current_aum' in data.columns:
            min_aum, max_aum = st.sidebar.slider(
                "AUM Range (Cr)",
                min_value=float(data['current_aum'].min()),
                max_value=float(data['current_aum'].max()),
                value=(float(data['current_aum'].min()), float(data['current_aum'].max())),
                step=0.1
            )
        else:
            min_aum, max_aum = 0, 100
        
        return {
            'search_term': search_term,
            'selected_rm': selected_rm,
            'selected_account_type': selected_account_type,
            'min_aum': min_aum,
            'max_aum': max_aum
        }
    
    def filter_data(self, data: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """Apply filters to data"""
        filtered_data = data.copy()
        
        # Search filter
        if filters['search_term']:
            search_cols = ['client_name', 'client_id', 'rm_name', 'profession']
            search_mask = pd.Series([False] * len(filtered_data))
            
            for col in search_cols:
                if col in filtered_data.columns:
                    search_mask |= filtered_data[col].astype(str).str.contains(
                        filters['search_term'], case=False, na=False
                    )
            
            filtered_data = filtered_data[search_mask]
        
        # RM filter
        if filters['selected_rm'] != 'All':
            filtered_data = filtered_data[filtered_data['rm_name'] == filters['selected_rm']]
        
        # Account type filter
        if filters['selected_account_type'] != 'All':
            filtered_data = filtered_data[filtered_data['account_type'] == filters['selected_account_type']]
        
        # AUM range filter
        if 'current_aum' in filtered_data.columns:
            filtered_data = filtered_data[
                (filtered_data['current_aum'] >= filters['min_aum']) &
                (filtered_data['current_aum'] <= filters['max_aum'])
            ]
        
        return filtered_data
    
    def render_key_metrics(self, data: pd.DataFrame):
        """Render key metrics cards"""
        st.subheader("📊 Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_clients = len(data)
            st.metric(
                label="Total Clients",
                value=f"{total_clients:,}",
                delta=f"+{np.random.randint(1, 5)} this month"
            )
        
        with col2:
            if 'current_aum' in data.columns:
                total_aum = data['current_aum'].sum()
                st.metric(
                    label="Total AUM",
                    value=f"₹{total_aum:.1f} Cr",
                    delta=f"+₹{np.random.uniform(0.5, 2.0):.1f} Cr"
                )
        
        with col3:
            if 'current_aum' in data.columns:
                avg_aum = data['current_aum'].mean()
                st.metric(
                    label="Average AUM",
                    value=f"₹{avg_aum:.1f} Cr",
                    delta=f"+{np.random.uniform(0.1, 0.5):.1f} Cr"
                )
        
        with col4:
            if 'profit_loss' in data.columns:
                avg_returns = data['profit_loss'].mean()
                st.metric(
                    label="Avg Returns",
                    value=f"{avg_returns:.1f}%",
                    delta=f"+{np.random.uniform(0.1, 1.0):.1f}%"
                )
    
    def render_charts(self, data: pd.DataFrame):
        """Render charts with error handling"""
        st.subheader("📈 Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # AUM Distribution by RM
            if 'rm_name' in data.columns and 'current_aum' in data.columns:
                aum_by_rm = data.groupby('rm_name')['current_aum'].sum().reset_index()
                
                fig = px.pie(
                    aum_by_rm,
                    values='current_aum',
                    names='rm_name',
                    title="AUM Distribution by RM"
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Account Type Distribution
            if 'account_type' in data.columns:
                account_dist = data['account_type'].value_counts().reset_index()
                account_dist.columns = ['account_type', 'count']
                
                fig = px.bar(
                    account_dist,
                    x='account_type',
                    y='count',
                    title="Clients by Account Type",
                    color='account_type'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # AUM vs Age Analysis (with proper error handling)
        if 'age' in data.columns and 'current_aum' in data.columns:
            st.subheader("AUM vs Age Analysis")
            
            # Clean data for scatter plot
            clean_data = data.dropna(subset=['age', 'current_aum'])
            clean_data = clean_data[clean_data['current_aum'] > 0]  # Remove zero/negative AUM
            
            if not clean_data.empty:
                fig = px.scatter(
                    clean_data,
                    x='age',
                    y='current_aum',
                    color='account_type' if 'account_type' in clean_data.columns else None,
                    size='current_aum',
                    hover_data=['client_name', 'rm_name'] if 'client_name' in clean_data.columns else None,
                    title="AUM vs Client Age",
                    labels={
                        'age': 'Client Age (Years)',
                        'current_aum': 'Current AUM (Cr)'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def render_client_details(self, data: pd.DataFrame):
        """Render detailed client table with notes functionality"""
        st.subheader("👥 Client Details")
        
        # Display data table
        if not data.empty:
            # Select columns to display matching Excel structure
            display_columns = [
                'client_name', 'client_id', 'account_type', 'activation_date', 'age', 
                'client_since_years', 'profession', 'nav_bucket', 'initial_aum', 
                'additions_withdrawals', 'withdrawals', 'net_corpus', 'current_aum',
                'annualized_returns', 'benchmark_returns', 'mobile', 'email', 'rm_name',
                'referral', 'family', 'city', 'sip_status'
            ]
            
            # Filter columns that exist in data
            available_columns = [col for col in display_columns if col in data.columns]
            display_data = data[available_columns]
            
            st.dataframe(
                display_data,
                use_container_width=True,
                height=400
            )
            
            # Client Notes Section
            st.subheader("📝 Client Notes")
            
            # Select client for notes
            client_options = data['client_id'].tolist() if 'client_id' in data.columns else []
            
            if client_options:
                selected_client = st.selectbox(
                    "Select Client for Notes",
                    client_options,
                    format_func=lambda x: f"{x} - {data[data['client_id']==x]['client_name'].iloc[0] if 'client_name' in data.columns else x}"
                )
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Add new note
                    new_note = st.text_area("Add Note", placeholder="Enter note for this client...")
                    
                    if st.button("Save Note") and new_note.strip():
                        self.add_client_note(selected_client, new_note.strip())
                        st.success("Note saved successfully!")
                        st.experimental_rerun()
                
                with col2:
                    # Display existing notes
                    st.write("**Existing Notes:**")
                    notes = self.get_client_notes(selected_client)
                    
                    if notes:
                        for note in notes:
                            st.write(f"**{note['created_by']}** ({note['created_at'][:16]})")
                            st.write(note['text'])
                            st.write("---")
                    else:
                        st.write("No notes found for this client.")
        
        else:
            st.info("No data available. Please upload client data or load sample data.")
    
    def render_export_options(self, data: pd.DataFrame):
        """Render data export options"""
        st.subheader("📤 Export Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Export to CSV"):
                csv = data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"pms_clients_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("Export to Excel"):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    data.to_excel(writer, sheet_name='Clients', index=False)
                
                st.download_button(
                    label="Download Excel",
                    data=output.getvalue(),
                    file_name=f"pms_clients_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col3:
            if st.button("Export Notes"):
                # Export all notes
                conn = sqlite3.connect(self.db_path)
                notes_df = pd.read_sql_query('''
                    SELECT cn.client_id, c.client_name, cn.note_text, cn.created_by, cn.created_at
                    FROM client_notes cn
                    LEFT JOIN clients c ON cn.client_id = c.client_id
                    ORDER BY cn.created_at DESC
                ''', conn)
                conn.close()
                
                if not notes_df.empty:
                    csv = notes_df.to_csv(index=False)
                    st.download_button(
                        label="Download Notes CSV",
                        data=csv,
                        file_name=f"client_notes_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No notes to export")
    
    def run(self):
        """Main dashboard runner"""
        self.render_header()
        
        # Create tabs for different sections
        tab1, tab2, tab3 = st.tabs(["📊 Client Overview", "💰 Client Flows", "📋 Data Management"])
        
        with tab1:
            # Load data
            data = self.load_data_from_db()
            
            # Render sidebar and get filters
            filters = self.render_sidebar(data)
            
            # Apply filters
            filtered_data = self.filter_data(data, filters)
            
            # Main content
            if not filtered_data.empty:
                self.render_key_metrics(filtered_data)
                st.divider()
                self.render_charts(filtered_data)
                st.divider()
                self.render_client_details(filtered_data)
            else:
                st.warning("No data matches the current filters.")
                
                # Show unfiltered data summary
                if not data.empty:
                    st.info(f"Total clients in database: {len(data)}")
        
        with tab2:
            # Client flows tracking
            self.flows_tracker.render_flows_dashboard()
        
        with tab3:
            # Data management and export options
            data = self.load_data_from_db()
            self.render_export_options(data)

# Run the dashboard
if __name__ == "__main__":
    dashboard = ClientDashboard()
    dashboard.run()

