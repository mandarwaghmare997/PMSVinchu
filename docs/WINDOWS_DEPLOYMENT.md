# PMS Intelligence Hub - Windows Deployment Guide

## Table of Contents
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Quick Start](#quick-start)
4. [Deployment Options](#deployment-options)
5. [Windows Service Installation](#windows-service-installation)
6. [Docker on Windows](#docker-on-windows)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)
9. [Performance Optimization](#performance-optimization)
10. [Security Considerations](#security-considerations)

## Overview

The PMS Intelligence Hub provides comprehensive Windows deployment support with multiple options to suit different use cases and environments. This guide covers Windows-specific deployment procedures, optimizations, and best practices.

### Windows Deployment Features

- **🎯 One-Click Setup**: Simple batch files for non-technical users
- **⚡ PowerShell Automation**: Advanced scripting with error handling and logging
- **🔧 Windows Service**: Production-ready service installation with auto-start
- **🐳 Docker Desktop**: Optimized containers for Windows environments
- **📊 Monitoring**: Built-in health checks and performance monitoring
- **🛡️ Security**: Windows-integrated authentication and permissions

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **Operating System** | Windows 10 (1903+) or Windows 11 |
| **Memory** | 4GB RAM |
| **Storage** | 10GB free space |
| **CPU** | 2 cores, 2.0 GHz |
| **Network** | Internet connectivity |

### Recommended Requirements

| Component | Requirement |
|-----------|-------------|
| **Operating System** | Windows 11 or Windows Server 2019+ |
| **Memory** | 8GB+ RAM |
| **Storage** | 50GB+ SSD |
| **CPU** | 4+ cores, 3.0 GHz |
| **Network** | High-speed broadband |

### Software Prerequisites

#### Required Software
- **Python 3.8+**: Download from [python.org](https://python.org)
- **Git**: Download from [git-scm.com](https://git-scm.com) (optional but recommended)

#### Optional Software
- **Docker Desktop**: For containerized deployment
- **Visual Studio Code**: For development and configuration editing
- **Windows Terminal**: Enhanced command-line experience

### Python Installation Notes

When installing Python on Windows:
1. ✅ **Check "Add Python to PATH"** during installation
2. ✅ **Install for all users** (recommended)
3. ✅ **Include pip** (should be default)
4. ✅ **Install py launcher** (recommended)

## Quick Start

### Option 1: One-Click Setup (Recommended for Beginners)

1. **Download the Repository**
   ```cmd
   git clone https://github.com/mandarwaghmare997/PMSVinchu.git
   cd PMSVinchu
   ```

2. **Run Quick Setup**
   ```cmd
   deployment\windows\setup.bat
   ```

3. **Follow the Interactive Setup**
   - The script will check requirements
   - Install dependencies automatically
   - Configure the application
   - Start the dashboard

4. **Access the Dashboard**
   - Open your browser to `http://localhost:8501`

### Option 2: Command Line Deployment

```cmd
# Clone repository
git clone https://github.com/mandarwaghmare997/PMSVinchu.git
cd PMSVinchu

# Local development
deployment\windows\deploy.bat local

# Docker deployment
deployment\windows\deploy.bat docker
```

### Option 3: PowerShell Advanced Deployment

```powershell
# Local deployment with verbose logging
.\deployment\windows\deploy.ps1 -Environment local -Verbose

# Docker deployment
.\deployment\windows\deploy.ps1 -Environment docker

# Windows service installation
.\deployment\windows\deploy.ps1 -Environment service
```

## Deployment Options

### 1. Local Development Deployment

**Best for**: Development, testing, single-user scenarios

**Features**:
- Quick setup and startup
- Easy debugging and development
- Minimal resource usage
- Direct file system access

**Setup**:
```cmd
deployment\windows\deploy.bat local
```

**Access**:
- Dashboard: `http://localhost:8501`
- Logs: `logs\pms_hub.log`

### 2. Docker Desktop Deployment

**Best for**: Production, team environments, isolated deployment

**Features**:
- Complete isolation
- Consistent environment
- Easy scaling
- Built-in monitoring

**Prerequisites**:
- Docker Desktop for Windows
- WSL 2 (recommended)
- 8GB+ RAM

**Setup**:
```cmd
deployment\windows\deploy.bat docker
```

**Access**:
- Dashboard: `http://localhost:8501`
- API: `http://localhost:8000`
- Grafana: `http://localhost:3000`

### 3. Windows Service Deployment

**Best for**: Production servers, always-on deployment, enterprise environments

**Features**:
- Automatic startup with Windows
- Background operation
- Service management integration
- Automatic restart on failure

**Prerequisites**:
- Administrator privileges
- Python virtual environment setup

**Setup**:
```cmd
# Run as Administrator
deployment\windows\service\install_service.bat
```

**Management**:
```cmd
# Start service
net start PMSIntelligenceHub

# Stop service
net stop PMSIntelligenceHub

# Remove service
deployment\windows\service\remove_service.bat
```

## Windows Service Installation

### Detailed Installation Steps

1. **Prepare Environment**
   ```cmd
   # Run initial setup first
   deployment\windows\setup.bat
   ```

2. **Open Administrator Command Prompt**
   - Press `Win + X`
   - Select "Command Prompt (Admin)" or "PowerShell (Admin)"
   - Navigate to the project directory

3. **Install Service**
   ```cmd
   deployment\windows\service\install_service.bat
   ```

4. **Start Service**
   ```cmd
   net start PMSIntelligenceHub
   ```

### Service Configuration

The Windows service is configured with the following settings:

| Setting | Value |
|---------|-------|
| **Service Name** | PMSIntelligenceHub |
| **Display Name** | PMS Intelligence Hub Dashboard |
| **Startup Type** | Automatic |
| **Log On As** | Local System |
| **Dependencies** | None |

### Service Management

#### Using Windows Services Manager
1. Press `Win + R`, type `services.msc`, press Enter
2. Find "PMS Intelligence Hub Dashboard"
3. Right-click for options (Start, Stop, Restart, Properties)

#### Using Command Line
```cmd
# Service status
sc query PMSIntelligenceHub

# Start service
net start PMSIntelligenceHub

# Stop service
net stop PMSIntelligenceHub

# Restart service
net stop PMSIntelligenceHub && net start PMSIntelligenceHub
```

#### Using PowerShell
```powershell
# Service status
Get-Service PMSIntelligenceHub

# Start service
Start-Service PMSIntelligenceHub

# Stop service
Stop-Service PMSIntelligenceHub

# Restart service
Restart-Service PMSIntelligenceHub
```

### Service Logs

Service logs are written to:
- **Service Log**: `logs\pms_service.log`
- **Application Log**: `logs\pms_hub.log`
- **Windows Event Log**: Windows Logs > Application

## Docker on Windows

### Docker Desktop Setup

1. **Install Docker Desktop**
   - Download from [docker.com](https://docker.com)
   - Enable WSL 2 integration (recommended)
   - Allocate at least 4GB RAM to Docker

2. **Configure Docker Desktop**
   ```
   Settings > Resources > Advanced:
   - Memory: 8GB (recommended)
   - CPUs: 4 (recommended)
   - Disk image size: 60GB
   ```

3. **Enable WSL 2 Integration**
   ```
   Settings > Resources > WSL Integration:
   - Enable integration with default WSL distro
   - Enable integration with additional distros (if any)
   ```

### Windows-Specific Docker Configuration

The project includes Windows-optimized Docker configurations:

- **`docker-compose.windows.yml`**: Windows-specific service definitions
- **Volume Mounting**: Proper Windows path handling
- **Networking**: Windows-compatible bridge networking
- **Resource Limits**: Optimized for Windows containers

### Docker Deployment Commands

```cmd
# Using Windows-specific compose file
docker-compose -f deployment\windows\docker-compose.windows.yml up -d

# View logs
docker-compose -f deployment\windows\docker-compose.windows.yml logs -f

# Stop services
docker-compose -f deployment\windows\docker-compose.windows.yml down

# Rebuild and restart
docker-compose -f deployment\windows\docker-compose.windows.yml up --build -d
```

### Docker Service Management

```cmd
# Check container status
docker ps

# View specific service logs
docker logs pms_dashboard_win
docker logs pms_api_win

# Execute commands in containers
docker exec -it pms_dashboard_win bash

# Monitor resource usage
docker stats
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with your configuration:

```env
# Application Settings
APP_NAME=PMS Intelligence Hub
SECRET_KEY=your-super-secret-key-change-this-for-production
ENVIRONMENT=production
DEBUG=false

# Database Configuration (for Docker deployment)
DATABASE_URL=postgresql://pms_user:pms_password@localhost:5432/pms_db

# Salesforce Configuration
SALESFORCE_USERNAME=your_salesforce_username
SALESFORCE_PASSWORD=your_salesforce_password
SALESFORCE_SECURITY_TOKEN=your_security_token

# Wealth Spectrum Configuration
WEALTH_SPECTRUM_API_KEY=your_api_key
WEALTH_SPECTRUM_BASE_URL=https://api.wealthspectrum.com

# Windows-Specific Settings
PYTHONIOENCODING=utf-8
STREAMLIT_SERVER_HEADLESS=true
```

### Windows-Specific Configuration

#### File Paths
Use forward slashes or escaped backslashes in configuration:
```env
# Correct
LOG_FILE_PATH=logs/application.log
UPLOAD_PATH=uploads/

# Also correct
LOG_FILE_PATH=logs\\application.log
UPLOAD_PATH=uploads\\
```

#### Windows Firewall
If you encounter connection issues, configure Windows Firewall:

1. **Allow Python through Firewall**
   - Windows Security > Firewall & network protection
   - Allow an app through firewall
   - Add Python.exe from your virtual environment

2. **Allow Specific Ports**
   ```cmd
   # Allow Streamlit port
   netsh advfirewall firewall add rule name="PMS Hub Dashboard" dir=in action=allow protocol=TCP localport=8501

   # Allow API port
   netsh advfirewall firewall add rule name="PMS Hub API" dir=in action=allow protocol=TCP localport=8000
   ```

#### Windows Defender
Add exclusions for better performance:
1. Windows Security > Virus & threat protection
2. Manage settings under "Virus & threat protection settings"
3. Add exclusions for:
   - Project directory
   - Python virtual environment directory
   - Docker Desktop (if using Docker)

## Troubleshooting

### Common Issues and Solutions

#### 1. Python Not Found
**Error**: `'python' is not recognized as an internal or external command`

**Solution**:
```cmd
# Check if Python is installed
py --version

# If py works but python doesn't, use py instead
py -m pip install --upgrade pip

# Or add Python to PATH manually
# Add C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\ to PATH
```

#### 2. Permission Denied Errors
**Error**: `PermissionError: [WinError 5] Access is denied`

**Solutions**:
- Run Command Prompt as Administrator
- Check antivirus software isn't blocking files
- Ensure user has write permissions to project directory

#### 3. Port Already in Use
**Error**: `OSError: [WinError 10048] Only one usage of each socket address`

**Solutions**:
```cmd
# Find process using port 8501
netstat -ano | findstr :8501

# Kill process (replace PID with actual process ID)
taskkill /PID 1234 /F

# Or use different port
streamlit run src\dashboard\main_dashboard.py --server.port 8502
```

#### 4. Virtual Environment Issues
**Error**: Virtual environment activation fails

**Solutions**:
```cmd
# Remove existing venv
rmdir /s venv

# Recreate virtual environment
python -m venv venv

# Activate with full path
venv\Scripts\activate.bat

# If execution policy error in PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 5. Docker Desktop Issues
**Error**: Docker commands fail or containers won't start

**Solutions**:
- Restart Docker Desktop
- Check WSL 2 is enabled and updated
- Increase Docker memory allocation
- Reset Docker Desktop to factory defaults

#### 6. Windows Service Issues
**Error**: Service fails to start or install

**Solutions**:
```cmd
# Check service status
sc query PMSIntelligenceHub

# View service logs
type logs\pms_service.log

# Reinstall service
deployment\windows\service\remove_service.bat
deployment\windows\service\install_service.bat

# Check Windows Event Log
eventvwr.msc
```

### Diagnostic Commands

```cmd
# System information
systeminfo

# Python environment
python --version
pip list

# Network connectivity
ping google.com
telnet localhost 8501

# Process information
tasklist | findstr python
tasklist | findstr streamlit

# Port usage
netstat -ano | findstr :8501
netstat -ano | findstr :8000

# Disk space
dir /s
```

### Log Files

Check these log files for troubleshooting:

| Log File | Purpose |
|----------|---------|
| `logs\pms_hub.log` | Application logs |
| `logs\pms_service.log` | Windows service logs |
| `deployment.log` | Deployment script logs |
| `logs\error.log` | Error logs |

## Performance Optimization

### Windows-Specific Optimizations

#### 1. Virtual Memory
Configure virtual memory for better performance:
1. System Properties > Advanced > Performance Settings
2. Advanced > Virtual Memory > Change
3. Set custom size: Initial = RAM size, Maximum = 2x RAM size

#### 2. Power Settings
Set high performance power plan:
```cmd
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
```

#### 3. Windows Search Indexing
Exclude project directory from indexing:
1. Control Panel > Indexing Options
2. Modify > Uncheck project directory

#### 4. Antivirus Exclusions
Add exclusions for:
- Project directory
- Python installation directory
- Virtual environment directory

### Application Performance

#### 1. Memory Management
```env
# Limit Streamlit memory usage
STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
STREAMLIT_SERVER_MAX_MESSAGE_SIZE=200
```

#### 2. Database Optimization
```env
# Connection pooling
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
```

#### 3. Caching Configuration
```env
# Cache settings
CACHE_TTL_SECONDS=3600
REDIS_MAX_CONNECTIONS=20
```

## Security Considerations

### Windows Security Features

#### 1. User Account Control (UAC)
- Service installation requires administrator privileges
- Regular operation runs with standard user privileges
- Use "Run as administrator" only when necessary

#### 2. Windows Firewall
Configure firewall rules for network access:
```cmd
# Inbound rules for dashboard
netsh advfirewall firewall add rule name="PMS Hub Dashboard" dir=in action=allow protocol=TCP localport=8501

# Outbound rules for API access
netsh advfirewall firewall add rule name="PMS Hub API Access" dir=out action=allow protocol=TCP remoteport=443
```

#### 3. Windows Defender
- Add exclusions for project directory
- Configure real-time protection settings
- Schedule regular scans outside business hours

### Application Security

#### 1. Environment Variables
Store sensitive configuration in environment variables:
```env
# Use strong, unique values
SECRET_KEY=your-256-bit-secret-key-here
DATABASE_PASSWORD=strong-database-password
API_KEYS=your-encrypted-api-keys
```

#### 2. File Permissions
Set appropriate file permissions:
```cmd
# Restrict access to configuration files
icacls .env /grant:r "%USERNAME%":R /inheritance:r

# Secure log directory
icacls logs /grant:r "%USERNAME%":F /inheritance:r
```

#### 3. Network Security
- Use HTTPS in production
- Implement rate limiting
- Configure CORS properly
- Use VPN for remote access

### Best Practices

1. **Regular Updates**
   - Keep Windows updated
   - Update Python and dependencies regularly
   - Monitor security advisories

2. **Backup Strategy**
   - Regular configuration backups
   - Database backups (if applicable)
   - Document recovery procedures

3. **Monitoring**
   - Enable application logging
   - Monitor system resources
   - Set up alerts for failures

4. **Access Control**
   - Use principle of least privilege
   - Implement role-based access
   - Regular access reviews

---

## Conclusion

This Windows deployment guide provides comprehensive instructions for deploying the PMS Intelligence Hub on Windows systems. Choose the deployment method that best fits your needs:

- **Quick Setup**: For immediate evaluation and testing
- **Local Development**: For development and single-user scenarios
- **Docker Desktop**: For production and team environments
- **Windows Service**: For enterprise and always-on deployments

For additional support or questions, please refer to the main project documentation or contact the development team.

**Happy deploying on Windows!** 🪟🚀

