#!/bin/bash

echo "========================================"
echo "PMS Intelligence Hub - Smart Update"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if git is available
if ! command -v git &> /dev/null; then
    echo -e "${RED}ERROR: Git is not installed${NC}"
    echo "Please install Git first"
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}ERROR: Not in a Git repository${NC}"
    echo "Please run this script from the PMSVinchu directory"
    exit 1
fi

echo "[1/6] Backing up current configuration..."
[ -f ".env" ] && cp ".env" ".env.backup"
[ -f "pms_client_data.db" ] && cp "pms_client_data.db" "pms_client_data.db.backup"

echo "[2/6] Fetching latest changes from GitHub..."
git fetch origin

echo "[3/6] Checking for updates..."
COMMITS_BEHIND=$(git rev-list HEAD...origin/master --count)

if [ "$COMMITS_BEHIND" -eq 0 ]; then
    echo -e "${GREEN}✅ Already up to date! No changes to pull.${NC}"
    echo
else
    echo "Found $COMMITS_BEHIND new commits. Updating..."
    
    echo "[4/6] Stashing local changes (if any)..."
    git stash push -m "Auto-stash before update $(date)"
    
    echo "[5/6] Pulling latest changes..."
    if ! git pull origin master; then
        echo -e "${RED}ERROR: Failed to pull changes${NC}"
        echo "Restoring stashed changes..."
        git stash pop
        exit 1
    fi
    
    echo "[6/6] Restoring stashed changes..."
    git stash pop 2>/dev/null || true
fi

echo
echo "========================================"
echo "Checking Dependencies..."
echo "========================================"

# Check Python
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✅ Python found${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    echo -e "${GREEN}✅ Python found${NC}"
    PYTHON_CMD="python"
else
    echo -e "${YELLOW}WARNING: Python not found. Please install Python 3.11+${NC}"
    PYTHON_CMD="python3"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: Failed to create virtual environment${NC}"
        exit 1
    fi
fi

# Activate virtual environment and install/update dependencies
echo "Updating Python dependencies..."
source venv/bin/activate
pip install --upgrade pip >/dev/null 2>&1
pip install -r requirements-core.txt >/dev/null 2>&1

echo
echo "========================================"
echo "Restoring Data..."
echo "========================================"

# Restore backed up files
if [ -f ".env.backup" ]; then
    echo "Restoring environment configuration..."
    mv ".env.backup" ".env"
fi

if [ -f "pms_client_data.db.backup" ]; then
    echo "Restoring database..."
    mv "pms_client_data.db.backup" "pms_client_data.db"
fi

echo
echo "========================================"
echo -e "${GREEN}✅ UPDATE COMPLETED SUCCESSFULLY!${NC}"
echo "========================================"
echo
echo "Your PMS Intelligence Hub has been updated with the latest features."
echo "Your data and configuration have been preserved."
echo
echo "To start the dashboard:"
echo "  1. Run: ./deployment/linux/start.sh"
echo "  2. Or manually: source venv/bin/activate && streamlit run src/dashboard/main_dashboard.py"
echo
echo "Changes in this update:"
git log --oneline -5 HEAD
echo

