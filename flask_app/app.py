"""
Simple Flask App for PMS Intelligence Hub
Direct integration without complex proxying
Author: Vulnuris Development Team
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import io
import os
import sys

# Add the dashboard directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'dashboard'))

app = Flask(__name__)

# Import dashboard functionality
try:
    from main_dashboard import PMSIntelligenceHub
    from flows_tracker import ClientFlowsTracker
    dashboard_available = True
except ImportError:
    dashboard_available = False

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    if not dashboard_available:
        return render_template('error.html')
    
    try:
        # Initialize dashboard
        hub = PMSIntelligenceHub()
        data = hub.load_data()
        
        # Basic statistics
        total_clients = len(data)
        total_aum = data['current_aum'].sum()
        avg_returns = data['annualised_returns'].mean()
        
        # Create simple charts
        fig_aum = px.histogram(data, x='current_aum', title='AUM Distribution')
        fig_returns = px.scatter(data, x='current_aum', y='annualised_returns', 
                               color='portfolio_type', title='AUM vs Returns')
        
        return render_template('dashboard.html', 
                             total_clients=total_clients,
                             total_aum=f"₹{total_aum:.2f} Cr",
                             avg_returns=f"{avg_returns:.2f}%",
                             chart_aum=fig_aum.to_html(div_id="aum_chart"),
                             chart_returns=fig_returns.to_html(div_id="returns_chart"),
                             clients=data.to_dict('records')[:20])  # Show first 20 clients
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/flows')
def flows():
    """Client flows page"""
    if not dashboard_available:
        return render_template('error.html')
    
    try:
        # Initialize flows tracker
        tracker = ClientFlowsTracker()
        
        # Generate sample flows if none exist
        hub = PMSIntelligenceHub()
        client_data = hub.load_data()
        client_ids = client_data['client_id'].tolist()
        
        flows_data = tracker.generate_sample_flows(client_ids[:10], 50)  # 50 transactions for 10 clients
        
        # Create flows chart
        fig_flows = px.bar(flows_data.groupby('transaction_label')['amount'].sum().reset_index(),
                          x='transaction_label', y='amount', title='Transaction Summary by Type')
        
        return render_template('flows.html',
                             chart_flows=fig_flows.to_html(div_id="flows_chart"),
                             flows=flows_data.to_dict('records')[:20])
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/data')
def data_management():
    """Data management page"""
    return render_template('data.html')

@app.route('/api/export/<format>')
def export_data(format):
    """Export data in CSV or Excel format"""
    try:
        hub = PMSIntelligenceHub()
        data = hub.load_data()
        
        if format == 'csv':
            output = io.StringIO()
            data.to_csv(output, index=False)
            output.seek(0)
            
            return send_file(
                io.BytesIO(output.getvalue().encode()),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'pms_data_{datetime.now().strftime("%Y%m%d")}.csv'
            )
        
        elif format == 'excel':
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                data.to_excel(writer, sheet_name='Client Data', index=False)
            output.seek(0)
            
            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=f'pms_data_{datetime.now().strftime("%Y%m%d")}.xlsx'
            )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'PMS Intelligence Hub', 'dashboard_available': dashboard_available}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

