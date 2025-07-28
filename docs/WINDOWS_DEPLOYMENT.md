# Windows Deployment Guide

## Quick Start
```cmd
git clone https://github.com/mandarwaghmare997/PMSVinchu.git
cd PMSVinchu
deployment\windows\quick_start.bat
```

## Requirements
- Windows 10/11
- Internet connection
- 4GB RAM minimum

## Deployment Options

### 1. One-Command Setup (Recommended)
```cmd
deployment\windows\quick_start.bat
```
Automatically installs Python, dependencies, and starts dashboard.

### 2. Interactive Setup
```cmd
deployment\windows\setup_clean.bat
```
Step-by-step setup with progress details.

### 3. Manual Deployment
```cmd
deployment\windows\deploy_clean.bat local
```

### 4. Docker Deployment
```cmd
deployment\windows\deploy_clean.bat docker
```

### 5. Windows Service (Production)
```cmd
# Install service (requires admin)
deployment\windows\service\install_service.bat

# Manage service
net start PMSIntelligenceHub
net stop PMSIntelligenceHub
```

## Troubleshooting

### Python Issues
- Scripts automatically install Python if missing
- If manual installation needed: download from python.org
- Check "Add Python to PATH" during installation

### Package Installation
- Scripts try multiple installation strategies
- Core packages installed first, optional packages as fallback
- Individual package installation if batch fails

### Common Issues
- **Port in use**: Change port or kill existing process
- **Permission errors**: Run as Administrator
- **Antivirus blocking**: Add project folder to exclusions

## Configuration
Copy `.env.example` to `.env` and configure:
```env
SECRET_KEY=your-secret-key
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password
WEALTH_SPECTRUM_API_KEY=your_api_key
```

## What Gets Installed
- **Core**: Streamlit, Pandas, Plotly, Requests
- **Optional**: FastAPI, SQLAlchemy, additional tools
- **Python**: 3.11.7 (if not present)

Dashboard available at: http://localhost:8501.

