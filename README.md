# PMS Intelligence Hub Dashboard

A comprehensive Financial Dashboard solution for SEBI-regulated Portfolio Management Services (PMS) entities to automate data consolidation from Salesforce CRM and Wealth Spectrum PMS systems.

## 🎯 Project Overview

This solution eliminates manual data consolidation by providing:
- **Automated Data Ingestion** from Salesforce (CRM) and Wealth Spectrum (PMS)
- **Interactive Dashboard** with filtering, sorting, and drill-down capabilities
- **Custom View Management** with save/load functionality
- **PDF Export** for reports and compliance
- **Real-time & Batch Processing** support
- **AWS & On-premise** deployment compatibility

## 🏗️ Architecture

```
Salesforce (API/CSV) ──┐
                       ├─► ETL Pipeline ──► Data Warehouse ──► FastAPI ──► Streamlit Dashboard
Wealth Spectrum (API/CSV) ──┘                                                    │
                                                                                 ▼
                                                                            PDF Reports
```

## 🚀 Features

### Core Dashboard Features
- **Multi-source Data Integration**: Salesforce CRM + Wealth Spectrum PMS
- **Dynamic Filtering**: Year, AUM, Investment Category, CAGR, Risk Profile
- **Interactive Charts**: Portfolio performance, AUM trends, client analytics
- **Client Search**: Quick access to specific client data (500+ clients supported)
- **Time-based Analysis**: Monthly, quarterly, yearly views
- **Asset-specific Views**: Equity, Debt, Hybrid fund analysis

### Advanced Features
- **Saved Views**: Bookmark custom filter combinations
- **PDF Export**: Generate branded reports with compliance footers
- **Role-based Access**: Optional RM-level data restrictions
- **Real-time Updates**: API-based live data refresh
- **Batch Processing**: CSV file import scheduling
- **Performance Metrics**: CAGR, XIRR, Alpha, Beta calculations

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI (Python) | REST API and business logic |
| **Frontend** | Streamlit | Interactive dashboard |
| **Database** | PostgreSQL/BigQuery | Data warehouse |
| **ETL** | Python (Pandas, Airflow) | Data ingestion and transformation |
| **Charts** | Plotly | Interactive visualizations |
| **Animations** | anime.js | UI enhancements |
| **PDF Export** | WeasyPrint/ReportLab | Report generation |
| **Authentication** | Streamlit Auth | User management |
| **Deployment** | Docker, AWS/On-premise | Containerized deployment |

## 📁 Project Structure

```
PMSVinchu/
├── src/
│   ├── data_ingestion/
│   │   ├── salesforce_connector.py
│   │   ├── wealth_spectrum_connector.py
│   │   └── csv_processor.py
│   ├── dashboard/
│   │   ├── main_dashboard.py
│   │   ├── components/
│   │   └── utils/
│   ├── api/
│   │   ├── main.py
│   │   └── endpoints/
│   └── database/
│       ├── models.py
│       └── migrations/
├── config/
├── tests/
├── docs/
├── requirements.txt
└── docker-compose.yml
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Docker (optional)

### Quick Start
```bash
# Clone repository
git clone https://github.com/mandarwaghmare997/PMSVinchu.git
cd PMSVinchu

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and database credentials

# Run database migrations
python src/database/setup.py

# Start the dashboard
streamlit run src/dashboard/main_dashboard.py
```

## 🔐 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/pms_db

# Salesforce API
SALESFORCE_CLIENT_ID=your_client_id
SALESFORCE_CLIENT_SECRET=your_client_secret
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password

# Wealth Spectrum API
WEALTH_SPECTRUM_API_KEY=your_api_key
WEALTH_SPECTRUM_BASE_URL=https://api.wealthspectrum.com

# Dashboard Settings
DASHBOARD_TITLE="PMS Intelligence Hub"
COMPANY_LOGO_URL=path/to/logo.png
```

## 📊 Data Sources

### Salesforce Integration
- **Client Data**: Names, contact info, onboarding dates
- **Relationship Manager**: RM assignments and hierarchies
- **AUM Data**: Assets under management tracking
- **Communication Logs**: Client interaction history

### Wealth Spectrum Integration
- **Portfolio Holdings**: Asset allocation and positions
- **Performance Metrics**: Returns, CAGR, risk metrics
- **Transaction History**: Buy/sell transactions
- **NAV Data**: Net asset value tracking
- **Benchmark Comparisons**: Index performance vs portfolio

## 🎨 Dashboard Views

### 1. Executive Summary
- Total AUM across all clients
- Performance overview (CAGR, returns)
- Top performing portfolios
- Risk distribution charts

### 2. Client Analytics
- Client-wise AUM and performance
- Onboarding trends
- RM-wise client distribution
- Geographic analysis

### 3. Portfolio Performance
- Time-series performance charts
- Benchmark comparisons
- Risk-return scatter plots
- Asset allocation breakdowns

### 4. Compliance & Reporting
- SEBI compliance metrics
- High watermark tracking
- Performance fee calculations
- Regulatory report templates

## 📈 Key Metrics Tracked

### Performance Metrics
- **CAGR**: Compound Annual Growth Rate
- **XIRR**: Extended Internal Rate of Return
- **Alpha**: Excess return vs benchmark
- **Beta**: Portfolio volatility vs market
- **Sharpe Ratio**: Risk-adjusted returns
- **Maximum Drawdown**: Peak-to-trough decline

### Business Metrics
- **AUM Growth**: Assets under management trends
- **Client Acquisition**: New client onboarding
- **Revenue Metrics**: Management fees, performance fees
- **Client Retention**: Churn analysis
- **Portfolio Turnover**: Trading activity levels

## 🔒 Security & Compliance

### Data Security
- **Encryption**: AES-256 for data at rest and in transit
- **Authentication**: Multi-factor authentication support
- **Audit Logging**: Complete access and modification logs
- **Data Masking**: PII protection in non-production environments

### SEBI Compliance
- **Data Localization**: India-based hosting options
- **Audit Trails**: Complete transaction and access logs
- **Reporting Standards**: SEBI-compliant report formats
- **Data Retention**: Regulatory data retention policies

## 🚀 Deployment Options

### AWS Deployment
```bash
# Using Docker and AWS ECS
docker build -t pms-dashboard .
# Deploy to ECS with RDS PostgreSQL
```

### On-Premise Deployment
```bash
# Using Docker Compose
docker-compose up -d
```

## 📝 API Documentation

### Core Endpoints
- `GET /api/clients` - List all clients with filters
- `GET /api/portfolios/{client_id}` - Client portfolio data
- `GET /api/performance` - Performance metrics
- `POST /api/views/save` - Save custom dashboard view
- `GET /api/export/pdf` - Generate PDF report

## 🧪 Testing

```bash
# Run unit tests
pytest tests/

# Run integration tests
pytest tests/integration/

# Run API tests
pytest tests/api/
```

## 📚 Documentation

- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)
- [User Manual](docs/user_guide.md)
- [Developer Guide](docs/development.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is proprietary software developed for SEBI-regulated PMS entities.

## 📞 Support

For technical support and feature requests, please contact the development team.

---

**Built with ❤️ for the Indian Financial Services Industry**

