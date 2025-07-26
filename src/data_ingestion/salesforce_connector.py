"""
Salesforce CRM Data Connector for PMS Intelligence Hub
Handles both API and CSV-based data ingestion from Salesforce
"""

import os
import pandas as pd
import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from simple_salesforce import Salesforce
import csv
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SalesforceConfig:
    """Salesforce connection configuration"""
    username: str
    password: str
    security_token: str
    domain: str = 'login'  # 'login' for production, 'test' for sandbox
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    api_version: str = '58.0'

class SalesforceConnector:
    """
    Salesforce CRM connector supporting both API and CSV data ingestion
    """
    
    def __init__(self, config: SalesforceConfig):
        self.config = config
        self.sf_client = None
        self.session = None
        self.last_sync_time = None
        
    def connect_api(self) -> bool:
        """
        Establish connection to Salesforce API
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.sf_client = Salesforce(
                username=self.config.username,
                password=self.config.password,
                security_token=self.config.security_token,
                domain=self.config.domain,
                client_id=self.config.client_id,
                version=self.config.api_version
            )
            
            # Test connection
            user_info = self.sf_client.query("SELECT Id, Name FROM User LIMIT 1")
            logger.info(f"Successfully connected to Salesforce. User: {user_info['records'][0]['Name']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Salesforce API: {str(e)}")
            return False
    
    def get_clients_api(self, last_modified_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Fetch client data from Salesforce API
        
        Args:
            last_modified_date: Filter for incremental sync
            
        Returns:
            List of client records
        """
        if not self.sf_client:
            raise Exception("Salesforce API not connected. Call connect_api() first.")
        
        try:
            # Build SOQL query for client data
            soql = """
            SELECT 
                Id, Name, Type, PersonEmail, Phone, BillingStreet, BillingCity, 
                BillingState, BillingCountry, BillingPostalCode, CreatedDate,
                LastModifiedDate, Owner.Name, Owner.Email,
                Custom_PAN__c, Custom_Risk_Profile__c, Custom_Investment_Objective__c,
                Custom_KYC_Status__c, Custom_KYC_Expiry__c
            FROM Account 
            WHERE RecordType.Name = 'Client'
            """
            
            # Add incremental sync filter
            if last_modified_date:
                soql += f" AND LastModifiedDate >= {last_modified_date.isoformat()}"
            
            soql += " ORDER BY LastModifiedDate DESC"
            
            # Execute query
            result = self.sf_client.query_all(soql)
            clients = result['records']
            
            logger.info(f"Retrieved {len(clients)} client records from Salesforce API")
            
            # Transform data to standard format
            transformed_clients = []
            for client in clients:
                transformed_client = self._transform_client_data(client)
                transformed_clients.append(transformed_client)
            
            return transformed_clients
            
        except Exception as e:
            logger.error(f"Error fetching clients from Salesforce API: {str(e)}")
            raise
    
    def get_relationship_managers_api(self) -> List[Dict[str, Any]]:
        """
        Fetch relationship manager data from Salesforce API
        
        Returns:
            List of RM records
        """
        if not self.sf_client:
            raise Exception("Salesforce API not connected. Call connect_api() first.")
        
        try:
            soql = """
            SELECT 
                Id, Name, Email, Phone, Department, Title, ManagerId, Manager.Name,
                EmployeeNumber, IsActive, CreatedDate, LastModifiedDate
            FROM User 
            WHERE Profile.Name LIKE '%Relationship Manager%' 
            OR Profile.Name LIKE '%Portfolio Manager%'
            ORDER BY Name
            """
            
            result = self.sf_client.query_all(soql)
            rms = result['records']
            
            logger.info(f"Retrieved {len(rms)} RM records from Salesforce API")
            
            # Transform data
            transformed_rms = []
            for rm in rms:
                transformed_rm = self._transform_rm_data(rm)
                transformed_rms.append(transformed_rm)
            
            return transformed_rms
            
        except Exception as e:
            logger.error(f"Error fetching RMs from Salesforce API: {str(e)}")
            raise
    
    def get_aum_data_api(self, start_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Fetch AUM data from Salesforce API
        
        Args:
            start_date: Filter for data from specific date
            
        Returns:
            List of AUM records
        """
        if not self.sf_client:
            raise Exception("Salesforce API not connected. Call connect_api() first.")
        
        try:
            soql = """
            SELECT 
                Id, Account__c, Account__r.Name, AUM_Amount__c, AUM_Date__c,
                Portfolio_Type__c, Investment_Category__c, CreatedDate, LastModifiedDate
            FROM AUM_Record__c
            """
            
            if start_date:
                soql += f" WHERE AUM_Date__c >= {start_date.strftime('%Y-%m-%d')}"
            
            soql += " ORDER BY AUM_Date__c DESC"
            
            result = self.sf_client.query_all(soql)
            aum_records = result['records']
            
            logger.info(f"Retrieved {len(aum_records)} AUM records from Salesforce API")
            
            # Transform data
            transformed_aum = []
            for record in aum_records:
                transformed_record = self._transform_aum_data(record)
                transformed_aum.append(transformed_record)
            
            return transformed_aum
            
        except Exception as e:
            logger.error(f"Error fetching AUM data from Salesforce API: {str(e)}")
            raise
    
    def process_csv_file(self, file_path: str, data_type: str) -> List[Dict[str, Any]]:
        """
        Process CSV file exported from Salesforce
        
        Args:
            file_path: Path to CSV file
            data_type: Type of data ('clients', 'rms', 'aum')
            
        Returns:
            List of processed records
        """
        try:
            # Read CSV file
            df = pd.read_csv(file_path, encoding='utf-8')
            logger.info(f"Processing CSV file: {file_path} with {len(df)} records")
            
            # Process based on data type
            if data_type == 'clients':
                return self._process_clients_csv(df)
            elif data_type == 'rms':
                return self._process_rms_csv(df)
            elif data_type == 'aum':
                return self._process_aum_csv(df)
            else:
                raise ValueError(f"Unsupported data type: {data_type}")
                
        except Exception as e:
            logger.error(f"Error processing CSV file {file_path}: {str(e)}")
            raise
    
    def _process_clients_csv(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Process clients CSV data"""
        clients = []
        
        # Define column mappings (Salesforce field -> Standard field)
        column_mapping = {
            'Id': 'salesforce_id',
            'Name': 'client_name',
            'Type': 'client_type',
            'PersonEmail': 'email',
            'Phone': 'phone',
            'BillingStreet': 'address',
            'BillingCity': 'city',
            'BillingState': 'state',
            'BillingCountry': 'country',
            'BillingPostalCode': 'pincode',
            'CreatedDate': 'onboarding_date',
            'Owner.Name': 'rm_name',
            'Custom_PAN__c': 'pan_number',
            'Custom_Risk_Profile__c': 'risk_profile',
            'Custom_KYC_Status__c': 'kyc_status'
        }
        
        for _, row in df.iterrows():
            client = {}
            
            # Map columns
            for sf_field, std_field in column_mapping.items():
                if sf_field in df.columns:
                    client[std_field] = row[sf_field] if pd.notna(row[sf_field]) else None
            
            # Generate client_id if not present
            if 'client_id' not in client:
                client['client_id'] = f"CL_{client.get('salesforce_id', '')}"
            
            # Set defaults
            client['status'] = 'Active'
            client['country'] = client.get('country', 'India')
            
            clients.append(client)
        
        logger.info(f"Processed {len(clients)} client records from CSV")
        return clients
    
    def _process_rms_csv(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Process relationship managers CSV data"""
        rms = []
        
        column_mapping = {
            'Id': 'salesforce_id',
            'Name': 'rm_name',
            'Email': 'email',
            'Phone': 'phone',
            'Department': 'department',
            'Title': 'designation',
            'EmployeeNumber': 'employee_id',
            'IsActive': 'status'
        }
        
        for _, row in df.iterrows():
            rm = {}
            
            for sf_field, std_field in column_mapping.items():
                if sf_field in df.columns:
                    rm[std_field] = row[sf_field] if pd.notna(row[sf_field]) else None
            
            # Generate rm_id
            rm['rm_id'] = f"RM_{rm.get('salesforce_id', '')}"
            
            # Convert status
            if rm.get('status') == True or rm.get('status') == 'true':
                rm['status'] = 'Active'
            else:
                rm['status'] = 'Inactive'
            
            rms.append(rm)
        
        logger.info(f"Processed {len(rms)} RM records from CSV")
        return rms
    
    def _process_aum_csv(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Process AUM CSV data"""
        aum_records = []
        
        column_mapping = {
            'Account__c': 'client_id',
            'Account__r.Name': 'client_name',
            'AUM_Amount__c': 'aum_amount',
            'AUM_Date__c': 'aum_date',
            'Portfolio_Type__c': 'portfolio_type',
            'Investment_Category__c': 'investment_category'
        }
        
        for _, row in df.iterrows():
            record = {}
            
            for sf_field, std_field in column_mapping.items():
                if sf_field in df.columns:
                    record[std_field] = row[sf_field] if pd.notna(row[sf_field]) else None
            
            # Convert date format
            if record.get('aum_date'):
                try:
                    record['aum_date'] = pd.to_datetime(record['aum_date']).date()
                except:
                    record['aum_date'] = None
            
            # Convert amount to float
            if record.get('aum_amount'):
                try:
                    record['aum_amount'] = float(record['aum_amount'])
                except:
                    record['aum_amount'] = 0.0
            
            aum_records.append(record)
        
        logger.info(f"Processed {len(aum_records)} AUM records from CSV")
        return aum_records
    
    def _transform_client_data(self, sf_client: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Salesforce client data to standard format"""
        return {
            'client_id': f"CL_{sf_client['Id']}",
            'salesforce_id': sf_client['Id'],
            'client_name': sf_client.get('Name'),
            'client_type': sf_client.get('Type', 'Individual'),
            'email': sf_client.get('PersonEmail'),
            'phone': sf_client.get('Phone'),
            'address': sf_client.get('BillingStreet'),
            'city': sf_client.get('BillingCity'),
            'state': sf_client.get('BillingState'),
            'country': sf_client.get('BillingCountry', 'India'),
            'pincode': sf_client.get('BillingPostalCode'),
            'onboarding_date': self._parse_sf_date(sf_client.get('CreatedDate')),
            'rm_name': sf_client.get('Owner', {}).get('Name'),
            'rm_email': sf_client.get('Owner', {}).get('Email'),
            'pan_number': sf_client.get('Custom_PAN__c'),
            'risk_profile': sf_client.get('Custom_Risk_Profile__c'),
            'investment_objective': sf_client.get('Custom_Investment_Objective__c'),
            'kyc_status': sf_client.get('Custom_KYC_Status__c', 'Pending'),
            'kyc_expiry_date': self._parse_sf_date(sf_client.get('Custom_KYC_Expiry__c')),
            'status': 'Active',
            'salesforce_last_sync': datetime.utcnow()
        }
    
    def _transform_rm_data(self, sf_rm: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Salesforce RM data to standard format"""
        return {
            'rm_id': f"RM_{sf_rm['Id']}",
            'salesforce_id': sf_rm['Id'],
            'rm_name': sf_rm.get('Name'),
            'email': sf_rm.get('Email'),
            'phone': sf_rm.get('Phone'),
            'department': sf_rm.get('Department'),
            'designation': sf_rm.get('Title'),
            'employee_id': sf_rm.get('EmployeeNumber'),
            'manager_name': sf_rm.get('Manager', {}).get('Name'),
            'status': 'Active' if sf_rm.get('IsActive') else 'Inactive',
            'joining_date': self._parse_sf_date(sf_rm.get('CreatedDate'))
        }
    
    def _transform_aum_data(self, sf_aum: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Salesforce AUM data to standard format"""
        return {
            'client_id': f"CL_{sf_aum.get('Account__c')}",
            'client_name': sf_aum.get('Account__r', {}).get('Name'),
            'aum_amount': float(sf_aum.get('AUM_Amount__c', 0)),
            'aum_date': self._parse_sf_date(sf_aum.get('AUM_Date__c')),
            'portfolio_type': sf_aum.get('Portfolio_Type__c'),
            'investment_category': sf_aum.get('Investment_Category__c')
        }
    
    def _parse_sf_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse Salesforce date string to datetime object"""
        if not date_str:
            return None
        
        try:
            # Salesforce typically returns ISO format
            if 'T' in date_str:
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                return datetime.strptime(date_str, '%Y-%m-%d')
        except:
            return None
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test Salesforce connection and return status
        
        Returns:
            Dictionary with connection status and details
        """
        try:
            if self.connect_api():
                # Get basic org info
                org_info = self.sf_client.query("SELECT Id, Name FROM Organization LIMIT 1")
                user_info = self.sf_client.query("SELECT Id, Name, Email FROM User WHERE Id = UserInfo.getUserId()")
                
                return {
                    'status': 'success',
                    'connected': True,
                    'org_name': org_info['records'][0]['Name'],
                    'user_name': user_info['records'][0]['Name'],
                    'user_email': user_info['records'][0]['Email'],
                    'api_version': self.config.api_version,
                    'connection_time': datetime.utcnow().isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'connected': False,
                    'message': 'Failed to connect to Salesforce API'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'connected': False,
                'message': str(e)
            }

# Utility functions
def create_salesforce_connector(
    username: str,
    password: str,
    security_token: str,
    domain: str = 'login'
) -> SalesforceConnector:
    """
    Create and return a configured Salesforce connector
    
    Args:
        username: Salesforce username
        password: Salesforce password
        security_token: Salesforce security token
        domain: Salesforce domain ('login' or 'test')
        
    Returns:
        Configured SalesforceConnector instance
    """
    config = SalesforceConfig(
        username=username,
        password=password,
        security_token=security_token,
        domain=domain
    )
    
    return SalesforceConnector(config)

def load_config_from_env() -> SalesforceConfig:
    """
    Load Salesforce configuration from environment variables
    
    Returns:
        SalesforceConfig object
    """
    return SalesforceConfig(
        username=os.getenv('SALESFORCE_USERNAME'),
        password=os.getenv('SALESFORCE_PASSWORD'),
        security_token=os.getenv('SALESFORCE_SECURITY_TOKEN'),
        domain=os.getenv('SALESFORCE_DOMAIN', 'login'),
        client_id=os.getenv('SALESFORCE_CLIENT_ID'),
        client_secret=os.getenv('SALESFORCE_CLIENT_SECRET'),
        api_version=os.getenv('SALESFORCE_API_VERSION', '58.0')
    )

