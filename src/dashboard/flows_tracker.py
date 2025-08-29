"""
Client Flows Tracker Module
Tracks historic cash inflows and outflows for PMS clients
Author: Vulnuris Development Team
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3
from typing import Dict, List, Optional, Tuple

class ClientFlowsTracker:
    """Track and analyze client cash flows"""
    
    def __init__(self, db_path: str = "pms_client_data.db"):
        self.db_path = db_path
        self.transaction_labels = [
            'Investment', 'Withdrawal', 'Fees', 'Dividend', 'Interest',
            'Bonus', 'Rights Issue', 'IPO Subscription', 'Redemption',
            'Switch In', 'Switch Out', 'SIP', 'STP', 'SWP'
        ]
        self.init_flows_database()
    
    def init_flows_database(self):
        """Initialize flows database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create client_flows table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_flows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT NOT NULL,
                transaction_date DATE NOT NULL,
                transaction_label TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (client_id)
            )
        ''')
        
        # Create index for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_flows_client ON client_flows(client_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_flows_date ON client_flows(transaction_date)')
        
        conn.commit()
        conn.close()
    
    def generate_sample_flows(self, client_ids: List[str], num_transactions: int = 200) -> pd.DataFrame:
        """Generate sample transaction flows for clients"""
        flows = []
        
        for _ in range(num_transactions):
            client_id = np.random.choice(client_ids)
            transaction_date = datetime.now() - timedelta(days=np.random.randint(1, 1825))  # 5 years
            
            # Transaction types with realistic probabilities
            transaction_weights = [0.3, 0.15, 0.1, 0.05, 0.05, 0.02, 0.02, 0.03, 0.1, 0.05, 0.05, 0.06, 0.01, 0.01]
            transaction_type = np.random.choice(self.transaction_labels, p=transaction_weights)
            
            # Amount based on transaction type
            if transaction_type in ['Investment', 'SIP', 'IPO Subscription']:
                amount = np.random.uniform(0.1, 10.0)  # Positive inflow
            elif transaction_type in ['Withdrawal', 'Fees', 'Redemption', 'SWP']:
                amount = -np.random.uniform(0.05, 5.0)  # Negative outflow
            elif transaction_type in ['Dividend', 'Interest', 'Bonus']:
                amount = np.random.uniform(0.01, 1.0)  # Small positive
            else:
                amount = np.random.uniform(-2.0, 2.0)  # Mixed
            
            description = f"{transaction_type} transaction for {client_id}"
            
            flow = {
                'client_id': client_id,
                'transaction_date': transaction_date.strftime('%Y-%m-%d'),
                'transaction_label': transaction_type,  # Match database schema
                'amount': round(amount, 2),
                'description': description
            }
            flows.append(flow)
        
        return pd.DataFrame(flows)
    
    def save_flows_to_db(self, flows_df: pd.DataFrame):
        """Save flows data to database"""
        conn = sqlite3.connect(self.db_path)
        
        # Clear existing flows
        conn.execute('DELETE FROM client_flows')
        
        # Insert new flows
        flows_df.to_sql('client_flows', conn, if_exists='append', index=False)
        
        conn.commit()
        conn.close()
    
    def load_flows_from_db(self) -> pd.DataFrame:
        """Load flows data from database"""
        conn = sqlite3.connect(self.db_path)
        
        try:
            flows_df = pd.read_sql_query('''
                SELECT cf.*, c.client_name, c.rm_name
                FROM client_flows cf
                LEFT JOIN clients c ON cf.client_id = c.client_id
                ORDER BY cf.transaction_date DESC
            ''', conn)
        except:
            flows_df = pd.DataFrame()
        
        conn.close()
        return flows_df
    
    def load_flows_data(self) -> pd.DataFrame:
        """Load flows data - alias for load_flows_from_db for compatibility"""
        flows_data = self.load_flows_from_db()
        
        # If no data exists, generate sample data
        if len(flows_data) == 0:
            # Get client IDs from clients table
            conn = sqlite3.connect(self.db_path)
            try:
                client_ids_df = pd.read_sql_query("SELECT client_id FROM clients LIMIT 50", conn)
                if len(client_ids_df) > 0:
                    client_ids = client_ids_df['client_id'].tolist()
                    sample_flows = self.generate_sample_flows(client_ids, 300)
                    self.save_flows_to_db(sample_flows)
                    flows_data = self.load_flows_from_db()
            except Exception as e:
                print(f"Error generating sample flows: {e}")
            finally:
                conn.close()
        
        return flows_data
    
    def get_client_flow_summary(self, client_id: str, years: int = 5) -> Dict:
        """Get flow summary for a specific client"""
        conn = sqlite3.connect(self.db_path)
        
        cutoff_date = (datetime.now() - timedelta(days=years*365)).strftime('%Y-%m-%d')
        
        query = '''
            SELECT 
                transaction_label,
                SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as total_inflow,
                SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as total_outflow,
                COUNT(*) as transaction_count
            FROM client_flows
            WHERE client_id = ? AND transaction_date >= ?
            GROUP BY transaction_label
            ORDER BY total_inflow + total_outflow DESC
        '''
        
        summary_df = pd.read_sql_query(query, conn, params=(client_id, cutoff_date))
        
        # Overall summary
        total_query = '''
            SELECT 
                SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as total_inflow,
                SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as total_outflow,
                COUNT(*) as total_transactions
            FROM client_flows
            WHERE client_id = ? AND transaction_date >= ?
        '''
        
        total_summary = pd.read_sql_query(total_query, conn, params=(client_id, cutoff_date))
        
        conn.close()
        
        return {
            'by_label': summary_df,
            'total': total_summary.iloc[0] if not total_summary.empty else None
        }
    
    def get_monthly_summary(self, client_id: str = None, years: int = 2) -> pd.DataFrame:
        """Get monthly flow summary"""
        conn = sqlite3.connect(self.db_path)
        
        cutoff_date = (datetime.now() - timedelta(days=years*365)).strftime('%Y-%m-%d')
        
        if client_id:
            query = '''
                SELECT 
                    strftime('%Y-%m', transaction_date) as month,
                    SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as inflow,
                    SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as outflow,
                    COUNT(*) as transactions
                FROM client_flows
                WHERE client_id = ? AND transaction_date >= ?
                GROUP BY strftime('%Y-%m', transaction_date)
                ORDER BY month
            '''
            params = (client_id, cutoff_date)
        else:
            query = '''
                SELECT 
                    strftime('%Y-%m', transaction_date) as month,
                    SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as inflow,
                    SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as outflow,
                    COUNT(*) as transactions
                FROM client_flows
                WHERE transaction_date >= ?
                GROUP BY strftime('%Y-%m', transaction_date)
                ORDER BY month
            '''
            params = (cutoff_date,)
        
        monthly_df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        if not monthly_df.empty:
            monthly_df['net_flow'] = monthly_df['inflow'] - monthly_df['outflow']
        
        return monthly_df
    
    def render_flows_dashboard(self):
        """Render the flows tracking dashboard"""
        st.subheader("💰 Client Flows Tracker")
        
        # Load flows data
        flows_df = self.load_flows_from_db()
        
        if flows_df.empty:
            st.info("No flow data available. Generating sample data...")
            
            # Get client IDs from main clients table
            conn = sqlite3.connect(self.db_path)
            try:
                client_ids_df = pd.read_sql_query('SELECT client_id FROM clients LIMIT 20', conn)
                client_ids = client_ids_df['client_id'].tolist()
            except:
                client_ids = [f'BWC{i:04d}' for i in range(1, 21)]
            conn.close()
            
            # Generate and save sample flows
            sample_flows = self.generate_sample_flows(client_ids)
            self.save_flows_to_db(sample_flows)
            flows_df = self.load_flows_from_db()
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Client filter
            client_options = ['All Clients'] + sorted(flows_df['client_id'].unique().tolist())
            selected_client = st.selectbox("Select Client", client_options)
        
        with col2:
            # Transaction label filter
            label_options = ['All Labels'] + sorted(flows_df['transaction_label'].unique().tolist())
            selected_label = st.selectbox("Transaction Type", label_options)
        
        with col3:
            # Time period
            time_periods = ['Last 6 months', 'Last 1 year', 'Last 2 years', 'Last 5 years', 'All time']
            selected_period = st.selectbox("Time Period", time_periods)
        
        # Filter data
        filtered_flows = flows_df.copy()
        
        if selected_client != 'All Clients':
            filtered_flows = filtered_flows[filtered_flows['client_id'] == selected_client]
        
        if selected_label != 'All Labels':
            filtered_flows = filtered_flows[filtered_flows['transaction_label'] == selected_label]
        
        # Time filter
        if selected_period != 'All time':
            days_map = {
                'Last 6 months': 180,
                'Last 1 year': 365,
                'Last 2 years': 730,
                'Last 5 years': 1825
            }
            cutoff_date = (datetime.now() - timedelta(days=days_map[selected_period])).strftime('%Y-%m-%d')
            filtered_flows = filtered_flows[filtered_flows['transaction_date'] >= cutoff_date]
        
        # Summary metrics
        if not filtered_flows.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_inflow = filtered_flows[filtered_flows['amount'] > 0]['amount'].sum()
                st.metric("Total Inflows", f"₹{total_inflow:.2f} Cr")
            
            with col2:
                total_outflow = abs(filtered_flows[filtered_flows['amount'] < 0]['amount'].sum())
                st.metric("Total Outflows", f"₹{total_outflow:.2f} Cr")
            
            with col3:
                net_flow = total_inflow - total_outflow
                st.metric("Net Flow", f"₹{net_flow:.2f} Cr", delta=f"{'Positive' if net_flow > 0 else 'Negative'}")
            
            with col4:
                total_transactions = len(filtered_flows)
                st.metric("Total Transactions", f"{total_transactions:,}")
        
        # Charts
        if not filtered_flows.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Flow by transaction type
                flow_by_type = filtered_flows.groupby('transaction_label')['amount'].sum().reset_index()
                flow_by_type['abs_amount'] = abs(flow_by_type['amount'])
                
                fig = px.bar(
                    flow_by_type.sort_values('abs_amount', ascending=True),
                    x='abs_amount',
                    y='transaction_label',
                    orientation='h',
                    title="Flows by Transaction Type",
                    color='amount',
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Monthly flow trend
                monthly_data = self.get_monthly_summary(
                    selected_client if selected_client != 'All Clients' else None
                )
                
                if not monthly_data.empty:
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        x=monthly_data['month'],
                        y=monthly_data['inflow'],
                        mode='lines+markers',
                        name='Inflows',
                        line=dict(color='green')
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=monthly_data['month'],
                        y=monthly_data['outflow'],
                        mode='lines+markers',
                        name='Outflows',
                        line=dict(color='red')
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=monthly_data['month'],
                        y=monthly_data['net_flow'],
                        mode='lines+markers',
                        name='Net Flow',
                        line=dict(color='blue', dash='dash')
                    ))
                    
                    fig.update_layout(
                        title="Monthly Flow Trends",
                        xaxis_title="Month",
                        yaxis_title="Amount (Cr)",
                        hovermode='x unified'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        
        # Detailed transactions table
        st.subheader("📋 Transaction Details")
        
        if not filtered_flows.empty:
            # Display columns
            display_cols = ['transaction_date', 'client_id', 'client_name', 'transaction_label', 'amount', 'description']
            available_cols = [col for col in display_cols if col in filtered_flows.columns]
            
            st.dataframe(
                filtered_flows[available_cols].sort_values('transaction_date', ascending=False),
                use_container_width=True,
                height=300
            )
            
            # Export option
            if st.button("Export Flow Data"):
                csv = filtered_flows.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"client_flows_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No transactions found for the selected filters.")
    
    def render_client_specific_flows(self, client_id: str):
        """Render flows for a specific client"""
        st.subheader(f"💰 Flows for Client: {client_id}")
        
        # Get client flow summary
        summary = self.get_client_flow_summary(client_id)
        
        if summary['total'] is not None:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Inflows (5Y)", f"₹{summary['total']['total_inflow']:.2f} Cr")
            
            with col2:
                st.metric("Total Outflows (5Y)", f"₹{summary['total']['total_outflow']:.2f} Cr")
            
            with col3:
                net = summary['total']['total_inflow'] - summary['total']['total_outflow']
                st.metric("Net Flow (5Y)", f"₹{net:.2f} Cr")
            
            # Flow breakdown by type
            if not summary['by_label'].empty:
                fig = px.treemap(
                    summary['by_label'],
                    path=['transaction_label'],
                    values='transaction_count',
                    color='total_inflow',
                    title="Transaction Breakdown by Type"
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No flow data available for this client.")

