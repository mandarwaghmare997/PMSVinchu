"""
Flask Wrapper for PMS Intelligence Hub
Provides permanent deployment for the Streamlit dashboard
Author: Vulnuris Development Team
"""

from flask import Flask, render_template, redirect, url_for
import subprocess
import threading
import time
import os
import sys

app = Flask(__name__)

# Global variable to track Streamlit process
streamlit_process = None

def start_streamlit():
    """Start Streamlit dashboard in background"""
    global streamlit_process
    
    # Change to dashboard directory
    dashboard_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'dashboard')
    
    # Start Streamlit process
    streamlit_process = subprocess.Popen([
        sys.executable, '-m', 'streamlit', 'run', 'main_dashboard.py',
        '--server.port', '8502',
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--browser.gatherUsageStats', 'false'
    ], cwd=dashboard_dir)
    
    # Wait for Streamlit to start
    time.sleep(5)

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Redirect to Streamlit dashboard"""
    return redirect('http://localhost:8502')

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'PMS Intelligence Hub'}

if __name__ == '__main__':
    # Start Streamlit in background thread
    streamlit_thread = threading.Thread(target=start_streamlit)
    streamlit_thread.daemon = True
    streamlit_thread.start()
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)

