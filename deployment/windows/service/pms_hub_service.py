"""
PMS Intelligence Hub - Windows Service Implementation
Allows running the dashboard as a Windows service for production deployment
"""

import sys
import os
import time
import subprocess
import logging
import threading
from pathlib import Path

try:
    import win32serviceutil
    import win32service
    import win32event
    import servicemanager
except ImportError:
    print("ERROR: pywin32 is required for Windows service functionality")
    print("Install with: pip install pywin32")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pms_service.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PMSIntelligenceHubService(win32serviceutil.ServiceFramework):
    """
    Windows Service for PMS Intelligence Hub
    Manages the Streamlit dashboard as a Windows service
    """
    
    # Service configuration
    _svc_name_ = "PMSIntelligenceHub"
    _svc_display_name_ = "PMS Intelligence Hub Dashboard"
    _svc_description_ = "Portfolio Management Services Intelligence Dashboard and Analytics Platform"
    
    # Service startup type
    _svc_start_type_ = win32service.SERVICE_AUTO_START
    
    def __init__(self, args):
        """Initialize the service"""
        win32serviceutil.ServiceFramework.__init__(self, args)
        
        # Create stop event
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        
        # Service state
        self.is_running = False
        self.dashboard_process = None
        self.api_process = None
        
        # Application paths
        self.app_dir = Path(__file__).parent.parent.parent.parent
        self.venv_python = self.app_dir / "venv" / "Scripts" / "python.exe"
        self.dashboard_script = self.app_dir / "src" / "dashboard" / "main_dashboard.py"
        self.api_script = self.app_dir / "src" / "api" / "main.py"
        
        # Ensure log directory exists
        log_dir = self.app_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # Configure service logging
        self.setup_logging()
        
        logger.info(f"Service initialized. App directory: {self.app_dir}")
    
    def setup_logging(self):
        """Setup service-specific logging"""
        log_file = self.app_dir / "logs" / "pms_service.log"
        
        # Create file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(file_handler)
    
    def SvcStop(self):
        """Stop the service"""
        logger.info("Service stop requested")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        
        # Set stop flag
        self.is_running = False
        
        # Stop processes
        self.stop_processes()
        
        # Signal stop event
        win32event.SetEvent(self.hWaitStop)
        
        logger.info("Service stopped")
    
    def SvcDoRun(self):
        """Main service execution"""
        logger.info("Starting PMS Intelligence Hub Service")
        
        # Log service start
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        try:
            # Change to application directory
            os.chdir(self.app_dir)
            logger.info(f"Changed to directory: {self.app_dir}")
            
            # Validate environment
            if not self.validate_environment():
                logger.error("Environment validation failed")
                return
            
            # Set running flag
            self.is_running = True
            
            # Start application components
            self.start_dashboard()
            
            # Optional: Start API server
            # self.start_api()
            
            # Monitor processes
            self.monitor_processes()
            
            # Wait for stop signal
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
            
        except Exception as e:
            logger.error(f"Service execution error: {e}")
            servicemanager.LogErrorMsg(f"Service error: {e}")
        finally:
            self.cleanup()
    
    def validate_environment(self):
        """Validate the service environment"""
        logger.info("Validating service environment")
        
        # Check Python executable
        if not self.venv_python.exists():
            logger.error(f"Python executable not found: {self.venv_python}")
            return False
        
        # Check dashboard script
        if not self.dashboard_script.exists():
            logger.error(f"Dashboard script not found: {self.dashboard_script}")
            return False
        
        # Check .env file
        env_file = self.app_dir / ".env"
        if not env_file.exists():
            logger.warning(".env file not found, using defaults")
        
        # Check required directories
        required_dirs = ["cache", "logs", "exports", "uploads"]
        for dir_name in required_dirs:
            dir_path = self.app_dir / dir_name
            if not dir_path.exists():
                dir_path.mkdir(exist_ok=True)
                logger.info(f"Created directory: {dir_path}")
        
        logger.info("Environment validation completed")
        return True
    
    def start_dashboard(self):
        """Start the Streamlit dashboard"""
        logger.info("Starting Streamlit dashboard")
        
        try:
            # Prepare command
            cmd = [
                str(self.venv_python),
                "-m", "streamlit", "run",
                str(self.dashboard_script),
                "--server.port", "8501",
                "--server.address", "0.0.0.0",
                "--server.headless", "true",
                "--server.runOnSave", "false",
                "--browser.gatherUsageStats", "false"
            ]
            
            logger.info(f"Dashboard command: {' '.join(cmd)}")
            
            # Start process
            self.dashboard_process = subprocess.Popen(
                cmd,
                cwd=self.app_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            logger.info(f"Dashboard started with PID: {self.dashboard_process.pid}")
            
            # Give it time to start
            time.sleep(5)
            
            # Check if process is still running
            if self.dashboard_process.poll() is None:
                logger.info("Dashboard started successfully")
                return True
            else:
                logger.error("Dashboard process terminated unexpectedly")
                return False
                
        except Exception as e:
            logger.error(f"Error starting dashboard: {e}")
            return False
    
    def start_api(self):
        """Start the FastAPI server (optional)"""
        logger.info("Starting FastAPI server")
        
        try:
            # Prepare command
            cmd = [
                str(self.venv_python),
                "-m", "uvicorn",
                "src.api.main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--workers", "1"
            ]
            
            logger.info(f"API command: {' '.join(cmd)}")
            
            # Start process
            self.api_process = subprocess.Popen(
                cmd,
                cwd=self.app_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            logger.info(f"API started with PID: {self.api_process.pid}")
            return True
            
        except Exception as e:
            logger.error(f"Error starting API: {e}")
            return False
    
    def monitor_processes(self):
        """Monitor running processes and restart if needed"""
        logger.info("Starting process monitoring")
        
        def monitor_loop():
            while self.is_running:
                try:
                    # Check dashboard process
                    if self.dashboard_process and self.dashboard_process.poll() is not None:
                        logger.warning("Dashboard process died, attempting restart")
                        self.start_dashboard()
                    
                    # Check API process (if running)
                    if self.api_process and self.api_process.poll() is not None:
                        logger.warning("API process died, attempting restart")
                        self.start_api()
                    
                    # Wait before next check
                    time.sleep(30)
                    
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {e}")
                    time.sleep(60)
        
        # Start monitoring in separate thread
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def stop_processes(self):
        """Stop all running processes"""
        logger.info("Stopping application processes")
        
        # Stop dashboard process
        if self.dashboard_process:
            try:
                self.dashboard_process.terminate()
                self.dashboard_process.wait(timeout=10)
                logger.info("Dashboard process stopped")
            except subprocess.TimeoutExpired:
                logger.warning("Dashboard process did not stop gracefully, killing")
                self.dashboard_process.kill()
            except Exception as e:
                logger.error(f"Error stopping dashboard: {e}")
        
        # Stop API process
        if self.api_process:
            try:
                self.api_process.terminate()
                self.api_process.wait(timeout=10)
                logger.info("API process stopped")
            except subprocess.TimeoutExpired:
                logger.warning("API process did not stop gracefully, killing")
                self.api_process.kill()
            except Exception as e:
                logger.error(f"Error stopping API: {e}")
    
    def cleanup(self):
        """Cleanup resources"""
        logger.info("Performing service cleanup")
        
        # Stop processes
        self.stop_processes()
        
        # Log service stop
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STOPPED,
            (self._svc_name_, '')
        )

def install_service():
    """Install the Windows service"""
    try:
        win32serviceutil.InstallService(
            PMSIntelligenceHubService,
            PMSIntelligenceHubService._svc_name_,
            PMSIntelligenceHubService._svc_display_name_,
            startType=win32service.SERVICE_AUTO_START,
            description=PMSIntelligenceHubService._svc_description_
        )
        print(f"Service '{PMSIntelligenceHubService._svc_display_name_}' installed successfully")
        print(f"Service name: {PMSIntelligenceHubService._svc_name_}")
        print("")
        print("To start the service:")
        print(f"  net start {PMSIntelligenceHubService._svc_name_}")
        print("  or")
        print(f"  sc start {PMSIntelligenceHubService._svc_name_}")
        print("")
        print("To stop the service:")
        print(f"  net stop {PMSIntelligenceHubService._svc_name_}")
        print("")
        print("To remove the service:")
        print(f"  python {__file__} remove")
        
    except Exception as e:
        print(f"Error installing service: {e}")
        return False
    
    return True

def remove_service():
    """Remove the Windows service"""
    try:
        win32serviceutil.RemoveService(PMSIntelligenceHubService._svc_name_)
        print(f"Service '{PMSIntelligenceHubService._svc_display_name_}' removed successfully")
    except Exception as e:
        print(f"Error removing service: {e}")
        return False
    
    return True

def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        # No arguments - run as service
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PMSIntelligenceHubService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        # Handle command line arguments
        command = sys.argv[1].lower()
        
        if command == "install":
            install_service()
        elif command == "remove":
            remove_service()
        elif command == "start":
            win32serviceutil.StartService(PMSIntelligenceHubService._svc_name_)
            print("Service started")
        elif command == "stop":
            win32serviceutil.StopService(PMSIntelligenceHubService._svc_name_)
            print("Service stopped")
        elif command == "restart":
            win32serviceutil.RestartService(PMSIntelligenceHubService._svc_name_)
            print("Service restarted")
        elif command == "debug":
            # Run in debug mode (console)
            service = PMSIntelligenceHubService([])
            service.SvcDoRun()
        else:
            # Use standard service utility handling
            win32serviceutil.HandleCommandLine(PMSIntelligenceHubService)

if __name__ == '__main__':
    main()

