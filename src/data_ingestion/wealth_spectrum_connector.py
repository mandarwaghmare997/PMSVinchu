"""
Wealth Spectrum PMS Data Connector for PMS Intelligence Hub
Handles both API and CSV/Excel-based data ingestion from Wealth Spectrum
"""

import os
import pandas as pd
import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import numpy as np
from decimal import Decimal
import xlrd
import openpyxl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WealthSpectrumConfig:
    """Wealth Spectrum connection configuration"""
    api_key: str
    base_url: str
    username: Optional[str] = None
    password: Optional[str] = None
    timeout: int = 30
    api_version: str = 'v1'

class WealthSpectrumConnector:
    """
    Wealth Spectrum PMS connector supporting both API and file-based data ingestion
    """
    
    def __init__(self, config: WealthSpectrumConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {config.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.authenticated = False
        
    def authenticate_api(self) -> bool:
        """
        Authenticate with Wealth Spectrum API
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            if self.config.username and self.config.password:
                # Username/password authentication
                auth_url = f"{self.config.base_url}/auth/login"
                auth_data = {
                    'username': self.config.username,
                    'password': self.config.password
                }
                
                response = self.session.post(auth_url, json=auth_data, timeout=self.config.timeout)
                response.raise_for_status()
                
                auth_result = response.json()
                if 'access_token' in auth_result:
                    self.session.headers.update({
                        'Authorization': f'Bearer {auth_result["access_token"]}'
                    })
                    self.authenticated = True
                    logger.info("Successfully authenticated with Wealth Spectrum API")
                    return True
            else:
                # API key authentication - test with a simple endpoint
                test_url = f"{self.config.base_url}/api/{self.config.api_version}/health"
                response = self.session.get(test_url, timeout=self.config.timeout)
                response.raise_for_status()
                
                self.authenticated = True
                logger.info("Successfully authenticated with Wealth Spectrum API using API key")
                return True
                
        except Exception as e:
            logger.error(f"Failed to authenticate with Wealth Spectrum API: {str(e)}")
            return False
    
    def get_portfolios_api(self, client_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch portfolio data from Wealth Spectrum API
        
        Args:
            client_id: Filter by specific client ID
            
        Returns:
            List of portfolio records
        """
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate_api() first.")
        
        try:
            url = f"{self.config.base_url}/api/{self.config.api_version}/portfolios"
            params = {}
            
            if client_id:
                params['client_id'] = client_id
            
            response = self.session.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()
            
            data = response.json()
            portfolios = data.get('portfolios', [])
            
            logger.info(f"Retrieved {len(portfolios)} portfolio records from Wealth Spectrum API")
            
            # Transform data to standard format
            transformed_portfolios = []
            for portfolio in portfolios:
                transformed_portfolio = self._transform_portfolio_data(portfolio)
                transformed_portfolios.append(transformed_portfolio)
            
            return transformed_portfolios
            
        except Exception as e:
            logger.error(f"Error fetching portfolios from Wealth Spectrum API: {str(e)}")
            raise
    
    def get_holdings_api(self, portfolio_id: str, as_of_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Fetch portfolio holdings from Wealth Spectrum API
        
        Args:
            portfolio_id: Portfolio identifier
            as_of_date: Holdings as of specific date
            
        Returns:
            List of holding records
        """
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate_api() first.")
        
        try:
            url = f"{self.config.base_url}/api/{self.config.api_version}/portfolios/{portfolio_id}/holdings"
            params = {}
            
            if as_of_date:
                params['as_of_date'] = as_of_date.strftime('%Y-%m-%d')
            
            response = self.session.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()
            
            data = response.json()
            holdings = data.get('holdings', [])
            
            logger.info(f"Retrieved {len(holdings)} holding records for portfolio {portfolio_id}")
            
            # Transform data
            transformed_holdings = []
            for holding in holdings:
                transformed_holding = self._transform_holding_data(holding, portfolio_id)
                transformed_holdings.append(transformed_holding)
            
            return transformed_holdings
            
        except Exception as e:
            logger.error(f"Error fetching holdings for portfolio {portfolio_id}: {str(e)}")
            raise
    
    def get_transactions_api(
        self, 
        portfolio_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch transaction data from Wealth Spectrum API
        
        Args:
            portfolio_id: Filter by portfolio ID
            start_date: Start date for transaction filter
            end_date: End date for transaction filter
            
        Returns:
            List of transaction records
        """
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate_api() first.")
        
        try:
            url = f"{self.config.base_url}/api/{self.config.api_version}/transactions"
            params = {}
            
            if portfolio_id:
                params['portfolio_id'] = portfolio_id
            if start_date:
                params['start_date'] = start_date.strftime('%Y-%m-%d')
            if end_date:
                params['end_date'] = end_date.strftime('%Y-%m-%d')
            
            response = self.session.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()
            
            data = response.json()
            transactions = data.get('transactions', [])
            
            logger.info(f"Retrieved {len(transactions)} transaction records")
            
            # Transform data
            transformed_transactions = []
            for transaction in transactions:
                transformed_transaction = self._transform_transaction_data(transaction)
                transformed_transactions.append(transformed_transaction)
            
            return transformed_transactions
            
        except Exception as e:
            logger.error(f"Error fetching transactions: {str(e)}")
            raise
    
    def get_performance_api(
        self, 
        portfolio_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch performance data from Wealth Spectrum API
        
        Args:
            portfolio_id: Portfolio identifier
            start_date: Start date for performance calculation
            end_date: End date for performance calculation
            
        Returns:
            List of performance records
        """
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate_api() first.")
        
        try:
            url = f"{self.config.base_url}/api/{self.config.api_version}/portfolios/{portfolio_id}/performance"
            params = {}
            
            if start_date:
                params['start_date'] = start_date.strftime('%Y-%m-%d')
            if end_date:
                params['end_date'] = end_date.strftime('%Y-%m-%d')
            
            response = self.session.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()
            
            data = response.json()
            performance_data = data.get('performance', [])
            
            logger.info(f"Retrieved performance data for portfolio {portfolio_id}")
            
            # Transform data
            transformed_performance = []
            for perf in performance_data:
                transformed_perf = self._transform_performance_data(perf, portfolio_id)
                transformed_performance.append(transformed_perf)
            
            return transformed_performance
            
        except Exception as e:
            logger.error(f"Error fetching performance for portfolio {portfolio_id}: {str(e)}")
            raise
    
    def process_excel_file(self, file_path: str, data_type: str) -> List[Dict[str, Any]]:
        """
        Process Excel file exported from Wealth Spectrum
        
        Args:
            file_path: Path to Excel file
            data_type: Type of data ('portfolios', 'holdings', 'transactions', 'performance')
            
        Returns:
            List of processed records
        """
        try:
            # Determine file type and read accordingly
            if file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path, engine='openpyxl')
            elif file_path.endswith('.xls'):
                df = pd.read_excel(file_path, engine='xlrd')
            else:
                # Try CSV
                df = pd.read_csv(file_path)
            
            logger.info(f"Processing file: {file_path} with {len(df)} records")
            
            # Process based on data type
            if data_type == 'portfolios':
                return self._process_portfolios_file(df)
            elif data_type == 'holdings':
                return self._process_holdings_file(df)
            elif data_type == 'transactions':
                return self._process_transactions_file(df)
            elif data_type == 'performance':
                return self._process_performance_file(df)
            else:
                raise ValueError(f"Unsupported data type: {data_type}")
                
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            raise
    
    def _process_portfolios_file(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Process portfolios from file data"""
        portfolios = []
        
        # Define column mappings (file column -> standard field)
        column_mapping = {
            'Portfolio ID': 'portfolio_id',
            'Portfolio Name': 'portfolio_name',
            'Client ID': 'client_id',
            'Client Name': 'client_name',
            'Portfolio Type': 'portfolio_type',
            'Investment Strategy': 'investment_strategy',
            'Inception Date': 'inception_date',
            'Initial Investment': 'initial_investment',
            'Management Fee': 'management_fee_rate',
            'Performance Fee': 'performance_fee_rate',
            'Benchmark': 'benchmark_name',
            'Status': 'status'
        }
        
        for _, row in df.iterrows():
            portfolio = {}
            
            # Map columns
            for file_col, std_field in column_mapping.items():
                if file_col in df.columns:
                    value = row[file_col]
                    if pd.notna(value):
                        portfolio[std_field] = value
            
            # Data type conversions
            if 'inception_date' in portfolio:
                portfolio['inception_date'] = pd.to_datetime(portfolio['inception_date']).date()
            
            if 'initial_investment' in portfolio:
                portfolio['initial_investment'] = float(portfolio['initial_investment'])
            
            if 'management_fee_rate' in portfolio:
                # Convert percentage to decimal
                fee = float(portfolio['management_fee_rate'])
                portfolio['management_fee_rate'] = fee / 100 if fee > 1 else fee
            
            # Set defaults
            portfolio['status'] = portfolio.get('status', 'Active')
            portfolio['wealth_spectrum_last_sync'] = datetime.utcnow()
            
            portfolios.append(portfolio)
        
        logger.info(f"Processed {len(portfolios)} portfolio records from file")
        return portfolios
    
    def _process_holdings_file(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Process holdings from file data"""
        holdings = []
        
        column_mapping = {
            'Portfolio ID': 'portfolio_id',
            'Asset ID': 'asset_id',
            'Asset Name': 'asset_name',
            'ISIN': 'isin',
            'Quantity': 'quantity',
            'Average Cost': 'average_cost',
            'Current Price': 'current_price',
            'Market Value': 'market_value',
            'Unrealized P&L': 'unrealized_pnl',
            'Asset Type': 'asset_type',
            'Sector': 'sector'
        }
        
        for _, row in df.iterrows():
            holding = {}
            
            for file_col, std_field in column_mapping.items():
                if file_col in df.columns:
                    value = row[file_col]
                    if pd.notna(value):
                        holding[std_field] = value
            
            # Data type conversions
            numeric_fields = ['quantity', 'average_cost', 'current_price', 'market_value', 'unrealized_pnl']
            for field in numeric_fields:
                if field in holding:
                    holding[field] = float(holding[field])
            
            holding['last_updated'] = datetime.utcnow()
            holdings.append(holding)
        
        logger.info(f"Processed {len(holdings)} holding records from file")
        return holdings
    
    def _process_transactions_file(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Process transactions from file data"""
        transactions = []
        
        column_mapping = {
            'Transaction ID': 'transaction_id',
            'Portfolio ID': 'portfolio_id',
            'Client ID': 'client_id',
            'Asset ID': 'asset_id',
            'Transaction Date': 'transaction_date',
            'Transaction Type': 'transaction_type',
            'Quantity': 'quantity',
            'Price': 'price',
            'Amount': 'amount',
            'Charges': 'charges',
            'Taxes': 'taxes',
            'Net Amount': 'net_amount',
            'Status': 'status'
        }
        
        for _, row in df.iterrows():
            transaction = {}
            
            for file_col, std_field in column_mapping.items():
                if file_col in df.columns:
                    value = row[file_col]
                    if pd.notna(value):
                        transaction[std_field] = value
            
            # Data type conversions
            if 'transaction_date' in transaction:
                transaction['transaction_date'] = pd.to_datetime(transaction['transaction_date']).date()
            
            numeric_fields = ['quantity', 'price', 'amount', 'charges', 'taxes', 'net_amount']
            for field in numeric_fields:
                if field in transaction:
                    transaction[field] = float(transaction[field])
            
            # Set defaults
            transaction['status'] = transaction.get('status', 'Settled')
            transaction['data_source'] = 'Wealth Spectrum File'
            
            transactions.append(transaction)
        
        logger.info(f"Processed {len(transactions)} transaction records from file")
        return transactions
    
    def _process_performance_file(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Process performance data from file"""
        performance_records = []
        
        column_mapping = {
            'Portfolio ID': 'portfolio_id',
            'Period End Date': 'period_end_date',
            'Period Type': 'period_type',
            'Beginning Value': 'beginning_value',
            'Ending Value': 'ending_value',
            'Cash Flows': 'cash_flows',
            'Absolute Return': 'absolute_return',
            'Percentage Return': 'percentage_return',
            'Annualized Return': 'annualized_return',
            'Volatility': 'volatility',
            'Max Drawdown': 'max_drawdown',
            'Sharpe Ratio': 'sharpe_ratio',
            'Benchmark Return': 'benchmark_return',
            'Alpha': 'alpha',
            'Beta': 'beta'
        }
        
        for _, row in df.iterrows():
            performance = {}
            
            for file_col, std_field in column_mapping.items():
                if file_col in df.columns:
                    value = row[file_col]
                    if pd.notna(value):
                        performance[std_field] = value
            
            # Data type conversions
            if 'period_end_date' in performance:
                performance['period_end_date'] = pd.to_datetime(performance['period_end_date']).date()
            
            numeric_fields = [
                'beginning_value', 'ending_value', 'cash_flows', 'absolute_return',
                'percentage_return', 'annualized_return', 'volatility', 'max_drawdown',
                'sharpe_ratio', 'benchmark_return', 'alpha', 'beta'
            ]
            for field in numeric_fields:
                if field in performance:
                    performance[field] = float(performance[field])
            
            performance['calculation_date'] = datetime.utcnow()
            performance_records.append(performance)
        
        logger.info(f"Processed {len(performance_records)} performance records from file")
        return performance_records
    
    def _transform_portfolio_data(self, ws_portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Wealth Spectrum portfolio data to standard format"""
        return {
            'portfolio_id': ws_portfolio.get('portfolio_id'),
            'wealth_spectrum_id': ws_portfolio.get('id'),
            'client_id': ws_portfolio.get('client_id'),
            'portfolio_name': ws_portfolio.get('name'),
            'portfolio_type': ws_portfolio.get('type', 'PMS'),
            'investment_strategy': ws_portfolio.get('strategy'),
            'inception_date': self._parse_date(ws_portfolio.get('inception_date')),
            'initial_investment': float(ws_portfolio.get('initial_investment', 0)),
            'management_fee_rate': float(ws_portfolio.get('management_fee_rate', 0)) / 100,
            'performance_fee_rate': float(ws_portfolio.get('performance_fee_rate', 0)) / 100,
            'benchmark_name': ws_portfolio.get('benchmark'),
            'status': ws_portfolio.get('status', 'Active'),
            'wealth_spectrum_last_sync': datetime.utcnow()
        }
    
    def _transform_holding_data(self, ws_holding: Dict[str, Any], portfolio_id: str) -> Dict[str, Any]:
        """Transform Wealth Spectrum holding data to standard format"""
        return {
            'portfolio_id': portfolio_id,
            'asset_id': ws_holding.get('asset_id') or ws_holding.get('security_id'),
            'asset_name': ws_holding.get('asset_name') or ws_holding.get('security_name'),
            'isin': ws_holding.get('isin'),
            'quantity': float(ws_holding.get('quantity', 0)),
            'average_cost': float(ws_holding.get('average_cost', 0)),
            'current_price': float(ws_holding.get('current_price', 0)),
            'market_value': float(ws_holding.get('market_value', 0)),
            'unrealized_pnl': float(ws_holding.get('unrealized_pnl', 0)),
            'asset_type': ws_holding.get('asset_type'),
            'sector': ws_holding.get('sector'),
            'last_updated': datetime.utcnow()
        }
    
    def _transform_transaction_data(self, ws_transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Wealth Spectrum transaction data to standard format"""
        return {
            'transaction_id': ws_transaction.get('transaction_id') or ws_transaction.get('id'),
            'portfolio_id': ws_transaction.get('portfolio_id'),
            'client_id': ws_transaction.get('client_id'),
            'asset_id': ws_transaction.get('asset_id') or ws_transaction.get('security_id'),
            'transaction_date': self._parse_date(ws_transaction.get('transaction_date')),
            'transaction_type': ws_transaction.get('transaction_type'),
            'quantity': float(ws_transaction.get('quantity', 0)),
            'price': float(ws_transaction.get('price', 0)),
            'amount': float(ws_transaction.get('amount', 0)),
            'charges': float(ws_transaction.get('charges', 0)),
            'taxes': float(ws_transaction.get('taxes', 0)),
            'net_amount': float(ws_transaction.get('net_amount', 0)),
            'status': ws_transaction.get('status', 'Settled'),
            'data_source': 'Wealth Spectrum API',
            'external_ref': ws_transaction.get('external_ref')
        }
    
    def _transform_performance_data(self, ws_performance: Dict[str, Any], portfolio_id: str) -> Dict[str, Any]:
        """Transform Wealth Spectrum performance data to standard format"""
        return {
            'portfolio_id': portfolio_id,
            'period_end_date': self._parse_date(ws_performance.get('period_end_date')),
            'period_type': ws_performance.get('period_type', 'Monthly'),
            'beginning_value': float(ws_performance.get('beginning_value', 0)),
            'ending_value': float(ws_performance.get('ending_value', 0)),
            'cash_flows': float(ws_performance.get('cash_flows', 0)),
            'absolute_return': float(ws_performance.get('absolute_return', 0)),
            'percentage_return': float(ws_performance.get('percentage_return', 0)),
            'annualized_return': float(ws_performance.get('annualized_return', 0)),
            'volatility': float(ws_performance.get('volatility', 0)),
            'max_drawdown': float(ws_performance.get('max_drawdown', 0)),
            'sharpe_ratio': float(ws_performance.get('sharpe_ratio', 0)),
            'benchmark_return': float(ws_performance.get('benchmark_return', 0)),
            'alpha': float(ws_performance.get('alpha', 0)),
            'beta': float(ws_performance.get('beta', 0)),
            'calculation_date': datetime.utcnow(),
            'calculation_method': ws_performance.get('calculation_method', 'TWR')
        }
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime object"""
        if not date_str:
            return None
        
        try:
            if isinstance(date_str, datetime):
                return date_str
            
            # Try different date formats
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S']:
                try:
                    return datetime.strptime(str(date_str), fmt)
                except ValueError:
                    continue
            
            # Try pandas parsing as last resort
            return pd.to_datetime(date_str)
            
        except:
            return None
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test Wealth Spectrum connection and return status
        
        Returns:
            Dictionary with connection status and details
        """
        try:
            if self.authenticate_api():
                # Test with a simple API call
                test_url = f"{self.config.base_url}/api/{self.config.api_version}/portfolios"
                response = self.session.get(test_url, params={'limit': 1}, timeout=self.config.timeout)
                
                if response.status_code == 200:
                    return {
                        'status': 'success',
                        'connected': True,
                        'api_version': self.config.api_version,
                        'base_url': self.config.base_url,
                        'connection_time': datetime.utcnow().isoformat()
                    }
                else:
                    return {
                        'status': 'error',
                        'connected': False,
                        'message': f'API returned status code: {response.status_code}'
                    }
            else:
                return {
                    'status': 'error',
                    'connected': False,
                    'message': 'Authentication failed'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'connected': False,
                'message': str(e)
            }

# Utility functions
def create_wealth_spectrum_connector(
    api_key: str,
    base_url: str,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> WealthSpectrumConnector:
    """
    Create and return a configured Wealth Spectrum connector
    
    Args:
        api_key: Wealth Spectrum API key
        base_url: Base URL for Wealth Spectrum API
        username: Optional username for authentication
        password: Optional password for authentication
        
    Returns:
        Configured WealthSpectrumConnector instance
    """
    config = WealthSpectrumConfig(
        api_key=api_key,
        base_url=base_url,
        username=username,
        password=password
    )
    
    return WealthSpectrumConnector(config)

def load_config_from_env() -> WealthSpectrumConfig:
    """
    Load Wealth Spectrum configuration from environment variables
    
    Returns:
        WealthSpectrumConfig object
    """
    return WealthSpectrumConfig(
        api_key=os.getenv('WEALTH_SPECTRUM_API_KEY'),
        base_url=os.getenv('WEALTH_SPECTRUM_BASE_URL'),
        username=os.getenv('WEALTH_SPECTRUM_USERNAME'),
        password=os.getenv('WEALTH_SPECTRUM_PASSWORD'),
        api_version=os.getenv('WEALTH_SPECTRUM_API_VERSION', 'v1')
    )

