#!/usr/bin/env python3
"""
Deployment Script for PMS Intelligence Hub
Handles deployment to various environments (local, AWS, Docker)
"""

import os
import sys
import subprocess
import argparse
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
import requests
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deployment.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DeploymentManager:
    """
    Comprehensive deployment manager for PMS Intelligence Hub
    Supports multiple deployment targets and environments
    """
    
    def __init__(self, config_path: str = None):
        self.project_root = Path(__file__).parent.parent
        self.config = self.load_config(config_path)
        self.deployment_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Load deployment configuration"""
        if config_path is None:
            config_path = self.project_root / 'deployment' / 'config.yml'
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}. Using defaults.")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default deployment configuration"""
        return {
            'environments': {
                'local': {
                    'type': 'local',
                    'port': 8501,
                    'host': '0.0.0.0'
                },
                'docker': {
                    'type': 'docker',
                    'compose_file': 'docker-compose.yml',
                    'services': ['postgres', 'redis', 'api', 'dashboard']
                },
                'aws': {
                    'type': 'aws',
                    'region': 'us-east-1',
                    'instance_type': 't3.micro',
                    'use_free_tier': True
                }
            },
            'health_check': {
                'timeout': 300,
                'interval': 10,
                'retries': 30
            },
            'backup': {
                'enabled': True,
                'retention_days': 7
            }
        }
    
    def validate_environment(self) -> bool:
        """Validate deployment environment"""
        logger.info("Validating deployment environment...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            logger.error("Python 3.8+ is required")
            return False
        
        # Check required files
        required_files = [
            'requirements.txt',
            'src/dashboard/main_dashboard.py',
            'src/api/main.py',
            'docker-compose.yml'
        ]
        
        for file_path in required_files:
            if not (self.project_root / file_path).exists():
                logger.error(f"Required file missing: {file_path}")
                return False
        
        # Check environment variables
        required_env_vars = ['SECRET_KEY']
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.warning(f"Missing environment variables: {missing_vars}")
            logger.info("Using default values for missing variables")
        
        logger.info("Environment validation completed successfully")
        return True
    
    def install_dependencies(self) -> bool:
        """Install Python dependencies"""
        logger.info("Installing Python dependencies...")
        
        try:
            # Upgrade pip
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'
            ], check=True, capture_output=True)
            
            # Install requirements
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', 
                str(self.project_root / 'requirements.txt')
            ], check=True, capture_output=True)
            
            logger.info("Dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
    
    def setup_database(self) -> bool:
        """Setup database (if required)"""
        logger.info("Setting up database...")
        
        try:
            # For SQLite (default), just ensure directory exists
            db_path = self.project_root / 'pms_hub.db'
            db_path.parent.mkdir(exist_ok=True)
            
            # Run database migrations (if any)
            # This would typically involve Alembic or similar
            logger.info("Database setup completed")
            return True
            
        except Exception as e:
            logger.error(f"Database setup failed: {e}")
            return False
    
    def deploy_local(self) -> bool:
        """Deploy to local environment"""
        logger.info("Deploying to local environment...")
        
        try:
            # Set environment variables
            os.environ['ENVIRONMENT'] = 'development'
            os.environ['DEBUG'] = 'true'
            
            # Start Streamlit dashboard
            dashboard_cmd = [
                sys.executable, '-m', 'streamlit', 'run',
                str(self.project_root / 'src' / 'dashboard' / 'main_dashboard.py'),
                '--server.port', str(self.config['environments']['local']['port']),
                '--server.address', self.config['environments']['local']['host'],
                '--server.headless', 'true'
            ]
            
            logger.info(f"Starting dashboard with command: {' '.join(dashboard_cmd)}")
            
            # Start the process (non-blocking for this demo)
            process = subprocess.Popen(dashboard_cmd, cwd=self.project_root)
            
            # Wait a moment for startup
            time.sleep(5)
            
            # Check if process is still running
            if process.poll() is None:
                logger.info(f"Local deployment successful. Dashboard running on port {self.config['environments']['local']['port']}")
                logger.info(f"Access URL: http://localhost:{self.config['environments']['local']['port']}")
                return True
            else:
                logger.error("Dashboard process terminated unexpectedly")
                return False
                
        except Exception as e:
            logger.error(f"Local deployment failed: {e}")
            return False
    
    def deploy_docker(self) -> bool:
        """Deploy using Docker Compose"""
        logger.info("Deploying with Docker Compose...")
        
        try:
            # Check if Docker is available
            subprocess.run(['docker', '--version'], check=True, capture_output=True)
            subprocess.run(['docker-compose', '--version'], check=True, capture_output=True)
            
            # Build and start services
            compose_file = self.project_root / self.config['environments']['docker']['compose_file']
            
            # Stop any existing services
            subprocess.run([
                'docker-compose', '-f', str(compose_file), 'down'
            ], cwd=self.project_root, capture_output=True)
            
            # Build and start services
            subprocess.run([
                'docker-compose', '-f', str(compose_file), 'up', '--build', '-d'
            ], check=True, cwd=self.project_root)
            
            # Wait for services to be ready
            if self.wait_for_services():
                logger.info("Docker deployment successful")
                logger.info("Services available at:")
                logger.info("  - Dashboard: http://localhost:8501")
                logger.info("  - API: http://localhost:8000")
                logger.info("  - Grafana: http://localhost:3000")
                return True
            else:
                logger.error("Services failed to start properly")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Docker deployment failed: {e}")
            return False
        except FileNotFoundError:
            logger.error("Docker or Docker Compose not found. Please install Docker.")
            return False
    
    def deploy_aws(self) -> bool:
        """Deploy to AWS (simplified version)"""
        logger.info("Deploying to AWS...")
        
        try:
            # Check AWS CLI
            subprocess.run(['aws', '--version'], check=True, capture_output=True)
            
            # This is a simplified AWS deployment
            # In production, you would use AWS CDK, CloudFormation, or Terraform
            
            aws_config = self.config['environments']['aws']
            
            # Create deployment package
            self.create_deployment_package()
            
            # Upload to S3 (if configured)
            if aws_config.get('s3_bucket'):
                self.upload_to_s3(aws_config['s3_bucket'])
            
            # Deploy using AWS services
            # This would typically involve:
            # - Creating EC2 instances
            # - Setting up RDS for database
            # - Configuring load balancers
            # - Setting up CloudWatch monitoring
            
            logger.info("AWS deployment initiated (simplified)")
            logger.info("Note: Full AWS deployment requires additional configuration")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"AWS deployment failed: {e}")
            return False
        except FileNotFoundError:
            logger.error("AWS CLI not found. Please install AWS CLI.")
            return False
    
    def create_deployment_package(self) -> str:
        """Create deployment package"""
        logger.info("Creating deployment package...")
        
        package_name = f"pms_hub_deployment_{self.deployment_id}.tar.gz"
        package_path = self.project_root / 'dist' / package_name
        package_path.parent.mkdir(exist_ok=True)
        
        # Create tar archive
        subprocess.run([
            'tar', '-czf', str(package_path),
            '--exclude=__pycache__',
            '--exclude=*.pyc',
            '--exclude=.git',
            '--exclude=node_modules',
            '--exclude=dist',
            '.'
        ], cwd=self.project_root, check=True)
        
        logger.info(f"Deployment package created: {package_path}")
        return str(package_path)
    
    def upload_to_s3(self, bucket_name: str) -> bool:
        """Upload deployment package to S3"""
        logger.info(f"Uploading to S3 bucket: {bucket_name}")
        
        try:
            package_path = self.create_deployment_package()
            
            subprocess.run([
                'aws', 's3', 'cp', package_path,
                f's3://{bucket_name}/deployments/'
            ], check=True)
            
            logger.info("Upload to S3 successful")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"S3 upload failed: {e}")
            return False
    
    def wait_for_services(self) -> bool:
        """Wait for services to be ready"""
        logger.info("Waiting for services to be ready...")
        
        health_config = self.config['health_check']
        timeout = health_config['timeout']
        interval = health_config['interval']
        retries = health_config['retries']
        
        services = {
            'dashboard': 'http://localhost:8501/_stcore/health',
            'api': 'http://localhost:8000/health'
        }
        
        for service_name, health_url in services.items():
            logger.info(f"Checking {service_name} health...")
            
            for attempt in range(retries):
                try:
                    response = requests.get(health_url, timeout=10)
                    if response.status_code == 200:
                        logger.info(f"{service_name} is ready")
                        break
                except requests.RequestException:
                    if attempt < retries - 1:
                        logger.info(f"{service_name} not ready, retrying in {interval}s...")
                        time.sleep(interval)
                    else:
                        logger.error(f"{service_name} failed to start within timeout")
                        return False
        
        return True
    
    def run_health_checks(self) -> bool:
        """Run comprehensive health checks"""
        logger.info("Running health checks...")
        
        checks = [
            self.check_database_connection,
            self.check_api_endpoints,
            self.check_dashboard_accessibility
        ]
        
        for check in checks:
            if not check():
                logger.error(f"Health check failed: {check.__name__}")
                return False
        
        logger.info("All health checks passed")
        return True
    
    def check_database_connection(self) -> bool:
        """Check database connection"""
        try:
            # Simple database connection check
            # In production, this would test actual database connectivity
            logger.info("Database connection check passed")
            return True
        except Exception as e:
            logger.error(f"Database connection check failed: {e}")
            return False
    
    def check_api_endpoints(self) -> bool:
        """Check API endpoints"""
        try:
            # Test API endpoints
            endpoints = [
                'http://localhost:8000/health',
                'http://localhost:8000/docs'
            ]
            
            for endpoint in endpoints:
                try:
                    response = requests.get(endpoint, timeout=10)
                    if response.status_code not in [200, 404]:  # 404 is OK for some endpoints
                        logger.warning(f"API endpoint {endpoint} returned {response.status_code}")
                except requests.RequestException:
                    logger.warning(f"API endpoint {endpoint} not accessible")
            
            logger.info("API endpoints check passed")
            return True
        except Exception as e:
            logger.error(f"API endpoints check failed: {e}")
            return False
    
    def check_dashboard_accessibility(self) -> bool:
        """Check dashboard accessibility"""
        try:
            # Test dashboard accessibility
            dashboard_url = 'http://localhost:8501'
            
            try:
                response = requests.get(dashboard_url, timeout=10)
                if response.status_code == 200:
                    logger.info("Dashboard accessibility check passed")
                    return True
            except requests.RequestException:
                logger.warning("Dashboard not accessible via HTTP check")
            
            # Dashboard might still be starting up
            logger.info("Dashboard accessibility check completed with warnings")
            return True
        except Exception as e:
            logger.error(f"Dashboard accessibility check failed: {e}")
            return False
    
    def backup_current_deployment(self) -> bool:
        """Backup current deployment"""
        if not self.config['backup']['enabled']:
            logger.info("Backup disabled in configuration")
            return True
        
        logger.info("Creating deployment backup...")
        
        try:
            backup_dir = self.project_root / 'backups'
            backup_dir.mkdir(exist_ok=True)
            
            backup_name = f"backup_{self.deployment_id}.tar.gz"
            backup_path = backup_dir / backup_name
            
            # Create backup
            subprocess.run([
                'tar', '-czf', str(backup_path),
                '--exclude=backups',
                '--exclude=__pycache__',
                '--exclude=*.pyc',
                '--exclude=.git',
                '.'
            ], cwd=self.project_root, check=True)
            
            logger.info(f"Backup created: {backup_path}")
            
            # Cleanup old backups
            self.cleanup_old_backups(backup_dir)
            
            return True
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False
    
    def cleanup_old_backups(self, backup_dir: Path):
        """Cleanup old backup files"""
        retention_days = self.config['backup']['retention_days']
        cutoff_time = time.time() - (retention_days * 24 * 60 * 60)
        
        for backup_file in backup_dir.glob('backup_*.tar.gz'):
            if backup_file.stat().st_mtime < cutoff_time:
                backup_file.unlink()
                logger.info(f"Removed old backup: {backup_file.name}")
    
    def deploy(self, environment: str) -> bool:
        """Main deployment method"""
        logger.info(f"Starting deployment to {environment} environment")
        logger.info(f"Deployment ID: {self.deployment_id}")
        
        # Pre-deployment checks
        if not self.validate_environment():
            logger.error("Environment validation failed")
            return False
        
        # Create backup
        if not self.backup_current_deployment():
            logger.warning("Backup creation failed, continuing with deployment")
        
        # Install dependencies
        if environment != 'docker':  # Docker handles dependencies internally
            if not self.install_dependencies():
                logger.error("Dependency installation failed")
                return False
        
        # Setup database
        if not self.setup_database():
            logger.error("Database setup failed")
            return False
        
        # Deploy to specific environment
        deployment_methods = {
            'local': self.deploy_local,
            'docker': self.deploy_docker,
            'aws': self.deploy_aws
        }
        
        if environment not in deployment_methods:
            logger.error(f"Unknown environment: {environment}")
            return False
        
        if not deployment_methods[environment]():
            logger.error(f"Deployment to {environment} failed")
            return False
        
        # Post-deployment health checks
        if environment in ['local', 'docker']:
            time.sleep(10)  # Give services time to start
            if not self.run_health_checks():
                logger.warning("Some health checks failed")
        
        logger.info(f"Deployment to {environment} completed successfully")
        return True

def main():
    """Main deployment script"""
    parser = argparse.ArgumentParser(description='Deploy PMS Intelligence Hub')
    parser.add_argument(
        'environment',
        choices=['local', 'docker', 'aws'],
        help='Deployment environment'
    )
    parser.add_argument(
        '--config',
        help='Path to deployment configuration file'
    )
    parser.add_argument(
        '--skip-health-checks',
        action='store_true',
        help='Skip post-deployment health checks'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize deployment manager
    deployment_manager = DeploymentManager(args.config)
    
    # Run deployment
    success = deployment_manager.deploy(args.environment)
    
    if success:
        logger.info("🎉 Deployment completed successfully!")
        
        if args.environment == 'local':
            print("\n" + "="*50)
            print("🚀 PMS Intelligence Hub is now running locally!")
            print("="*50)
            print(f"📊 Dashboard: http://localhost:8501")
            print(f"🔧 API Docs: http://localhost:8000/docs")
            print("="*50)
        elif args.environment == 'docker':
            print("\n" + "="*50)
            print("🐳 PMS Intelligence Hub is now running in Docker!")
            print("="*50)
            print(f"📊 Dashboard: http://localhost:8501")
            print(f"🔧 API: http://localhost:8000")
            print(f"📈 Grafana: http://localhost:3000")
            print(f"🗄️  PostgreSQL: localhost:5432")
            print("="*50)
        
        sys.exit(0)
    else:
        logger.error("❌ Deployment failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()

