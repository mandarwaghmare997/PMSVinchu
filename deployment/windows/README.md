# Windows Deployment Files

This directory contains Windows-specific deployment scripts and configurations for the PMS Intelligence Hub.

## Quick Start

### For First-Time Users
```cmd
setup.bat
```
Interactive setup with guided configuration.

### For Developers
```cmd
deploy.bat local
```
Quick local development setup.

### For Production
```cmd
service\install_service.bat
```
Install as Windows service (requires administrator).

## File Structure

```
windows/
├── setup.bat                          # Interactive setup script
├── deploy.bat                         # Simple deployment script
├── deploy.ps1                         # Advanced PowerShell script
├── docker-compose.windows.yml         # Windows-optimized Docker Compose
├── dockerfiles/
│   └── Dockerfile.windows             # Windows-optimized Dockerfile
├── service/
│   ├── pms_hub_service.py            # Windows service implementation
│   ├── install_service.bat          # Service installation script
│   └── remove_service.bat           # Service removal script
├── nginx/
│   └── nginx.windows.conf            # Windows-optimized Nginx config
└── README.md                         # This file
```

## Deployment Options

### 1. Interactive Setup (`setup.bat`)
- **Best for**: First-time users, non-technical users
- **Features**: Guided setup, automatic dependency installation
- **Requirements**: Python 3.8+

### 2. Simple Deployment (`deploy.bat`)
- **Best for**: Quick development setup
- **Usage**: `deploy.bat [local|docker]`
- **Features**: Fast setup, minimal configuration

### 3. Advanced PowerShell (`deploy.ps1`)
- **Best for**: Advanced users, automation
- **Usage**: `.\deploy.ps1 -Environment [local|docker|service]`
- **Features**: Verbose logging, error handling, service installation

### 4. Windows Service
- **Best for**: Production environments
- **Requirements**: Administrator privileges
- **Features**: Auto-start, background operation, service management

### 5. Docker Desktop
- **Best for**: Containerized deployment
- **Requirements**: Docker Desktop for Windows
- **Features**: Complete isolation, easy scaling

## Prerequisites

### Required Software
- **Python 3.8+**: Download from [python.org](https://python.org)
  - ✅ Check "Add Python to PATH" during installation
  - ✅ Install for all users (recommended)

### Optional Software
- **Git**: For cloning repository
- **Docker Desktop**: For containerized deployment
- **Visual Studio Code**: For development

### System Requirements
- **OS**: Windows 10 (1903+) or Windows 11
- **Memory**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space
- **CPU**: 2+ cores

## Usage Examples

### Local Development
```cmd
# Quick setup
setup.bat

# Or manual deployment
deploy.bat local

# Or PowerShell
.\deploy.ps1 -Environment local
```

### Docker Deployment
```cmd
# Simple Docker deployment
deploy.bat docker

# Or PowerShell with logging
.\deploy.ps1 -Environment docker -Verbose
```

### Windows Service
```cmd
# Install service (run as Administrator)
service\install_service.bat

# Start service
net start PMSIntelligenceHub

# Stop service
net stop PMSIntelligenceHub

# Remove service
service\remove_service.bat
```

## Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```env
# Application
SECRET_KEY=your-secret-key
ENVIRONMENT=production

# Salesforce
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password
SALESFORCE_SECURITY_TOKEN=your_token

# Wealth Spectrum
WEALTH_SPECTRUM_API_KEY=your_api_key
```

### Windows-Specific Settings
```env
# Windows encoding
PYTHONIOENCODING=utf-8

# Streamlit settings
STREAMLIT_SERVER_HEADLESS=true
```

## Troubleshooting

### Common Issues

#### Python Not Found
```cmd
# Check Python installation
python --version
py --version

# If only py works, use py instead of python
py -m pip install --upgrade pip
```

#### Permission Errors
- Run Command Prompt as Administrator
- Check antivirus software settings
- Verify user permissions

#### Port Already in Use
```cmd
# Find process using port
netstat -ano | findstr :8501

# Kill process (replace PID)
taskkill /PID 1234 /F
```

#### Service Installation Fails
- Ensure running as Administrator
- Check Windows Event Log
- Verify Python virtual environment exists

### Log Files
- **Application**: `logs\pms_hub.log`
- **Service**: `logs\pms_service.log`
- **Deployment**: `deployment.log`

## Support

For detailed Windows deployment instructions, see:
- [Windows Deployment Guide](../docs/WINDOWS_DEPLOYMENT.md)
- [Main Documentation](../README.md)
- [GitHub Issues](https://github.com/mandarwaghmare997/PMSVinchu/issues)

## Security Notes

- Service installation requires administrator privileges
- Regular operation uses standard user privileges
- Configure Windows Firewall for network access
- Add antivirus exclusions for better performance
- Use strong passwords and API keys

---

**Windows deployment made easy!** 🪟✨

