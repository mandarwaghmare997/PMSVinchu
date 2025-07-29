"""
PMS Intelligence Hub - Simplified Dashboard
Basic Streamlit dashboard for Portfolio Management Services
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="PMS Intelligence Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-metric {
        border-left-color: #28a745;
    }
    .warning-metric {
        border-left-color: #ffc107;
    }
    .danger-metric {
        border-left-color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)

def generate_sample_data():
    """Generate sample data for demonstration"""
    
    # Sample client data
    clients_data = {
        'Client Name': ['ABC Corp', 'XYZ Ltd', 'PQR Industries', 'LMN Holdings', 'DEF Enterprises'],
        'AUM (Cr)': [150.5, 89.2, 234.7, 67.8, 123.4],
        'Portfolio Type': ['Equity', 'Balanced', 'Debt', 'Equity', 'Balanced'],
        'Risk Profile': ['High', 'Medium', 'Low', 'High', 'Medium'],
        'RM Name': ['John Smith', 'Sarah Johnson', 'Mike Wilson', 'Lisa Brown', 'David Lee']
    }
    
    # Sample performance data
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='M')
    performance_data = {
        'Date': dates,
        'Portfolio Value': [100 + i*2 + random.uniform(-5, 5) for i in range(len(dates))],
        'Benchmark': [100 + i*1.5 + random.uniform(-3, 3) for i in range(len(dates))],
        'Alpha': [random.uniform(-2, 4) for _ in range(len(dates))]
    }
    
    return pd.DataFrame(clients_data), pd.DataFrame(performance_data)

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 PMS Intelligence Hub</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Generate sample data
    clients_df, performance_df = generate_sample_data()
    
    # Sidebar
    st.sidebar.title("🔧 Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Filters
    st.sidebar.subheader("Filters")
    selected_rm = st.sidebar.selectbox(
        "Select Relationship Manager",
        ["All"] + list(clients_df['RM Name'].unique())
    )
    
    selected_portfolio_type = st.sidebar.selectbox(
        "Select Portfolio Type",
        ["All"] + list(clients_df['Portfolio Type'].unique())
    )
    
    # Filter data based on selections
    filtered_clients = clients_df.copy()
    if selected_rm != "All":
        filtered_clients = filtered_clients[filtered_clients['RM Name'] == selected_rm]
    if selected_portfolio_type != "All":
        filtered_clients = filtered_clients[filtered_clients['Portfolio Type'] == selected_portfolio_type]
    
    # Key Metrics Row
    st.subheader("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    total_aum = filtered_clients['AUM (Cr)'].sum()
    total_clients = len(filtered_clients)
    avg_aum = filtered_clients['AUM (Cr)'].mean() if total_clients > 0 else 0
    latest_performance = performance_df['Alpha'].iloc[-1] if len(performance_df) > 0 else 0
    
    with col1:
        st.metric(
            label="Total AUM",
            value=f"₹{total_aum:.1f} Cr",
            delta=f"+{total_aum*0.05:.1f} Cr"
        )
    
    with col2:
        st.metric(
            label="Total Clients",
            value=f"{total_clients}",
            delta="+2"
        )
    
    with col3:
        st.metric(
            label="Average AUM",
            value=f"₹{avg_aum:.1f} Cr",
            delta=f"+{avg_aum*0.03:.1f} Cr"
        )
    
    with col4:
        st.metric(
            label="Current Alpha",
            value=f"{latest_performance:.2f}%",
            delta=f"+{latest_performance*0.1:.2f}%"
        )
    
    st.markdown("---")
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 AUM Distribution by Portfolio Type")
        if not filtered_clients.empty:
            aum_by_type = filtered_clients.groupby('Portfolio Type')['AUM (Cr)'].sum()
            fig_pie = px.pie(
                values=aum_by_type.values,
                names=aum_by_type.index,
                title="AUM Distribution"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No data available for selected filters")
    
    with col2:
        st.subheader("📈 Portfolio Performance Trend")
        if not performance_df.empty:
            fig_line = px.line(
                performance_df,
                x='Date',
                y=['Portfolio Value', 'Benchmark'],
                title="Performance vs Benchmark"
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No performance data available")
    
    # Data Tables
    st.markdown("---")
    st.subheader("📋 Client Portfolio Details")
    
    if not filtered_clients.empty:
        # Format the dataframe for better display
        display_df = filtered_clients.copy()
        display_df['AUM (Cr)'] = display_df['AUM (Cr)'].apply(lambda x: f"₹{x:.1f} Cr")
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Download button
        csv = filtered_clients.to_csv(index=False)
        st.download_button(
            label="📥 Download Client Data as CSV",
            data=csv,
            file_name=f"pms_client_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No clients match the selected filters")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p>PMS Intelligence Hub | Portfolio Management Services Dashboard</p>
            <p>Built with Streamlit | Data as of {}</p>
        </div>
        """.format(datetime.now().strftime("%B %d, %Y")),
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

