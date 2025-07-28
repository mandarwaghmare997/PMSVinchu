# PMS Intelligence Hub

Portfolio Management Services dashboard integrating Salesforce CRM and Wealth Spectrum PMS data for SEBI-regulated entities.

## 🚀 Quick Start

### Windows (One Command)
```cmd
git clone https://github.com/mandarwaghmare997/PMSVinchu.git
cd PMSVinchu
deployment\windows\quick_start.bat
```

### Linux/macOS
```bash
git clone https://github.com/mandarwaghmare997/PMSVinchu.git
cd PMSVinchu
pip install -r requirements.txt
streamlit run src/dashboard/main_dashboard.py
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
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run src/dashboard/main_dashboard.py

# Run API server
uvicorn src.api.main:app --reload

# Run tests
pytest tests/
```

## 📚 Documentation

- [Architecture Overview](ARCHITECTURE.md)
- [Windows Deployment](docs/WINDOWS_DEPLOYMENT.md)

## 🔒 Security & Compliance

- SEBI regulation compliance
- Secure API key management
- Audit logging
- Data encryption

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

**Dashboard URL**: http://localhost:8501  
**API Documentation**: http://localhost:8000/docs

