# PMS Intelligence Hub - Windows PowerShell Deployment Script
# Advanced deployment with error handling, logging, and service management

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("local", "docker", "service", "help")]
    [string]$Environment = "local",
    
    [Parameter(Mandatory=$false)]
    [switch]$Force,
    
    [Parameter(Mandatory=$false)]
    [switch]$Verbose,
    
    [Parameter(Mandatory=$false)]
    [string]$LogFile = "deployment.log"
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Enable verbose output if requested
if ($Verbose) {
    $VerbosePreference = "Continue"
}

# Function to write log messages
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    # Write to console with color coding
    switch ($Level) {
        "ERROR" { Write-Host $logMessage -ForegroundColor Red }
        "WARN"  { Write-Host $logMessage -ForegroundColor Yellow }
        "SUCCESS" { Write-Host $logMessage -ForegroundColor Green }
        default { Write-Host $logMessage -ForegroundColor White }
    }
    
    # Write to log file
    Add-Content -Path $LogFile -Value $logMessage
}

# Function to check prerequisites
function Test-Prerequisites {
    Write-Log "Checking prerequisites..."
    
    # Check PowerShell version
    if ($PSVersionTable.PSVersion.Major -lt 5) {
        Write-Log "PowerShell 5.0+ is required. Current version: $($PSVersionTable.PSVersion)" "ERROR"
        return $false
    }
    
    # Check Python installation
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Log "Python is not installed or not in PATH" "ERROR"
            Write-Log "Please install Python 3.8+ from https://python.org" "ERROR"
            return $false
        }
        
        Write-Log "Found Python: $pythonVersion"
        
        # Check Python version - support 3.8 and higher
        if ($pythonVersion -match "Python (\d+)\.(\d+)") {
            $majorVersion = [int]$matches[1]
            $minorVersion = [int]$matches[2]
            
            if ($majorVersion -eq 3 -and $minorVersion -ge 8) {
                Write-Log "Python version check passed: $pythonVersion"
            } elseif ($majorVersion -gt 3) {
                Write-Log "Python version check passed: $pythonVersion"
            } else {
                Write-Log "Python 3.8+ is required. Found: $pythonVersion" "ERROR"
                return $false
            }
        } else {
            Write-Log "Could not parse Python version: $pythonVersion" "ERROR"
            return $false
        }
    }
    catch {
        Write-Log "Error checking Python: $($_.Exception.Message)" "ERROR"
        return $false
    }
    
    # Check Git (optional but recommended)
    try {
        $gitVersion = git --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Log "Found Git: $gitVersion"
        }
    }
    catch {
        Write-Log "Git not found (optional)" "WARN"
    }
    
    return $true
}

# Function to setup virtual environment
function Setup-VirtualEnvironment {
    Write-Log "Setting up Python virtual environment..."
    
    if (Test-Path "venv") {
        if ($Force) {
            Write-Log "Removing existing virtual environment..."
            Remove-Item -Path "venv" -Recurse -Force
        } else {
            Write-Log "Virtual environment already exists. Use -Force to recreate."
            return $true
        }
    }
    
    try {
        # Create virtual environment
        python -m venv venv
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create virtual environment"
        }
        
        # Activate virtual environment
        & "venv\Scripts\Activate.ps1"
        
        # Upgrade pip
        Write-Log "Upgrading pip..."
        python -m pip install --upgrade pip
        
        # Install requirements
        Write-Log "Installing Python dependencies..."
        pip install -r requirements.txt
        
        Write-Log "Virtual environment setup completed successfully" "SUCCESS"
        return $true
    }
    catch {
        Write-Log "Error setting up virtual environment: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Function to setup configuration
function Setup-Configuration {
    Write-Log "Setting up configuration..."
    
    if (-not (Test-Path ".env")) {
        if (Test-Path ".env.example") {
            Copy-Item ".env.example" ".env"
            Write-Log "Created .env file from template"
            Write-Log "IMPORTANT: Please edit .env file with your configuration" "WARN"
            
            # Ask user if they want to edit the file now
            $response = Read-Host "Do you want to edit the .env file now? (y/n)"
            if ($response -eq "y" -or $response -eq "Y") {
                notepad .env
            }
        } else {
            Write-Log ".env.example file not found" "ERROR"
            return $false
        }
    } else {
        Write-Log ".env file already exists"
    }
    
    # Create necessary directories
    $directories = @("cache", "logs", "exports", "uploads", "backups")
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir | Out-Null
            Write-Log "Created directory: $dir"
        }
    }
    
    return $true
}

# Function for local deployment
function Deploy-Local {
    Write-Log "Starting local deployment..." "SUCCESS"
    
    if (-not (Test-Prerequisites)) {
        return $false
    }
    
    if (-not (Setup-VirtualEnvironment)) {
        return $false
    }
    
    if (-not (Setup-Configuration)) {
        return $false
    }
    
    # Activate virtual environment
    & "venv\Scripts\Activate.ps1"
    
    Write-Log "Starting PMS Intelligence Hub dashboard..." "SUCCESS"
    Write-Log "Dashboard will be available at: http://localhost:8501"
    Write-Log "Press Ctrl+C to stop the application"
    
    try {
        # Start Streamlit dashboard
        streamlit run src\dashboard\main_dashboard.py --server.port 8501 --server.address 0.0.0.0
    }
    catch {
        Write-Log "Error starting dashboard: $($_.Exception.Message)" "ERROR"
        return $false
    }
    
    return $true
}

# Function for Docker deployment
function Deploy-Docker {
    Write-Log "Starting Docker deployment..." "SUCCESS"
    
    # Check Docker installation
    try {
        $dockerVersion = docker --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Log "Docker is not installed or not running" "ERROR"
            Write-Log "Please install Docker Desktop from https://docker.com" "ERROR"
            return $false
        }
        Write-Log "Found Docker: $dockerVersion"
    }
    catch {
        Write-Log "Error checking Docker: $($_.Exception.Message)" "ERROR"
        return $false
    }
    
    # Check Docker Compose
    try {
        $composeVersion = docker-compose --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Log "Docker Compose is not available" "ERROR"
            return $false
        }
        Write-Log "Found Docker Compose: $composeVersion"
    }
    catch {
        Write-Log "Error checking Docker Compose: $($_.Exception.Message)" "ERROR"
        return $false
    }
    
    if (-not (Setup-Configuration)) {
        return $false
    }
    
    try {
        # Stop existing containers
        Write-Log "Stopping existing containers..."
        docker-compose down 2>&1 | Out-Null
        
        # Build and start containers
        Write-Log "Building and starting Docker containers..."
        docker-compose up --build -d
        
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to start Docker containers"
        }
        
        # Wait for services to start
        Write-Log "Waiting for services to start..."
        Start-Sleep -Seconds 15
        
        # Check container status
        Write-Log "Container status:"
        docker-compose ps
        
        Write-Log "Docker deployment completed successfully!" "SUCCESS"
        Write-Log ""
        Write-Log "Services are now available at:"
        Write-Log "  Dashboard:  http://localhost:8501"
        Write-Log "  API:        http://localhost:8000"
        Write-Log "  API Docs:   http://localhost:8000/docs"
        Write-Log "  Grafana:    http://localhost:3000 (admin/admin123)"
        Write-Log ""
        Write-Log "To view logs: docker-compose logs -f"
        Write-Log "To stop:      docker-compose down"
        
        return $true
    }
    catch {
        Write-Log "Error during Docker deployment: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Function to install as Windows service
function Install-Service {
    Write-Log "Installing PMS Intelligence Hub as Windows Service..." "SUCCESS"
    
    # Check if running as administrator
    if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-Log "Administrator privileges required to install Windows service" "ERROR"
        Write-Log "Please run PowerShell as Administrator and try again" "ERROR"
        return $false
    }
    
    if (-not (Test-Prerequisites)) {
        return $false
    }
    
    if (-not (Setup-VirtualEnvironment)) {
        return $false
    }
    
    if (-not (Setup-Configuration)) {
        return $false
    }
    
    try {
        # Install additional service dependencies
        & "venv\Scripts\Activate.ps1"
        pip install pywin32
        
        # Create service script
        $serviceScript = @"
import sys
import os
import time
import subprocess
import win32serviceutil
import win32service
import win32event

class PMSHubService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PMSIntelligenceHub"
    _svc_display_name_ = "PMS Intelligence Hub Dashboard"
    _svc_description_ = "Portfolio Management Services Intelligence Dashboard"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.process:
            self.process.terminate()
        win32event.SetEvent(self.hWaitStop)
        
    def SvcDoRun(self):
        # Change to application directory
        app_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(app_dir)
        
        # Activate virtual environment and start application
        venv_python = os.path.join(app_dir, "venv", "Scripts", "python.exe")
        streamlit_script = os.path.join(app_dir, "src", "dashboard", "main_dashboard.py")
        
        cmd = [venv_python, "-m", "streamlit", "run", streamlit_script, 
               "--server.port", "8501", "--server.address", "0.0.0.0", 
               "--server.headless", "true"]
        
        self.process = subprocess.Popen(cmd)
        
        # Wait for stop signal
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PMSHubService)
"@
        
        # Write service script
        $serviceScript | Out-File -FilePath "pms_hub_service.py" -Encoding UTF8
        
        # Install the service
        & "venv\Scripts\python.exe" "pms_hub_service.py" install
        
        Write-Log "Windows service installed successfully!" "SUCCESS"
        Write-Log "Service name: PMSIntelligenceHub"
        Write-Log ""
        Write-Log "To start the service: net start PMSIntelligenceHub"
        Write-Log "To stop the service:  net stop PMSIntelligenceHub"
        Write-Log "To remove service:    python pms_hub_service.py remove"
        
        # Ask if user wants to start the service now
        $response = Read-Host "Do you want to start the service now? (y/n)"
        if ($response -eq "y" -or $response -eq "Y") {
            Start-Service -Name "PMSIntelligenceHub"
            Write-Log "Service started successfully!" "SUCCESS"
            Write-Log "Dashboard is available at: http://localhost:8501"
        }
        
        return $true
    }
    catch {
        Write-Log "Error installing Windows service: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Function to show help
function Show-Help {
    Write-Host ""
    Write-Host "PMS Intelligence Hub - Windows PowerShell Deployment Script" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\deploy.ps1 [-Environment <env>] [-Force] [-Verbose] [-LogFile <path>]"
    Write-Host ""
    Write-Host "PARAMETERS:" -ForegroundColor Yellow
    Write-Host "  -Environment  Deployment environment (local, docker, service, help)"
    Write-Host "  -Force        Force recreation of virtual environment"
    Write-Host "  -Verbose      Enable verbose output"
    Write-Host "  -LogFile      Path to log file (default: deployment.log)"
    Write-Host ""
    Write-Host "ENVIRONMENTS:" -ForegroundColor Yellow
    Write-Host "  local         Local development setup (default)"
    Write-Host "  docker        Docker containerized deployment"
    Write-Host "  service       Install as Windows service"
    Write-Host "  help          Show this help message"
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "  .\deploy.ps1"
    Write-Host "  .\deploy.ps1 -Environment docker"
    Write-Host "  .\deploy.ps1 -Environment service -Force"
    Write-Host "  .\deploy.ps1 -Environment local -Verbose"
    Write-Host ""
    Write-Host "REQUIREMENTS:" -ForegroundColor Yellow
    Write-Host "  - Windows 10/11 or Windows Server 2016+"
    Write-Host "  - PowerShell 5.0+"
    Write-Host "  - Python 3.8+"
    Write-Host "  - Docker Desktop (for docker environment)"
    Write-Host "  - Administrator privileges (for service installation)"
    Write-Host ""
}

# Main execution
function Main {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " PMS Intelligence Hub - Windows Setup  " -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Initialize log file
    "PMS Intelligence Hub Deployment Log - $(Get-Date)" | Out-File -FilePath $LogFile
    
    Write-Log "Starting deployment with environment: $Environment"
    Write-Log "PowerShell version: $($PSVersionTable.PSVersion)"
    Write-Log "Windows version: $([System.Environment]::OSVersion.VersionString)"
    
    $success = $false
    
    switch ($Environment) {
        "local" {
            $success = Deploy-Local
        }
        "docker" {
            $success = Deploy-Docker
        }
        "service" {
            $success = Install-Service
        }
        "help" {
            Show-Help
            return
        }
        default {
            Write-Log "Invalid environment: $Environment" "ERROR"
            Show-Help
            return
        }
    }
    
    if ($success) {
        Write-Log "Deployment completed successfully!" "SUCCESS"
    } else {
        Write-Log "Deployment failed. Check the log file for details: $LogFile" "ERROR"
        exit 1
    }
}

# Execute main function
Main

