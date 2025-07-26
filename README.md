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



## 🚀 Quick Start

### Option 1: Local Development
```bash
git clone https://github.com/mandarwaghmare997/PMSVinchu.git
cd PMSVinchu
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure your environment variables
python deployment/deploy.py local
```

### Option 2: Docker Deployment
```bash
git clone https://github.com/mandarwaghmare997/PMSVinchu.git
cd PMSVinchu
cp .env.example .env  # Configure your environment variables
python deployment/deploy.py docker
```

### Option 3: AWS Cloud Deployment
```bash
git clone https://github.com/mandarwaghmare997/PMSVinchu.git
cd PMSVinchu
aws configure  # Set up AWS credentials
cp .env.example .env  # Configure for production
python deployment/deploy.py aws
```

## 📊 Dashboard Features

### Interactive Analytics
- **Real-time Metrics**: Live AUM tracking, performance indicators, client statistics
- **Advanced Charts**: Plotly-powered visualizations with drill-down capabilities  
- **Custom Filters**: Multi-dimensional filtering by RM, category, risk profile, AUM range
- **Animated UI**: Smooth transitions and number counters using anime.js

### Data Management
- **Dual Integration**: Both API and CSV/Excel file support for maximum flexibility
- **Smart Caching**: Multi-layer caching strategy for optimal performance
- **Data Validation**: Comprehensive error handling and data quality checks
- **Export Options**: PDF reports, Excel exports, saved custom views

### Performance Analytics
- **20+ Financial Metrics**: CAGR, Alpha, Beta, Sharpe Ratio, VaR, Max Drawdown
- **Benchmark Analysis**: Compare portfolio performance against market indices
- **Risk Assessment**: Volatility analysis, downside deviation, risk-adjusted returns
- **Attribution Analysis**: Understand sources of portfolio performance

## 🏗️ Architecture Overview

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Salesforce    │    │ Wealth Spectrum │    │   File Upload   │
│      CRM        │    │      PMS        │    │   CSV/Excel    │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼───────────────┐
                    │     Data Ingestion Layer    │
                    │   (API + File Processing)   │
                    └─────────────┬───────────────┘
                                 │
                    ┌─────────────▼───────────────┐
                    │     Data Processing &       │
                    │    Performance Calculation  │
                    └─────────────┬───────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
┌─────────▼───────┐    ┌─────────▼───────┐    ┌─────────▼───────┐
│   Streamlit     │    │    FastAPI      │    │   PostgreSQL    │
│   Dashboard     │    │   Backend       │    │   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

#### Frontend & UI
- **Streamlit**: Interactive dashboard framework
- **Plotly**: Advanced charting and visualizations  
- **anime.js**: Smooth animations and transitions
- **Custom CSS**: Professional styling and responsive design

#### Backend & API
- **FastAPI**: High-performance API framework
- **Pydantic**: Data validation and settings management
- **SQLAlchemy**: Database ORM with connection pooling
- **Celery**: Background task processing

#### Data & Storage
- **PostgreSQL**: Primary database for production
- **Redis**: Caching and session management
- **SQLite**: Development database
- **S3**: File storage and backups (AWS deployment)

#### Infrastructure & Deployment
- **Docker**: Containerization with multi-service orchestration
- **Nginx**: Reverse proxy and load balancing
- **AWS**: Cloud deployment with free tier optimization
- **Grafana**: Monitoring and alerting

## 📁 Project Structure

```
PMSVinchu/
├── 📄 README.md                     # Project documentation
├── 📄 requirements.txt              # Python dependencies
├── 📄 docker-compose.yml           # Multi-service container setup
├── 📄 Dockerfile                   # Container configuration
├── 📄 .env.example                 # Environment variables template
├── 📁 src/                         # Source code
│   ├── 📁 api/                     # FastAPI backend
│   │   ├── 📄 main.py              # API application entry point
│   │   └── 📁 endpoints/           # API route definitions
│   ├── 📁 dashboard/               # Streamlit frontend
│   │   ├── 📄 main_dashboard.py    # Main dashboard application
│   │   ├── 📁 components/          # Reusable UI components
│   │   └── 📁 utils/               # Dashboard utilities
│   ├── 📁 data_ingestion/          # Data connectors
│   │   ├── 📄 salesforce_connector.py    # Salesforce CRM integration
│   │   └── 📄 wealth_spectrum_connector.py # PMS system integration
│   ├── 📁 database/                # Database models and migrations
│   │   └── 📄 models.py            # SQLAlchemy data models
│   └── 📁 config/                  # Configuration management
│       └── 📄 settings.py          # Pydantic settings
├── 📁 tests/                       # Test suite
│   └── 📄 test_dashboard.py        # Comprehensive test cases
├── 📁 deployment/                  # Deployment scripts and configs
│   ├── 📄 deploy.py                # Multi-environment deployment
│   └── 📄 config.yml               # Deployment configuration
├── 📁 docs/                        # Documentation
│   ├── 📄 architecture.md          # Technical architecture
│   └── 📄 DEPLOYMENT_GUIDE.md      # Deployment instructions
├── 📁 cache/                       # Data caching directory
├── 📁 logs/                        # Application logs
├── 📁 exports/                     # Generated reports
└── 📁 uploads/                     # File upload storage
```

## 🔧 Configuration

### Environment Variables

The application uses environment variables for configuration. Copy `.env.example` to `.env` and configure:

#### Core Application
```bash
APP_NAME="PMS Intelligence Hub"
SECRET_KEY=your-super-secret-key-change-this
ENVIRONMENT=production  # development, production, testing
DEBUG=false
```

#### Database Configuration
```bash
# PostgreSQL (Production)
DATABASE_URL=postgresql://user:password@localhost:5432/pms_db

# SQLite (Development)  
DATABASE_URL=sqlite:///./pms_hub.db
```

#### API Integrations
```bash
# Salesforce CRM
SALESFORCE_USERNAME=your_salesforce_username
SALESFORCE_PASSWORD=your_salesforce_password
SALESFORCE_SECURITY_TOKEN=your_security_token
SALESFORCE_API_VERSION=58.0

# Wealth Spectrum PMS
WEALTH_SPECTRUM_API_KEY=your_wealth_spectrum_api_key
WEALTH_SPECTRUM_BASE_URL=https://api.wealthspectrum.com
WEALTH_SPECTRUM_API_VERSION=v1
```

#### Security & Performance
```bash
# Security
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8501

# Caching
CACHE_TTL_SECONDS=3600
REDIS_URL=redis://localhost:6379/0

# Performance
DATABASE_POOL_SIZE=10
MAX_FILE_SIZE_MB=100
```

### Feature Configuration

Enable/disable features through environment variables:

```bash
# Feature Flags
ENABLE_API_DOCS=true
ENABLE_METRICS_ENDPOINT=true
ENABLE_AUDIT_LOGGING=true
ENABLE_PROFILING=false
```

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test categories
pytest tests/test_dashboard.py::TestDataLoader -v
pytest tests/test_dashboard.py::TestPerformanceCalculator -v
pytest tests/test_dashboard.py::TestIntegration -v
```

### Test Coverage

The test suite includes:
- **Unit Tests**: Individual component testing (50+ test cases)
- **Integration Tests**: End-to-end workflow validation  
- **Performance Tests**: Large dataset handling and benchmarks
- **Error Handling**: Edge cases and invalid input scenarios

### Continuous Integration

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ -v --cov=src
```

## 📈 Performance & Scalability

### Performance Metrics
- **Dashboard Load Time**: < 3 seconds with cached data
- **API Response Time**: < 500ms for standard queries
- **Data Processing**: 10,000+ records in < 2 seconds
- **Concurrent Users**: 50+ simultaneous users (Docker deployment)

### Scalability Features
- **Horizontal Scaling**: Load balancer support with multiple instances
- **Database Optimization**: Connection pooling, query optimization, indexing
- **Caching Strategy**: Multi-layer caching (Redis, Streamlit, application-level)
- **Async Processing**: Background tasks for data ingestion and report generation

### Resource Requirements

#### Minimum (Development)
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 10GB
- **Network**: Broadband internet

#### Recommended (Production)
- **CPU**: 4+ cores  
- **RAM**: 8GB+
- **Storage**: 50GB+ SSD
- **Network**: High-speed internet with low latency

#### AWS Free Tier Deployment
- **EC2**: t3.micro instances (1 vCPU, 1GB RAM)
- **RDS**: db.t3.micro (1 vCPU, 1GB RAM, 20GB storage)
- **Estimated Cost**: $0-5/month (within free tier limits)

## 🔒 Security & Compliance

### Security Features
- **Authentication**: JWT-based authentication with role-based access
- **Data Encryption**: TLS/SSL for data in transit, encrypted storage
- **Input Validation**: Comprehensive data validation and sanitization
- **Audit Logging**: Complete audit trail of user actions and data changes
- **Rate Limiting**: API rate limiting to prevent abuse

### SEBI Compliance
- **Data Privacy**: Client data protection and access controls
- **Audit Trail**: Complete logging of portfolio management activities
- **Report Generation**: Compliance-ready PDF reports with disclaimers
- **Data Retention**: Configurable data retention policies

### Best Practices
- **Secrets Management**: Environment-based configuration, no hardcoded secrets
- **Least Privilege**: Role-based access control with minimal permissions
- **Regular Updates**: Automated dependency updates and security patches
- **Backup Strategy**: Automated daily backups with retention policies

## 🤝 Contributing

We welcome contributions to the PMS Intelligence Hub! Here's how you can help:

### Development Setup
```bash
# Fork the repository and clone your fork
git clone https://github.com/yourusername/PMSVinchu.git
cd PMSVinchu

# Create a development branch
git checkout -b feature/your-feature-name

# Set up development environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests to ensure everything works
pytest tests/ -v
```

### Code Standards
- **Python Style**: Follow PEP 8, use Black for formatting
- **Documentation**: Comprehensive docstrings and comments
- **Testing**: Write tests for new features and bug fixes
- **Type Hints**: Use type hints for better code clarity

### Contribution Process
1. **Fork** the repository
2. **Create** a feature branch
3. **Write** code and tests
4. **Run** the test suite
5. **Submit** a pull request with detailed description

### Areas for Contribution
- **New Data Sources**: Additional PMS/CRM integrations
- **Advanced Analytics**: More financial metrics and calculations
- **UI/UX Improvements**: Enhanced dashboard features and visualizations
- **Performance Optimization**: Database queries, caching strategies
- **Documentation**: Tutorials, examples, API documentation

## 📞 Support & Community

### Getting Help
- **📚 Documentation**: Comprehensive guides in the `/docs` folder
- **🐛 Bug Reports**: GitHub Issues with detailed templates
- **💡 Feature Requests**: GitHub Discussions for new ideas
- **📧 Email Support**: support@pmsintelligencehub.com

### Community Resources
- **GitHub Discussions**: https://github.com/mandarwaghmare997/PMSVinchu/discussions
- **Issue Tracker**: https://github.com/mandarwaghmare997/PMSVinchu/issues
- **Wiki**: https://github.com/mandarwaghmare997/PMSVinchu/wiki

### Commercial Support
For enterprise deployments, custom integrations, or professional support:
- **Email**: enterprise@pmsintelligencehub.com
- **LinkedIn**: Connect with the development team
- **Consulting**: Custom development and deployment services available

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses
- **Streamlit**: Apache License 2.0
- **FastAPI**: MIT License  
- **Plotly**: MIT License
- **PostgreSQL**: PostgreSQL License
- **Redis**: BSD License

## 🙏 Acknowledgments

### Special Thanks
- **Salesforce**: For providing robust CRM APIs and documentation
- **Wealth Spectrum**: For PMS integration capabilities and support
- **Open Source Community**: For the amazing tools and libraries that make this project possible
- **Financial Industry**: For feedback and requirements that shaped this platform

### Built With
- ❤️ **Passion** for financial technology
- 🧠 **Intelligence** from industry experts  
- 🔧 **Modern Tools** and best practices
- 🌟 **Community** feedback and contributions

---

## 🎯 Roadmap

### Version 2.0 (Planned)
- **Mobile App**: React Native mobile application
- **Advanced ML**: Predictive analytics and portfolio optimization
- **Real-time Data**: WebSocket integration for live market data
- **Multi-tenant**: Support for multiple organizations

### Version 3.0 (Future)
- **AI Assistant**: Natural language queries and insights
- **Blockchain**: Cryptocurrency portfolio tracking
- **Global Markets**: International market support
- **Advanced Compliance**: Regulatory reporting automation

---

**Ready to revolutionize your portfolio management? Get started today!** 🚀

For the latest updates and releases, watch this repository and join our community discussions.



## 🪟 Windows Deployment

### Quick Windows Setup
```cmd
git clone https://github.com/mandarwaghmare997/PMSVinchu.git
cd PMSVinchu
deployment\windows\setup.bat
```

### Windows Deployment Options

#### 1. One-Click Setup (Recommended)
```cmd
deployment\windows\setup.bat
```
Perfect for first-time users with guided interactive setup.

#### 2. Command Line Deployment
```cmd
# Local development
deployment\windows\deploy.bat local

# Docker deployment
deployment\windows\deploy.bat docker
```

#### 3. PowerShell Advanced
```powershell
# Local with verbose logging
.\deployment\windows\deploy.ps1 -Environment local -Verbose

# Windows service installation (requires admin)
.\deployment\windows\deploy.ps1 -Environment service
```

#### 4. Windows Service (Production)
```cmd
# Install as Windows service (requires admin)
deployment\windows\service\install_service.bat

# Service management
net start PMSIntelligenceHub
net stop PMSIntelligenceHub
```

### Windows-Specific Features
- **🎯 One-Click Setup**: Interactive guided installation
- **🔧 Windows Service**: Production-ready service with auto-start
- **🐳 Docker Desktop**: Optimized for Windows containers
- **⚡ PowerShell**: Advanced automation with error handling
- **📊 Monitoring**: Built-in health checks and logging
- **🛡️ Security**: Windows-integrated authentication

### Windows Requirements
- **OS**: Windows 10 (1903+) or Windows 11
- **Python**: 3.8+ (with "Add to PATH" enabled)
- **Memory**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space

For detailed Windows deployment instructions, see [Windows Deployment Guide](docs/WINDOWS_DEPLOYMENT.md).

