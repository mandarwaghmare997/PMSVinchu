"""
Flask Wrapper for PMS Intelligence Hub
Provides permanent deployment for the Streamlit dashboard
Author: Vulnuris Development Team
"""

from flask import Flask, render_template, redirect, url_for, request
import subprocess
import threading
import time
import os
import sys
import requests

app = Flask(__name__)

# Global variable to track Streamlit process
streamlit_process = None
streamlit_ready = False

def start_streamlit():
    """Start Streamlit dashboard in background"""
    global streamlit_process, streamlit_ready
    
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
    for i in range(30):  # Wait up to 30 seconds
        try:
            response = requests.get('http://localhost:8502', timeout=2)
            if response.status_code == 200:
                streamlit_ready = True
                break
        except:
            pass
        time.sleep(1)

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Serve the dashboard directly"""
    if not streamlit_ready:
        return render_template('loading.html')
    
    # Proxy the Streamlit app
    try:
        response = requests.get('http://localhost:8502' + request.full_path)
        return response.content, response.status_code, response.headers.items()
    except:
        return render_template('error.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'PMS Intelligence Hub', 'streamlit_ready': streamlit_ready}

@app.route('/<path:path>')
def proxy_streamlit(path):
    """Proxy all other requests to Streamlit"""
    if not streamlit_ready:
        return redirect(url_for('index'))
    
    try:
        url = f'http://localhost:8502/{path}'
        if request.query_string:
            url += f'?{request.query_string.decode()}'
        
        response = requests.get(url, headers=dict(request.headers))
        return response.content, response.status_code, response.headers.items()
    except:
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Start Streamlit in background thread
    streamlit_thread = threading.Thread(target=start_streamlit)
    streamlit_thread.daemon = True
    streamlit_thread.start()
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)

