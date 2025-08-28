"""
Ultra-Simple Flask App for PMS Intelligence Hub
No complex dependencies - just working dashboard
Author: Vulnuris Development Team
"""

from flask import Flask, render_template, jsonify
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Simple dashboard with basic data"""
    try:
        # Simple client data without pandas
        clients = [
            {"client_id": "CL001", "client_name": "Rajesh Sharma", "current_aum": 25.50, "annualised_returns": 12.5, "portfolio_type": "Equity", "rm_name": "Priya Patel"},
            {"client_id": "CL002", "client_name": "Anita Gupta", "current_aum": 45.75, "annualised_returns": 15.2, "portfolio_type": "Hybrid", "rm_name": "Amit Kumar"},
            {"client_id": "CL003", "client_name": "Vikram Singh", "current_aum": 32.25, "annualised_returns": 11.8, "portfolio_type": "Debt", "rm_name": "Rajesh Kumar"},
            {"client_id": "CL004", "client_name": "Meera Joshi", "current_aum": 67.80, "annualised_returns": 18.3, "portfolio_type": "Equity", "rm_name": "Priya Patel"},
            {"client_id": "CL005", "client_name": "Suresh Reddy", "current_aum": 28.90, "annualised_returns": 9.7, "portfolio_type": "Debt", "rm_name": "Amit Kumar"},
            {"client_id": "CL006", "client_name": "Kavita Nair", "current_aum": 55.40, "annualised_returns": 16.1, "portfolio_type": "Hybrid", "rm_name": "Rajesh Kumar"},
            {"client_id": "CL007", "client_name": "Arjun Mehta", "current_aum": 41.20, "annualised_returns": 13.9, "portfolio_type": "Equity", "rm_name": "Priya Patel"},
            {"client_id": "CL008", "client_name": "Deepika Iyer", "current_aum": 38.65, "annualised_returns": 14.7, "portfolio_type": "Hybrid", "rm_name": "Amit Kumar"},
            {"client_id": "CL009", "client_name": "Rohit Agarwal", "current_aum": 22.15, "annualised_returns": 10.4, "portfolio_type": "Debt", "rm_name": "Rajesh Kumar"},
            {"client_id": "CL010", "client_name": "Sunita Kapoor", "current_aum": 73.25, "annualised_returns": 19.2, "portfolio_type": "Equity", "rm_name": "Priya Patel"}
        ]
        
        # Calculate simple metrics
        total_clients = len(clients)
        total_aum = sum(client['current_aum'] for client in clients)
        avg_returns = sum(client['annualised_returns'] for client in clients) / len(clients)
        
        return render_template('simple_dashboard.html', 
                             total_clients=total_clients,
                             total_aum=f"₹{total_aum:.2f} Cr",
                             avg_returns=f"{avg_returns:.2f}%",
                             clients=clients)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/flows')
def flows():
    """Simple flows page"""
    flows = [
        {"client_id": "CL001", "date": "2024-08-15", "type": "Investment", "amount": 5.0, "description": "Monthly SIP"},
        {"client_id": "CL002", "date": "2024-08-14", "type": "Withdrawal", "amount": -2.5, "description": "Partial redemption"},
        {"client_id": "CL003", "date": "2024-08-13", "type": "Dividend", "amount": 0.8, "description": "Quarterly dividend"},
        {"client_id": "CL004", "date": "2024-08-12", "type": "Investment", "amount": 10.0, "description": "Lump sum investment"},
        {"client_id": "CL005", "date": "2024-08-11", "type": "Fees", "amount": -0.3, "description": "Management fees"},
    ]
    
    return render_template('simple_flows.html', flows=flows)

@app.route('/data')
def data_management():
    """Simple data management page"""
    return render_template('simple_data.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'PMS Intelligence Hub - Simple Version'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

