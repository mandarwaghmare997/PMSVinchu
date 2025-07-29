# Windows Deployment Guide

## Quick Start (Recommended)

**Single Command Setup:**
```cmd
deployment\windows\ultimate_setup.bat
```

This script will:
- ✅ Automatically run as Administrator
- ✅ Install Python if not found
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Start the dashboard

## What It Does

1. **Admin Check**: Automatically requests Administrator privileges
2. **Python Detection**: Finds existing Python or installs Python 3.11.7
3. **Environment Setup**: Creates isolated virtual environment
4. **Package Installation**: Installs core packages (streamlit, pandas, plotly)
5. **App Launch**: Starts the dashboard at http://localhost:8501

## Troubleshooting

### If the script fails:

1. **Run as Administrator**: Right-click → "Run as administrator"
2. **Check Internet**: Ensure internet connection for Python download
3. **Antivirus**: Temporarily disable antivirus during installation
4. **Manual Python**: Install Python from https://python.org if auto-install fails

### Common Issues:

- **"Access Denied"**: Run as Administrator
- **"Download Failed"**: Check internet connection
- **"Virtual Environment Failed"**: Python installation issue

## Alternative Scripts

If `ultimate_setup.bat` doesn't work:

- `simple_start.bat` - Basic setup without admin elevation
- `setup_clean.bat` - Interactive setup with progress
- `fix_python_path.bat` - Fix Python PATH issues

## Requirements

- Windows 10 or later
- Internet connection (for Python download if needed)
- Administrator privileges (script will request automatically)

## Dashboard Access

Once running:
- **URL**: http://localhost:8501
- **Stop**: Press Ctrl+C in the command window
- **Restart**: Run the script again

## Files Created

- `venv/` - Virtual environment
- `.env` - Configuration file
- `temp/` - Temporary files (auto-deleted)

The script is designed to be run multiple times safely.

