"""
PMS Intelligence Hub - Main Dashboard Application
Interactive Streamlit dashboard for Portfolio Management Services
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta, date
import json
import base64
from typing import Dict, List, Optional, Any
import logging

# Import custom components and utilities
from .components.sidebar import render_sidebar
from .components.metrics_cards import render_metrics_cards
from .components.charts import (
    create_aum_trend_chart, create_performance_chart, 
    create_portfolio_allocation_chart, create_client_distribution_chart
)
from .components.data_tables import render_client_table, render_portfolio_table
from .components.filters import render_filters
from .utils.data_loader import DataLoader
from .utils.calculations import PerformanceCalculator
from .utils.pdf_generator import generate_pdf_report

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="PMS Intelligence Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling and animations
def load_custom_css():
    """Load custom CSS for styling and animations"""
    css = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styles */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .dashboard-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Metrics Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        animation: slideInUp 0.6s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
        counter-reset: number;
        animation: countUp 2s ease-out;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #718096;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-change {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .metric-change.positive {
        color: #38a169;
    }
    
    .metric-change.negative {
        color: #e53e3e;
    }
    
    /* Chart Containers */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-out;
    }
    
    .chart-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Filter Section */
    .filter-section {
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
    }
    
    /* Data Tables */
    .dataframe {
        border: none !important;
    }
    
    .dataframe thead th {
        background-color: #667eea !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background-color: #f8f9fa !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #e3f2fd !important;
        transition: background-color 0.3s ease;
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes countUp {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .dashboard-title {
            font-size: 2rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .chart-container {
            padding: 1rem;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Anime.js integration for enhanced animations
def load_anime_js():
    """Load anime.js library for advanced animations"""
    anime_js = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
    <script>
    // Animate metric cards on load
    anime({
        targets: '.metric-card',
        translateY: [50, 0],
        opacity: [0, 1],
        delay: anime.stagger(100),
        duration: 800,
        easing: 'easeOutExpo'
    });
    
    // Animate chart containers
    anime({
        targets: '.chart-container',
        scale: [0.9, 1],
        opacity: [0, 1],
        delay: anime.stagger(200, {start: 300}),
        duration: 1000,
        easing: 'easeOutElastic(1, .8)'
    });
    
    // Number counter animation for metrics
    function animateNumbers() {
        const metricValues = document.querySelectorAll('.metric-value');
        metricValues.forEach(element => {
            const finalValue = parseFloat(element.textContent.replace(/[^0-9.-]+/g, ''));
            if (!isNaN(finalValue)) {
                anime({
                    targets: element,
                    innerHTML: [0, finalValue],
                    duration: 2000,
                    round: 1,
                    easing: 'easeOutExpo',
                    update: function(anim) {
                        element.innerHTML = Math.round(anim.animatables[0].target.innerHTML).toLocaleString();
                    }
                });
            }
        });
    }
    
    // Trigger animations when page loads
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(animateNumbers, 500);
    });
    </script>
    """
    st.markdown(anime_js, unsafe_allow_html=True)

class DashboardApp:
    """Main Dashboard Application Class"""
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.performance_calc = PerformanceCalculator()
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
        
        if 'current_filters' not in st.session_state:
            st.session_state.current_filters = {}
        
        if 'saved_views' not in st.session_state:
            st.session_state.saved_views = {}
        
        if 'selected_clients' not in st.session_state:
            st.session_state.selected_clients = []
    
    def load_sample_data(self):
        """Load sample data for demonstration"""
        # Generate sample client data
        np.random.seed(42)
        n_clients = 150
        
        clients_data = {
            'client_id': [f'CL_{i:04d}' for i in range(1, n_clients + 1)],
            'client_name': [f'Client {i}' for i in range(1, n_clients + 1)],
            'rm_name': np.random.choice(['John Smith', 'Sarah Johnson', 'Mike Wilson', 'Lisa Brown', 'David Lee'], n_clients),
            'aum': np.random.lognormal(15, 1, n_clients) * 1000,  # AUM in thousands
            'onboarding_date': pd.date_range('2020-01-01', '2024-12-31', periods=n_clients),
            'risk_profile': np.random.choice(['Conservative', 'Moderate', 'Aggressive'], n_clients),
            'investment_category': np.random.choice(['Equity', 'Debt', 'Hybrid', 'Multi-Asset'], n_clients),
            'status': np.random.choice(['Active', 'Inactive'], n_clients, p=[0.9, 0.1])
        }
        
        # Calculate performance metrics
        clients_data['cagr'] = np.random.normal(12, 4, n_clients)  # CAGR in percentage
        clients_data['alpha'] = np.random.normal(2, 1.5, n_clients)  # Alpha
        clients_data['beta'] = np.random.normal(1, 0.3, n_clients)  # Beta
        clients_data['sharpe_ratio'] = np.random.normal(1.2, 0.4, n_clients)  # Sharpe Ratio
        
        return pd.DataFrame(clients_data)
    
    def render_header(self):
        """Render dashboard header"""
        header_html = """
        <div class="dashboard-header">
            <div class="dashboard-title">PMS Intelligence Hub</div>
            <div class="dashboard-subtitle">Portfolio Management Services Dashboard</div>
        </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)
    
    def render_metrics_overview(self, data: pd.DataFrame):
        """Render key metrics overview"""
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate metrics
        total_aum = data['aum'].sum()
        total_clients = len(data[data['status'] == 'Active'])
        avg_cagr = data['cagr'].mean()
        avg_alpha = data['alpha'].mean()
        
        with col1:
            metric_html = f"""
            <div class="metric-card">
                <div class="metric-value">₹{total_aum/10000000:.1f}Cr</div>
                <div class="metric-label">Total AUM</div>
                <div class="metric-change positive">+12.5% vs last month</div>
            </div>
            """
            st.markdown(metric_html, unsafe_allow_html=True)
        
        with col2:
            metric_html = f"""
            <div class="metric-card">
                <div class="metric-value">{total_clients}</div>
                <div class="metric-label">Active Clients</div>
                <div class="metric-change positive">+8 new clients</div>
            </div>
            """
            st.markdown(metric_html, unsafe_allow_html=True)
        
        with col3:
            metric_html = f"""
            <div class="metric-card">
                <div class="metric-value">{avg_cagr:.1f}%</div>
                <div class="metric-label">Average CAGR</div>
                <div class="metric-change positive">+0.8% vs benchmark</div>
            </div>
            """
            st.markdown(metric_html, unsafe_allow_html=True)
        
        with col4:
            metric_html = f"""
            <div class="metric-card">
                <div class="metric-value">{avg_alpha:.2f}</div>
                <div class="metric-label">Average Alpha</div>
                <div class="metric-change positive">Outperforming</div>
            </div>
            """
            st.markdown(metric_html, unsafe_allow_html=True)
    
    def render_charts_section(self, data: pd.DataFrame):
        """Render charts section"""
        # AUM Trend Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">AUM Trend Over Time</div>', unsafe_allow_html=True)
        
        # Generate time series data for AUM trend
        date_range = pd.date_range('2023-01-01', '2024-12-31', freq='M')
        aum_trend = pd.DataFrame({
            'date': date_range,
            'aum': np.cumsum(np.random.normal(5000000, 1000000, len(date_range))) + 100000000
        })
        
        fig_aum = px.line(
            aum_trend, 
            x='date', 
            y='aum',
            title='',
            color_discrete_sequence=['#667eea']
        )
        fig_aum.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif"),
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        fig_aum.update_traces(line=dict(width=3))
        fig_aum.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        fig_aum.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        
        st.plotly_chart(fig_aum, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Portfolio Performance and Client Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Performance Distribution</div>', unsafe_allow_html=True)
            
            fig_perf = px.histogram(
                data, 
                x='cagr', 
                nbins=20,
                title='',
                color_discrete_sequence=['#764ba2']
            )
            fig_perf.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif"),
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig_perf, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Investment Category Distribution</div>', unsafe_allow_html=True)
            
            category_counts = data['investment_category'].value_counts()
            fig_pie = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title='',
                color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c']
            )
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif"),
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    def render_data_tables(self, data: pd.DataFrame):
        """Render data tables section"""
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Client Portfolio Overview</div>', unsafe_allow_html=True)
        
        # Prepare display data
        display_data = data[['client_name', 'rm_name', 'aum', 'cagr', 'alpha', 'investment_category', 'status']].copy()
        display_data['aum'] = display_data['aum'].apply(lambda x: f"₹{x/100000:.1f}L")
        display_data['cagr'] = display_data['cagr'].apply(lambda x: f"{x:.1f}%")
        display_data['alpha'] = display_data['alpha'].apply(lambda x: f"{x:.2f}")
        
        display_data.columns = ['Client Name', 'RM', 'AUM', 'CAGR', 'Alpha', 'Category', 'Status']
        
        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True,
            height=400
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_filters(self, data: pd.DataFrame):
        """Render filter section"""
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.subheader("🔍 Filters & Search")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            rm_filter = st.multiselect(
                "Relationship Manager",
                options=data['rm_name'].unique(),
                default=[]
            )
        
        with col2:
            category_filter = st.multiselect(
                "Investment Category",
                options=data['investment_category'].unique(),
                default=[]
            )
        
        with col3:
            risk_filter = st.multiselect(
                "Risk Profile",
                options=data['risk_profile'].unique(),
                default=[]
            )
        
        with col4:
            aum_range = st.slider(
                "AUM Range (Lakhs)",
                min_value=int(data['aum'].min()/100000),
                max_value=int(data['aum'].max()/100000),
                value=(int(data['aum'].min()/100000), int(data['aum'].max()/100000))
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Apply filters
        filtered_data = data.copy()
        
        if rm_filter:
            filtered_data = filtered_data[filtered_data['rm_name'].isin(rm_filter)]
        
        if category_filter:
            filtered_data = filtered_data[filtered_data['investment_category'].isin(category_filter)]
        
        if risk_filter:
            filtered_data = filtered_data[filtered_data['risk_profile'].isin(risk_filter)]
        
        filtered_data = filtered_data[
            (filtered_data['aum'] >= aum_range[0] * 100000) &
            (filtered_data['aum'] <= aum_range[1] * 100000)
        ]
        
        return filtered_data
    
    def render_export_section(self, data: pd.DataFrame):
        """Render export and save view section"""
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Export to PDF", type="primary"):
                with st.spinner("Generating PDF report..."):
                    # Simulate PDF generation
                    st.success("PDF report generated successfully!")
                    st.download_button(
                        label="Download PDF Report",
                        data=b"Sample PDF content",  # In real implementation, this would be actual PDF bytes
                        file_name=f"pms_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
        
        with col2:
            view_name = st.text_input("Save Current View As:", placeholder="Enter view name")
            if st.button("💾 Save View") and view_name:
                st.session_state.saved_views[view_name] = st.session_state.current_filters
                st.success(f"View '{view_name}' saved successfully!")
        
        with col3:
            if st.session_state.saved_views:
                selected_view = st.selectbox("Load Saved View:", [""] + list(st.session_state.saved_views.keys()))
                if st.button("📂 Load View") and selected_view:
                    st.session_state.current_filters = st.session_state.saved_views[selected_view]
                    st.success(f"View '{selected_view}' loaded!")
                    st.rerun()
    
    def run(self):
        """Main application runner"""
        # Load custom styling and animations
        load_custom_css()
        load_anime_js()
        
        # Render header
        self.render_header()
        
        # Load data
        with st.spinner("Loading portfolio data..."):
            data = self.load_sample_data()
            st.session_state.data_loaded = True
        
        # Render filters and get filtered data
        filtered_data = self.render_filters(data)
        
        # Render metrics overview
        self.render_metrics_overview(filtered_data)
        
        # Render charts
        self.render_charts_section(filtered_data)
        
        # Render data tables
        self.render_data_tables(filtered_data)
        
        # Render export section
        self.render_export_section(filtered_data)
        
        # Footer
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: #718096; font-size: 0.9rem; padding: 2rem;'>
                PMS Intelligence Hub v1.0 | Built with ❤️ for Financial Services
            </div>
            """,
            unsafe_allow_html=True
        )

# Main execution
if __name__ == "__main__":
    app = DashboardApp()
    app.run()

