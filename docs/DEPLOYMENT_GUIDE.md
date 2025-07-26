# PMS Intelligence Hub - Deployment Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Local Development Setup](#local-development-setup)
4. [Docker Deployment](#docker-deployment)
5. [AWS Cloud Deployment](#aws-cloud-deployment)
6. [Configuration Management](#configuration-management)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)
8. [Troubleshooting](#troubleshooting)

## Overview

The PMS Intelligence Hub supports multiple deployment environments to accommodate different use cases and infrastructure requirements. This guide provides step-by-step instructions for deploying the application in various environments.

### Deployment Options

| Environment | Use Case | Complexity | Cost | Scalability |
|-------------|----------|------------|------|-------------|
| **Local** | Development, Testing | Low | Free | Single User |
| **Docker** | Production, Team Use | Medium | Low | Multi-User |
| **AWS** | Enterprise, Scale | High | Variable | High |

## Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu 20.04+), macOS (10.15+), Windows 10+
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 10GB free space minimum
- **Network**: Internet connectivity for API integrations

### Required Software

```bash
# Python and pip
python3 --version  # Should be 3.8+
pip3 --version

# Git
git --version

# For Docker deployment
docker --version
docker-compose --version

# For AWS deployment
aws --version
```

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Application Settings
SECRET_KEY=your-super-secret-key-change-this
ENVIRONMENT=production
DEBUG=false

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/pms_db

# Salesforce Configuration
SALESFORCE_USERNAME=your_salesforce_username
SALESFORCE_PASSWORD=your_salesforce_password
SALESFORCE_SECURITY_TOKEN=your_security_token

# Wealth Spectrum Configuration
WEALTH_SPECTRUM_API_KEY=your_api_key
WEALTH_SPECTRUM_BASE_URL=https://api.wealthspectrum.com

# Optional: Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_USERNAME=your_email@company.com
SMTP_PASSWORD=your_email_password
```

## Local Development Setup

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mandarwaghmare997/PMSVinchu.git
   cd PMSVinchu
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the Application**
   ```bash
   python deployment/deploy.py local
   ```

6. **Access the Dashboard**
   - Open your browser and navigate to `http://localhost:8501`
   - The dashboard should load with sample data

### Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit dashboard directly
streamlit run src/dashboard/main_dashboard.py --server.port 8501

# In another terminal, run the API (optional)
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

## Docker Deployment

Docker deployment provides a complete, isolated environment with all services.

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 1.29+
- 8GB RAM recommended
- 20GB free disk space

### Deployment Steps

1. **Prepare Environment**
   ```bash
   git clone https://github.com/mandarwaghmare997/PMSVinchu.git
   cd PMSVinchu
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Deploy with Docker Compose**
   ```bash
   python deployment/deploy.py docker
   ```

   Or manually:
   ```bash
   docker-compose up --build -d
   ```

3. **Verify Deployment**
   ```bash
   docker-compose ps
   ```

4. **Access Services**
   - **Dashboard**: http://localhost:8501
   - **API Documentation**: http://localhost:8000/docs
   - **Grafana Monitoring**: http://localhost:3000 (admin/admin123)
   - **PostgreSQL**: localhost:5432

### Docker Services Overview

| Service | Purpose | Port | Health Check |
|---------|---------|------|--------------|
| **postgres** | Database | 5432 | `pg_isready` |
| **redis** | Caching | 6379 | `redis-cli ping` |
| **api** | Backend API | 8000 | `/health` |
| **dashboard** | Streamlit UI | 8501 | `/_stcore/health` |
| **nginx** | Reverse Proxy | 80/443 | HTTP check |
| **worker** | Background Tasks | - | Process check |
| **grafana** | Monitoring | 3000 | `/api/health` |

### Docker Management Commands

```bash
# View logs
docker-compose logs -f dashboard
docker-compose logs -f api

# Restart services
docker-compose restart dashboard

# Update services
docker-compose pull
docker-compose up -d

# Stop all services
docker-compose down

# Remove all data (careful!)
docker-compose down -v
```

## AWS Cloud Deployment

AWS deployment provides enterprise-grade scalability and reliability.

### Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured with credentials
- Domain name (optional, for SSL)
- Basic understanding of AWS services

### Cost Estimation

**Free Tier Usage (First 12 months):**
- EC2 t3.micro: 750 hours/month (Free)
- RDS db.t3.micro: 750 hours/month (Free)
- S3: 5GB storage (Free)
- **Estimated Monthly Cost**: $0-5 (within free tier limits)

**Production Usage:**
- EC2 t3.small: ~$15/month
- RDS db.t3.small: ~$25/month
- Load Balancer: ~$20/month
- **Estimated Monthly Cost**: $60-80

### Deployment Steps

1. **Configure AWS CLI**
   ```bash
   aws configure
   # Enter your AWS Access Key ID, Secret Access Key, and region
   ```

2. **Prepare Deployment**
   ```bash
   git clone https://github.com/mandarwaghmare997/PMSVinchu.git
   cd PMSVinchu
   cp .env.example .env
   # Configure with production values
   ```

3. **Deploy to AWS**
   ```bash
   python deployment/deploy.py aws
   ```

### AWS Architecture

The AWS deployment creates the following infrastructure:

```
Internet Gateway
       |
   Load Balancer (ALB)
       |
   +---------+---------+
   |                   |
EC2 Instance      EC2 Instance
(Dashboard)       (API)
   |                   |
   +------- RDS -------+
   |                   |
   +---- ElastiCache --+
   |                   |
   +------ S3 ---------+
```

### AWS Services Used

| Service | Purpose | Configuration |
|---------|---------|---------------|
| **EC2** | Application hosting | t3.micro instances |
| **RDS** | PostgreSQL database | db.t3.micro |
| **ALB** | Load balancing | Application Load Balancer |
| **S3** | File storage | Standard storage class |
| **CloudWatch** | Monitoring | Logs and metrics |
| **IAM** | Security | Least privilege roles |
| **VPC** | Networking | Private subnets |

### Post-Deployment Configuration

1. **Update DNS Records**
   ```bash
   # Point your domain to the Load Balancer DNS name
   # Example: pms-hub.yourdomain.com -> alb-xxxxxxxxx.us-east-1.elb.amazonaws.com
   ```

2. **Configure SSL Certificate**
   ```bash
   # Request SSL certificate through AWS Certificate Manager
   aws acm request-certificate --domain-name pms-hub.yourdomain.com
   ```

3. **Set up Monitoring Alerts**
   ```bash
   # CloudWatch alarms are automatically configured
   # Check AWS Console -> CloudWatch -> Alarms
   ```

## Configuration Management

### Environment-Specific Configuration

The application uses a hierarchical configuration system:

1. **Default values** in `src/config/settings.py`
2. **Environment file** `.env`
3. **Environment variables** (highest priority)

### Key Configuration Areas

#### Database Configuration
```bash
# PostgreSQL (Production)
DATABASE_URL=postgresql://user:password@host:5432/database

# SQLite (Development)
DATABASE_URL=sqlite:///./pms_hub.db
```

#### API Integration
```bash
# Salesforce
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password
SALESFORCE_SECURITY_TOKEN=your_token

# Wealth Spectrum
WEALTH_SPECTRUM_API_KEY=your_api_key
WEALTH_SPECTRUM_BASE_URL=https://api.wealthspectrum.com
```

#### Security Settings
```bash
SECRET_KEY=your-secret-key-minimum-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Configuration Validation

The application automatically validates configuration on startup:

```bash
# Check configuration
python -c "from src.config.settings import get_settings, validate_configuration; settings = get_settings(); print(validate_configuration(settings))"
```

## Monitoring and Maintenance

### Health Checks

The application provides several health check endpoints:

| Endpoint | Purpose | Expected Response |
|----------|---------|-------------------|
| `/health` | API health | `{"status": "healthy"}` |
| `/_stcore/health` | Dashboard health | HTTP 200 |
| `/db/health` | Database connectivity | `{"database": "connected"}` |

### Monitoring Dashboard

Access Grafana at `http://localhost:3000` (Docker) with:
- **Username**: admin
- **Password**: admin123

Key metrics monitored:
- Application response times
- Database connection pool usage
- Memory and CPU utilization
- Error rates and exceptions
- User activity and session counts

### Log Management

Logs are stored in the following locations:

```bash
# Application logs
logs/pms_hub.log

# Docker logs
docker-compose logs dashboard
docker-compose logs api

# AWS CloudWatch logs
# Check AWS Console -> CloudWatch -> Log Groups
```

### Backup Procedures

#### Automated Backups

Backups are automatically created daily at 2 AM UTC:

```bash
# Local backups
ls -la backups/

# S3 backups (AWS deployment)
aws s3 ls s3://pms-hub-backups/daily-backups/
```

#### Manual Backup

```bash
# Create manual backup
python deployment/backup.py --type manual

# Restore from backup
python deployment/restore.py --backup-file backup_20240101_120000.tar.gz
```

### Update Procedures

#### Application Updates

```bash
# Pull latest changes
git pull origin master

# Update dependencies
pip install -r requirements.txt

# Restart services
docker-compose restart dashboard api
```

#### Database Migrations

```bash
# Run database migrations
python src/database/migrate.py

# Verify migration
python src/database/verify_schema.py
```

## Troubleshooting

### Common Issues

#### 1. Dashboard Won't Start

**Symptoms**: Streamlit dashboard fails to load
**Solutions**:
```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip install -r requirements.txt

# Check port availability
netstat -tulpn | grep 8501

# Run with verbose logging
streamlit run src/dashboard/main_dashboard.py --logger.level=debug
```

#### 2. Database Connection Issues

**Symptoms**: "Database connection failed" errors
**Solutions**:
```bash
# Check database status
docker-compose ps postgres

# Check connection string
echo $DATABASE_URL

# Test connection manually
python -c "import psycopg2; conn = psycopg2.connect('your_database_url'); print('Connected successfully')"

# Reset database
docker-compose down postgres
docker-compose up -d postgres
```

#### 3. API Integration Failures

**Symptoms**: "Failed to load data from Salesforce/Wealth Spectrum"
**Solutions**:
```bash
# Check API credentials
python -c "from src.data_ingestion.salesforce_connector import SalesforceConnector; print('Testing connection...')"

# Check network connectivity
curl -I https://login.salesforce.com
curl -I https://api.wealthspectrum.com

# Review API logs
tail -f logs/pms_hub.log | grep -i "salesforce\|wealth"
```

#### 4. Performance Issues

**Symptoms**: Slow dashboard loading, timeouts
**Solutions**:
```bash
# Check system resources
htop
df -h

# Clear cache
rm -rf cache/*
docker-compose restart redis

# Optimize database
python src/database/optimize.py

# Check slow queries
tail -f logs/pms_hub.log | grep -i "slow"
```

#### 5. Docker Issues

**Symptoms**: Services won't start, container crashes
**Solutions**:
```bash
# Check Docker status
docker system info

# View container logs
docker-compose logs --tail=50 dashboard

# Restart specific service
docker-compose restart dashboard

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Getting Help

#### Log Collection

When reporting issues, please collect the following logs:

```bash
# Application logs
tar -czf logs_$(date +%Y%m%d_%H%M%S).tar.gz logs/

# Docker logs
docker-compose logs > docker_logs_$(date +%Y%m%d_%H%M%S).log

# System information
python --version > system_info.txt
docker --version >> system_info.txt
docker-compose --version >> system_info.txt
uname -a >> system_info.txt
```

#### Support Channels

- **GitHub Issues**: https://github.com/mandarwaghmare997/PMSVinchu/issues
- **Documentation**: https://github.com/mandarwaghmare997/PMSVinchu/docs
- **Email Support**: support@pmsintelligencehub.com

### Performance Tuning

#### Database Optimization

```sql
-- Create indexes for better performance
CREATE INDEX idx_clients_status ON clients(status);
CREATE INDEX idx_portfolios_client_id ON portfolios(client_id);
CREATE INDEX idx_performance_portfolio_date ON performance_records(portfolio_id, period_end_date);
```

#### Caching Configuration

```bash
# Redis cache optimization
CACHE_TTL_SECONDS=3600
REDIS_MAX_CONNECTIONS=20
REDIS_CONNECTION_POOL_KWARGS={"max_connections": 20, "retry_on_timeout": True}
```

#### Application Tuning

```python
# Streamlit configuration
[server]
maxUploadSize = 200
maxMessageSize = 200

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
```

---

## Conclusion

This deployment guide covers all major deployment scenarios for the PMS Intelligence Hub. For additional support or custom deployment requirements, please refer to the project documentation or contact the development team.

Remember to:
- Always backup your data before major updates
- Monitor system resources and performance
- Keep your API credentials secure
- Regularly update dependencies and security patches
- Test deployments in a staging environment first

Happy deploying! 🚀

