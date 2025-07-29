# PMS Intelligence Hub

Portfolio Management Services dashboard integrating Salesforce CRM and Wealth Spectrum PMS data for SEBI-regulated entities.

## 🚀 Quick Start

### Windows (Ultimate Setup - Recommended)
```cmd
git clone https://github.com/mandarwaghmare997/PMSVinchu.git
cd PMSVinchu
deployment\windows\ultimate_setup.bat
```
**Features**: Auto-admin elevation, automatic Python installation, simplified dashboard

### Windows (Alternative)
```cmd
deployment\windows\simple_start.bat
```
**Use if**: You prefer manual Python installation

### Linux/macOS
```bash
git clone https://github.com/mandarwaghmare997/PMSVinchu.git
cd PMSVinchu
pip install -r requirements-core.txt
streamlit run src/dashboard/simple_dashboard.py
```

### Docker
```bash
docker-compose up -d
```

## 📊 Features

- **Data Integration**: Salesforce CRM + Wealth Spectrum PMS
- **Interactive Dashboard**: Real-time filtering and analytics
- **Performance Metrics**: CAGR, Alpha, Beta, Sharpe ratio calculations
- **PDF Reports**: Automated report generation
- **Multi-deployment**: Local, Docker, Windows Service options

## 🔧 Configuration

1. Copy `.env.example` to `.env`
2. Configure your API credentials:
```env
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password
SALESFORCE_SECURITY_TOKEN=your_token
WEALTH_SPECTRUM_API_KEY=your_api_key
```

## 📁 Project Structure

```
src/
├── dashboard/           # Streamlit UI
├── data_ingestion/      # API connectors  
├── database/           # Data models
├── api/               # FastAPI backend
└── config/            # Settings

deployment/
└── windows/           # Windows deployment scripts
```

## 🛠️ Development

```bash
# Install dependencies (minimal)
pip install -r requirements-core.txt

# Run simplified dashboard
streamlit run src/dashboard/simple_dashboard.py

# Run full dashboard (if all dependencies available)
streamlit run src/dashboard/main_dashboard.py

# Run API server
uvicorn src.api.main:app --reload

# Run tests
pytest tests/
```

## 📚 Documentation

- [Architecture Overview](ARCHITECTURE.md)
- [Windows Deployment Guide](deployment/windows/README.md)

## 🚀 Windows Users

**Recommended**: Use `deployment\windows\ultimate_setup.bat` for automatic setup with:
- ✅ Administrator privilege elevation
- ✅ Automatic Python installation
- ✅ Simplified dashboard with sample data
- ✅ One-command deployment

## 🌐 Access

**Dashboard URL**: http://localhost:8501  
**API Documentation**: http://localhost:8000/docs (if running API server)

