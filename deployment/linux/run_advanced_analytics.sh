#!/bin/bash

echo "========================================"
echo "PMS Intelligence Hub - Advanced Analytics"
echo "Linux Deployment Script"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade requirements
echo "Installing requirements..."
pip install --upgrade pip
pip install streamlit pandas numpy plotly

# Check if database exists, if not create sample data
if [ ! -f "src/dashboard/pms_client_data.db" ]; then
    echo "Creating sample database..."
    cd src/dashboard
    python3 -c "from advanced_analytics_dashboard import AdvancedAnalyticsDashboard; dashboard = AdvancedAnalyticsDashboard(); data = dashboard.load_data(); print(f'Sample data created: {len(data)} records')"
    cd ../..
fi

# Start the advanced analytics dashboard
echo "========================================"
echo "Starting PMS Intelligence Hub - Advanced Analytics"
echo "========================================"
echo ""
echo "Dashboard will be available at:"
echo "http://localhost:8504"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo "========================================"

cd src/dashboard
streamlit run advanced_analytics_dashboard.py --server.port 8504

