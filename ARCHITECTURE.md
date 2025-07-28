# PMS Intelligence Hub - Architecture

## Overview
Portfolio Management Services dashboard integrating Salesforce CRM and Wealth Spectrum PMS data.

## Tech Stack
- **Frontend**: Streamlit + Plotly
- **Backend**: FastAPI + SQLAlchemy  
- **Database**: PostgreSQL (optional)
- **Deployment**: Docker + Local

## Data Sources
- **Salesforce**: Client data, relationship managers, AUM
- **Wealth Spectrum**: Portfolio holdings, transactions, performance

## Core Features
- Interactive dashboard with filtering
- Performance calculations (CAGR, Alpha, Beta, Sharpe)
- PDF report generation
- Real-time data synchronization

## Project Structure
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

## Deployment
- **Windows**: `deployment\windows\quick_start.bat`
- **Docker**: `docker-compose up`
- **Local**: `streamlit run src/dashboard/main_dashboard.py`

## Configuration
Copy `.env.example` to `.env` and configure API credentials.

