# Windows Deployment - Simplified

Clean, efficient Windows deployment for PMS Intelligence Hub.

## 🚀 Quick Start (One Command)

```cmd
deployment\windows\quick_start.bat
```

This single command will:
- ✅ Install Python automatically (if needed)
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Start the dashboard

## 📁 Files

| File | Purpose |
|------|---------|
| `quick_start.bat` | **One-command setup** - Recommended for everyone |
| `setup_clean.bat` | Interactive setup with detailed progress |
| `deploy_clean.bat` | Local or Docker deployment |
| `deploy.ps1` | Advanced PowerShell deployment |

## 🔧 Manual Options

### Interactive Setup
```cmd
deployment\windows\setup_clean.bat
```

### Local Development
```cmd
deployment\windows\deploy_clean.bat local
```

### Docker Deployment
```cmd
deployment\windows\deploy_clean.bat docker
```

## 📋 Requirements

- **Windows 10/11** (any edition)
- **Internet connection** (for automatic Python installation)
- **4GB RAM** minimum

## 🛠️ Troubleshooting

### Python Issues
If Python installation fails, install manually:
1. Download from [python.org](https://python.org)
2. Check "Add Python to PATH"
3. Run `quick_start.bat` again

### Package Installation Issues
The scripts automatically try multiple approaches:
1. Core packages first (streamlit, pandas, plotly)
2. Fallback to minimal requirements
3. Individual package installation if needed

### Access Issues
- Run Command Prompt as Administrator if needed
- Check Windows Defender/antivirus settings
- Ensure internet connectivity

## 🎯 What Gets Installed

**Core packages:**
- Streamlit (dashboard framework)
- Pandas (data processing)
- Plotly (charts and graphs)
- Requests (API connections)
- Python-dotenv (configuration)

**Optional packages** (installed if possible):
- FastAPI (backend API)
- SQLAlchemy (database)
- Additional visualization tools

---

**Need help?** Check the main [Windows Deployment Guide](../../docs/WINDOWS_DEPLOYMENT.md)

