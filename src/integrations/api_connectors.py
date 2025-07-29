"""
Optimized API Integration Module for PMS Intelligence Hub
Efficient connectors for Salesforce and Wealth Spectrum APIs
Author: Vulnuris Development Team
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import streamlit as st
from dataclasses import dataclass
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class APIConfig:
    """Configuration class for API connections"""
    base_url: str
    api_key: str
    api_secret: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    rate_limit_per_minute: int = 60

class OptimizedAPIConnector:
    """
    Base class for optimized API connections with caching and rate limiting
    """
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PMS-Intelligence-Hub/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        self.last_request_time = 0
        self.request_count = 0
        self.rate_limit_window = 60  # seconds
        
    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        
        # Reset counter if window has passed
        if current_time - self.last_request_time > self.rate_limit_window:
            self.request_count = 0
            self.last_request_time = current_time
        
        # Check if we've hit the rate limit
        if self.request_count >= self.config.rate_limit_per_minute:
            sleep_time = self.rate_limit_window - (current_time - self.last_request_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
                self.request_count = 0
                self.last_request_time = time.time()
        
        self.request_count += 1
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make optimized HTTP request with retry logic"""
        self._rate_limit()
        
        url = f"{self.config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        for attempt in range(self.config.max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.config.timeout,
                    **kwargs
                )
                
                if response.status_code == 429:  # Rate limited
                    wait_time = int(response.headers.get('Retry-After', 60))
                    time.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                if attempt == self.config.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
        
        raise requests.exceptions.RequestException("Max retries exceeded")
    
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def _cached_request(_self, method: str, endpoint: str, cache_key: str, **kwargs) -> Dict:
        """Make cached request to avoid redundant API calls"""
        response = _self._make_request(method, endpoint, **kwargs)
        return response.json()

class SalesforceConnector(OptimizedAPIConnector):
    """
    Optimized Salesforce API connector with OAuth2 and bulk operations
    """
    
    def __init__(self, config: APIConfig, client_id: str, client_secret: str):
        super().__init__(config)
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = None
        
    def authenticate(self) -> bool:
        """Authenticate with Salesforce using OAuth2"""
        try:
            auth_url = f"{self.config.base_url}/services/oauth2/token"
            
            auth_data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            
            response = requests.post(auth_url, data=auth_data, timeout=self.config.timeout)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.token_expires_at = datetime.now() + timedelta(seconds=token_data.get('expires_in', 3600))
            
            # Update session headers
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })
            
            logger.info("Successfully authenticated with Salesforce")
            return True
            
        except Exception as e:
            logger.error(f"Salesforce authentication failed: {e}")
            return False
    
    def _ensure_authenticated(self):
        """Ensure we have a valid access token"""
        if not self.access_token or datetime.now() >= self.token_expires_at:
            if not self.authenticate():
                raise Exception("Failed to authenticate with Salesforce")
    
    def get_clients(self, limit: int = 1000, offset: int = 0) -> pd.DataFrame:
        """
        Fetch client data from Salesforce with optimized SOQL query
        """
        self._ensure_authenticated()
        
        # Optimized SOQL query
        soql_query = f"""
        SELECT Id, Name, Email, Phone, Account.Name, Account.Type, 
               CreatedDate, LastModifiedDate, Account.AnnualRevenue
        FROM Contact 
        WHERE Account.Type = 'Client'
        ORDER BY LastModifiedDate DESC
        LIMIT {limit} OFFSET {offset}
        """
        
        cache_key = hashlib.md5(f"clients_{limit}_{offset}".encode()).hexdigest()
        
        try:
            data = self._cached_request(
                'GET',
                f'services/data/v58.0/query/?q={soql_query}',
                cache_key
            )
            
            if 'records' in data:
                # Flatten nested account data
                records = []
                for record in data['records']:
                    flat_record = {
                        'client_id': record['Id'],
                        'client_name': record['Name'],
                        'email': record.get('Email', ''),
                        'phone': record.get('Phone', ''),
                        'account_name': record.get('Account', {}).get('Name', ''),
                        'account_type': record.get('Account', {}).get('Type', ''),
                        'annual_revenue': record.get('Account', {}).get('AnnualRevenue', 0),
                        'created_date': record.get('CreatedDate', ''),
                        'last_modified': record.get('LastModifiedDate', '')
                    }
                    records.append(flat_record)
                
                return pd.DataFrame(records)
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Failed to fetch clients from Salesforce: {e}")
            return pd.DataFrame()
    
    def get_opportunities(self, client_ids: List[str] = None) -> pd.DataFrame:
        """
        Fetch opportunity data from Salesforce
        """
        self._ensure_authenticated()
        
        where_clause = ""
        if client_ids:
            client_ids_str = "','".join(client_ids)
            where_clause = f"WHERE AccountId IN ('{client_ids_str}')"
        
        soql_query = f"""
        SELECT Id, Name, AccountId, Amount, StageName, CloseDate, 
               Probability, CreatedDate, LastModifiedDate
        FROM Opportunity 
        {where_clause}
        ORDER BY LastModifiedDate DESC
        LIMIT 1000
        """
        
        cache_key = hashlib.md5(f"opportunities_{len(client_ids) if client_ids else 0}".encode()).hexdigest()
        
        try:
            data = self._cached_request(
                'GET',
                f'services/data/v58.0/query/?q={soql_query}',
                cache_key
            )
            
            if 'records' in data:
                return pd.DataFrame(data['records'])
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Failed to fetch opportunities from Salesforce: {e}")
            return pd.DataFrame()

class WealthSpectrumConnector(OptimizedAPIConnector):
    """
    Optimized Wealth Spectrum API connector for portfolio data
    """
    
    def __init__(self, config: APIConfig):
        super().__init__(config)
        self.session.headers.update({
            'X-API-Key': config.api_key
        })
    
    def get_portfolios(self, client_ids: List[str] = None) -> pd.DataFrame:
        """
        Fetch portfolio data with optimized batch processing
        """
        try:
            params = {}
            if client_ids:
                params['client_ids'] = ','.join(client_ids)
            
            cache_key = hashlib.md5(f"portfolios_{len(client_ids) if client_ids else 0}".encode()).hexdigest()
            
            data = self._cached_request(
                'GET',
                'api/v1/portfolios',
                cache_key,
                params=params
            )
            
            if 'portfolios' in data:
                return pd.DataFrame(data['portfolios'])
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Failed to fetch portfolios from Wealth Spectrum: {e}")
            return pd.DataFrame()
    
    def get_holdings(self, portfolio_ids: List[str]) -> pd.DataFrame:
        """
        Fetch holdings data with concurrent requests for performance
        """
        if not portfolio_ids:
            return pd.DataFrame()
        
        all_holdings = []
        
        # Use ThreadPoolExecutor for concurrent API calls
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_portfolio = {
                executor.submit(self._get_portfolio_holdings, portfolio_id): portfolio_id
                for portfolio_id in portfolio_ids
            }
            
            for future in as_completed(future_to_portfolio):
                portfolio_id = future_to_portfolio[future]
                try:
                    holdings = future.result()
                    if not holdings.empty:
                        holdings['portfolio_id'] = portfolio_id
                        all_holdings.append(holdings)
                except Exception as e:
                    logger.error(f"Failed to fetch holdings for portfolio {portfolio_id}: {e}")
        
        if all_holdings:
            return pd.concat(all_holdings, ignore_index=True)
        
        return pd.DataFrame()
    
    def _get_portfolio_holdings(self, portfolio_id: str) -> pd.DataFrame:
        """
        Fetch holdings for a single portfolio
        """
        cache_key = hashlib.md5(f"holdings_{portfolio_id}".encode()).hexdigest()
        
        try:
            data = self._cached_request(
                'GET',
                f'api/v1/portfolios/{portfolio_id}/holdings',
                cache_key
            )
            
            if 'holdings' in data:
                return pd.DataFrame(data['holdings'])
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Failed to fetch holdings for portfolio {portfolio_id}: {e}")
            return pd.DataFrame()
    
    def get_performance_data(self, portfolio_ids: List[str], 
                           start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        Fetch performance data with date range optimization
        """
        if not portfolio_ids:
            return pd.DataFrame()
        
        params = {
            'portfolio_ids': ','.join(portfolio_ids)
        }
        
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        
        cache_key = hashlib.md5(
            f"performance_{len(portfolio_ids)}_{start_date}_{end_date}".encode()
        ).hexdigest()
        
        try:
            data = self._cached_request(
                'GET',
                'api/v1/performance',
                cache_key,
                params=params
            )
            
            if 'performance_data' in data:
                return pd.DataFrame(data['performance_data'])
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Failed to fetch performance data from Wealth Spectrum: {e}")
            return pd.DataFrame()

class IntegratedDataManager:
    """
    Optimized data manager that combines Salesforce and Wealth Spectrum data
    """
    
    def __init__(self, salesforce_connector: SalesforceConnector, 
                 wealth_spectrum_connector: WealthSpectrumConnector):
        self.sf_connector = salesforce_connector
        self.ws_connector = wealth_spectrum_connector
    
    @st.cache_data(ttl=1800)  # Cache for 30 minutes
    def get_integrated_client_data(_self, limit: int = 1000) -> pd.DataFrame:
        """
        Get integrated client data from both systems with optimized joins
        """
        try:
            # Fetch data from both systems concurrently
            with ThreadPoolExecutor(max_workers=2) as executor:
                sf_future = executor.submit(_self.sf_connector.get_clients, limit)
                ws_future = executor.submit(_self.ws_connector.get_portfolios)
                
                sf_clients = sf_future.result()
                ws_portfolios = ws_future.result()
            
            if sf_clients.empty and ws_portfolios.empty:
                return pd.DataFrame()
            
            # Optimize merge operation
            if not sf_clients.empty and not ws_portfolios.empty:
                # Use efficient merge with proper indexing
                merged_data = pd.merge(
                    sf_clients,
                    ws_portfolios,
                    left_on='client_id',
                    right_on='client_id',
                    how='outer',
                    suffixes=('_sf', '_ws')
                )
            elif not sf_clients.empty:
                merged_data = sf_clients
            else:
                merged_data = ws_portfolios
            
            # Optimize data types for memory efficiency
            merged_data = _self._optimize_dataframe_dtypes(merged_data)
            
            return merged_data
            
        except Exception as e:
            logger.error(f"Failed to get integrated client data: {e}")
            return pd.DataFrame()
    
    def _optimize_dataframe_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize DataFrame data types for memory efficiency
        """
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to convert to category if low cardinality
                if df[col].nunique() / len(df) < 0.5:
                    df[col] = df[col].astype('category')
            elif df[col].dtype == 'float64':
                # Downcast floats if possible
                df[col] = pd.to_numeric(df[col], downcast='float')
            elif df[col].dtype == 'int64':
                # Downcast integers if possible
                df[col] = pd.to_numeric(df[col], downcast='integer')
        
        return df
    
    def sync_data_incremental(self, last_sync_time: datetime = None) -> Dict[str, int]:
        """
        Perform incremental data sync for efficiency
        """
        if last_sync_time is None:
            last_sync_time = datetime.now() - timedelta(days=1)
        
        sync_results = {
            'clients_updated': 0,
            'portfolios_updated': 0,
            'errors': 0
        }
        
        try:
            # Implement incremental sync logic here
            # This would typically involve checking LastModifiedDate fields
            # and only fetching records that have changed since last sync
            
            logger.info(f"Incremental sync completed: {sync_results}")
            return sync_results
            
        except Exception as e:
            logger.error(f"Incremental sync failed: {e}")
            sync_results['errors'] = 1
            return sync_results

# Factory function for creating optimized connectors
def create_api_connectors(salesforce_config: Dict, wealth_spectrum_config: Dict) -> tuple:
    """
    Factory function to create optimized API connectors
    """
    # Salesforce connector
    sf_config = APIConfig(
        base_url=salesforce_config['base_url'],
        api_key=salesforce_config['api_key'],
        timeout=30,
        max_retries=3,
        rate_limit_per_minute=100
    )
    
    sf_connector = SalesforceConnector(
        sf_config,
        salesforce_config['client_id'],
        salesforce_config['client_secret']
    )
    
    # Wealth Spectrum connector
    ws_config = APIConfig(
        base_url=wealth_spectrum_config['base_url'],
        api_key=wealth_spectrum_config['api_key'],
        timeout=30,
        max_retries=3,
        rate_limit_per_minute=60
    )
    
    ws_connector = WealthSpectrumConnector(ws_config)
    
    return sf_connector, ws_connector

