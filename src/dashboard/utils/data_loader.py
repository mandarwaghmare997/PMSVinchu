"""
Data Loader Utility for PMS Intelligence Hub Dashboard
Handles data loading from various sources and caching
"""

import pandas as pd
import streamlit as st
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import json
import os
from pathlib import Path

# Import data connectors
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from data_ingestion.salesforce_connector import SalesforceConnector, load_config_from_env as sf_config
from data_ingestion.wealth_spectrum_connector import WealthSpectrumConnector, load_config_from_env as ws_config

logger = logging.getLogger(__name__)

class DataLoader:
    """
    Centralized data loader for dashboard
    Handles caching, data refresh, and integration with multiple sources
    """
    
    def __init__(self):
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_duration = timedelta(hours=1)  # Cache for 1 hour
        
        # Initialize connectors
        self.sf_connector = None
        self.ws_connector = None
        
    def _get_cache_path(self, data_type: str) -> Path:
        """Get cache file path for data type"""
        return self.cache_dir / f"{data_type}_cache.json"
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Check if cache file is still valid"""
        if not cache_path.exists():
            return False
        
        cache_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        return datetime.now() - cache_time < self.cache_duration
    
    def _save_to_cache(self, data: Any, data_type: str):
        """Save data to cache file"""
        try:
            cache_path = self._get_cache_path(data_type)
            with open(cache_path, 'w') as f:
                if isinstance(data, pd.DataFrame):
                    json.dump(data.to_dict('records'), f, default=str)
                else:
                    json.dump(data, f, default=str)
            logger.info(f"Data cached for {data_type}")
        except Exception as e:
            logger.error(f"Error caching data for {data_type}: {str(e)}")
    
    def _load_from_cache(self, data_type: str) -> Optional[Any]:
        """Load data from cache file"""
        try:
            cache_path = self._get_cache_path(data_type)
            if self._is_cache_valid(cache_path):
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                logger.info(f"Data loaded from cache for {data_type}")
                return pd.DataFrame(data) if isinstance(data, list) else data
        except Exception as e:
            logger.error(f"Error loading cache for {data_type}: {str(e)}")
        return None
    
    @st.cache_data(ttl=3600)  # Streamlit cache for 1 hour
    def load_clients_data(_self, force_refresh: bool = False) -> pd.DataFrame:
        """
        Load clients data from Salesforce
        
        Args:
            force_refresh: Force refresh from source instead of cache
            
        Returns:
            DataFrame with client data
        """
        if not force_refresh:
            cached_data = _self._load_from_cache('clients')
            if cached_data is not None:
                return cached_data
        
        try:
            # Try to load from Salesforce API
            if _self._init_salesforce_connector():
                clients_data = _self.sf_connector.get_clients_api()
                df = pd.DataFrame(clients_data)
                _self._save_to_cache(df, 'clients')
                return df
            else:
                # Fallback to sample data
                return _self._generate_sample_clients_data()
                
        except Exception as e:
            logger.error(f"Error loading clients data: {str(e)}")
            return _self._generate_sample_clients_data()
    
    @st.cache_data(ttl=3600)
    def load_portfolios_data(_self, force_refresh: bool = False) -> pd.DataFrame:
        """
        Load portfolios data from Wealth Spectrum
        
        Args:
            force_refresh: Force refresh from source
            
        Returns:
            DataFrame with portfolio data
        """
        if not force_refresh:
            cached_data = _self._load_from_cache('portfolios')
            if cached_data is not None:
                return cached_data
        
        try:
            # Try to load from Wealth Spectrum API
            if _self._init_wealth_spectrum_connector():
                portfolios_data = _self.ws_connector.get_portfolios_api()
                df = pd.DataFrame(portfolios_data)
                _self._save_to_cache(df, 'portfolios')
                return df
            else:
                # Fallback to sample data
                return _self._generate_sample_portfolios_data()
                
        except Exception as e:
            logger.error(f"Error loading portfolios data: {str(e)}")
            return _self._generate_sample_portfolios_data()
    
    @st.cache_data(ttl=1800)  # Cache for 30 minutes (more frequent updates)
    def load_performance_data(_self, portfolio_ids: List[str] = None, force_refresh: bool = False) -> pd.DataFrame:
        """
        Load performance data for portfolios
        
        Args:
            portfolio_ids: List of portfolio IDs to load data for
            force_refresh: Force refresh from source
            
        Returns:
            DataFrame with performance data
        """
        cache_key = f"performance_{hash(str(portfolio_ids)) if portfolio_ids else 'all'}"
        
        if not force_refresh:
            cached_data = _self._load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        try:
            # Try to load from Wealth Spectrum API
            if _self._init_wealth_spectrum_connector():
                performance_data = []
                if portfolio_ids:
                    for portfolio_id in portfolio_ids:
                        perf_data = _self.ws_connector.get_performance_api(portfolio_id)
                        performance_data.extend(perf_data)
                else:
                    # Load for all portfolios (limited sample)
                    performance_data = _self._generate_sample_performance_data()
                
                df = pd.DataFrame(performance_data)
                _self._save_to_cache(df, cache_key)
                return df
            else:
                # Fallback to sample data
                return _self._generate_sample_performance_data()
                
        except Exception as e:
            logger.error(f"Error loading performance data: {str(e)}")
            return _self._generate_sample_performance_data()
    
    @st.cache_data(ttl=3600)
    def load_holdings_data(_self, portfolio_id: str = None, force_refresh: bool = False) -> pd.DataFrame:
        """
        Load holdings data for portfolios
        
        Args:
            portfolio_id: Specific portfolio ID or None for all
            force_refresh: Force refresh from source
            
        Returns:
            DataFrame with holdings data
        """
        cache_key = f"holdings_{portfolio_id or 'all'}"
        
        if not force_refresh:
            cached_data = _self._load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        try:
            # Try to load from Wealth Spectrum API
            if _self._init_wealth_spectrum_connector():
                if portfolio_id:
                    holdings_data = _self.ws_connector.get_holdings_api(portfolio_id)
                else:
                    # Load sample holdings for demonstration
                    holdings_data = _self._generate_sample_holdings_data()
                
                df = pd.DataFrame(holdings_data)
                _self._save_to_cache(df, cache_key)
                return df
            else:
                # Fallback to sample data
                return _self._generate_sample_holdings_data()
                
        except Exception as e:
            logger.error(f"Error loading holdings data: {str(e)}")
            return _self._generate_sample_holdings_data()
    
    def _init_salesforce_connector(self) -> bool:
        """Initialize Salesforce connector"""
        try:
            if self.sf_connector is None:
                # Try to load from environment variables
                config = sf_config()
                if config.username and config.password and config.security_token:
                    self.sf_connector = SalesforceConnector(config)
                    return self.sf_connector.connect_api()
            return self.sf_connector is not None
        except Exception as e:
            logger.error(f"Error initializing Salesforce connector: {str(e)}")
            return False
    
    def _init_wealth_spectrum_connector(self) -> bool:
        """Initialize Wealth Spectrum connector"""
        try:
            if self.ws_connector is None:
                # Try to load from environment variables
                config = ws_config()
                if config.api_key and config.base_url:
                    self.ws_connector = WealthSpectrumConnector(config)
                    return self.ws_connector.authenticate_api()
            return self.ws_connector is not None
        except Exception as e:
            logger.error(f"Error initializing Wealth Spectrum connector: {str(e)}")
            return False
    
    def _generate_sample_clients_data(self) -> pd.DataFrame:
        """Generate sample clients data for demonstration"""
        import numpy as np
        np.random.seed(42)
        
        n_clients = 150
        
        # Generate realistic client names
        first_names = ['Rajesh', 'Priya', 'Amit', 'Sunita', 'Vikram', 'Meera', 'Arjun', 'Kavya', 
                      'Ravi', 'Deepika', 'Suresh', 'Anita', 'Kiran', 'Pooja', 'Manoj']
        last_names = ['Sharma', 'Patel', 'Singh', 'Kumar', 'Agarwal', 'Gupta', 'Jain', 'Shah',
                     'Reddy', 'Nair', 'Iyer', 'Chopra', 'Malhotra', 'Bansal', 'Mittal']
        
        client_names = [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" 
                       for _ in range(n_clients)]
        
        data = {
            'client_id': [f'CL_{i:04d}' for i in range(1, n_clients + 1)],
            'client_name': client_names,
            'client_type': np.random.choice(['Individual', 'HUF', 'Corporate', 'Trust'], n_clients, p=[0.6, 0.2, 0.15, 0.05]),
            'rm_name': np.random.choice(['Rohit Sharma', 'Priya Nair', 'Amit Gupta', 'Sneha Patel', 'Vikash Kumar'], n_clients),
            'onboarding_date': pd.date_range('2020-01-01', '2024-12-31', periods=n_clients),
            'risk_profile': np.random.choice(['Conservative', 'Moderate', 'Aggressive'], n_clients, p=[0.3, 0.5, 0.2]),
            'investment_category': np.random.choice(['Equity', 'Debt', 'Hybrid', 'Multi-Asset'], n_clients, p=[0.4, 0.3, 0.2, 0.1]),
            'status': np.random.choice(['Active', 'Inactive'], n_clients, p=[0.92, 0.08]),
            'aum': np.random.lognormal(15.5, 0.8, n_clients) * 1000,  # AUM in thousands
            'city': np.random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Pune', 'Hyderabad'], n_clients),
            'kyc_status': np.random.choice(['Verified', 'Pending', 'Expired'], n_clients, p=[0.85, 0.1, 0.05])
        }
        
        # Add performance metrics
        data['cagr'] = np.random.normal(12.5, 4.2, n_clients)
        data['alpha'] = np.random.normal(2.1, 1.8, n_clients)
        data['beta'] = np.random.normal(1.05, 0.25, n_clients)
        data['sharpe_ratio'] = np.random.normal(1.35, 0.45, n_clients)
        data['max_drawdown'] = np.random.normal(-8.5, 3.2, n_clients)
        
        return pd.DataFrame(data)
    
    def _generate_sample_portfolios_data(self) -> pd.DataFrame:
        """Generate sample portfolios data"""
        import numpy as np
        np.random.seed(42)
        
        n_portfolios = 200
        
        data = {
            'portfolio_id': [f'PF_{i:04d}' for i in range(1, n_portfolios + 1)],
            'client_id': [f'CL_{np.random.randint(1, 151):04d}' for _ in range(n_portfolios)],
            'portfolio_name': [f'Portfolio {i}' for i in range(1, n_portfolios + 1)],
            'portfolio_type': np.random.choice(['PMS', 'AIF', 'Discretionary'], n_portfolios, p=[0.6, 0.3, 0.1]),
            'investment_strategy': np.random.choice(['Growth', 'Value', 'Balanced', 'Income'], n_portfolios),
            'inception_date': pd.date_range('2019-01-01', '2024-06-30', periods=n_portfolios),
            'initial_investment': np.random.lognormal(14, 1, n_portfolios) * 1000,
            'current_value': np.random.lognormal(14.5, 1, n_portfolios) * 1000,
            'management_fee_rate': np.random.normal(0.02, 0.005, n_portfolios),
            'performance_fee_rate': np.random.normal(0.15, 0.03, n_portfolios),
            'benchmark': np.random.choice(['NIFTY 50', 'NIFTY 500', 'BSE 500', 'Custom'], n_portfolios),
            'status': np.random.choice(['Active', 'Closed'], n_portfolios, p=[0.9, 0.1])
        }
        
        return pd.DataFrame(data)
    
    def _generate_sample_performance_data(self) -> pd.DataFrame:
        """Generate sample performance data"""
        import numpy as np
        np.random.seed(42)
        
        # Generate monthly performance data for last 2 years
        date_range = pd.date_range('2023-01-31', '2024-12-31', freq='M')
        portfolio_ids = [f'PF_{i:04d}' for i in range(1, 51)]  # Sample 50 portfolios
        
        data = []
        for portfolio_id in portfolio_ids:
            for date in date_range:
                record = {
                    'portfolio_id': portfolio_id,
                    'period_end_date': date,
                    'period_type': 'Monthly',
                    'beginning_value': np.random.lognormal(14, 0.5) * 1000,
                    'ending_value': np.random.lognormal(14.1, 0.5) * 1000,
                    'cash_flows': np.random.normal(0, 50000),
                    'absolute_return': np.random.normal(50000, 200000),
                    'percentage_return': np.random.normal(1.2, 3.5),
                    'annualized_return': np.random.normal(12.5, 4.0),
                    'volatility': np.random.normal(15.2, 3.5),
                    'max_drawdown': np.random.normal(-8.5, 3.0),
                    'sharpe_ratio': np.random.normal(1.35, 0.4),
                    'benchmark_return': np.random.normal(1.0, 3.0),
                    'alpha': np.random.normal(0.2, 1.5),
                    'beta': np.random.normal(1.05, 0.2)
                }
                data.append(record)
        
        return pd.DataFrame(data)
    
    def _generate_sample_holdings_data(self) -> pd.DataFrame:
        """Generate sample holdings data"""
        import numpy as np
        np.random.seed(42)
        
        # Sample asset names
        equity_assets = ['Reliance Industries', 'TCS', 'HDFC Bank', 'Infosys', 'ICICI Bank', 
                        'Hindustan Unilever', 'ITC', 'Kotak Mahindra Bank', 'Bharti Airtel', 'SBI']
        debt_assets = ['Government Bond 7.5%', 'Corporate Bond AAA', 'Treasury Bill', 
                      'State Development Loan', 'PSU Bond']
        
        n_holdings = 500
        
        data = {
            'portfolio_id': [f'PF_{np.random.randint(1, 51):04d}' for _ in range(n_holdings)],
            'asset_id': [f'AS_{i:04d}' for i in range(1, n_holdings + 1)],
            'asset_name': np.random.choice(equity_assets + debt_assets, n_holdings),
            'asset_type': np.random.choice(['Equity', 'Debt', 'Mutual Fund'], n_holdings, p=[0.6, 0.3, 0.1]),
            'quantity': np.random.uniform(10, 10000, n_holdings),
            'average_cost': np.random.uniform(50, 5000, n_holdings),
            'current_price': np.random.uniform(45, 5500, n_holdings),
            'market_value': np.random.uniform(50000, 5000000, n_holdings),
            'unrealized_pnl': np.random.normal(0, 100000, n_holdings),
            'sector': np.random.choice(['Technology', 'Banking', 'FMCG', 'Energy', 'Healthcare'], n_holdings),
            'weight': np.random.uniform(0.5, 15.0, n_holdings)
        }
        
        return pd.DataFrame(data)
    
    def get_data_freshness_info(self) -> Dict[str, Any]:
        """Get information about data freshness and last update times"""
        info = {}
        
        for data_type in ['clients', 'portfolios', 'performance', 'holdings']:
            cache_path = self._get_cache_path(data_type)
            if cache_path.exists():
                last_update = datetime.fromtimestamp(cache_path.stat().st_mtime)
                info[data_type] = {
                    'last_updated': last_update.strftime('%Y-%m-%d %H:%M:%S'),
                    'is_fresh': self._is_cache_valid(cache_path),
                    'age_minutes': int((datetime.now() - last_update).total_seconds() / 60)
                }
            else:
                info[data_type] = {
                    'last_updated': 'Never',
                    'is_fresh': False,
                    'age_minutes': None
                }
        
        return info
    
    def refresh_all_data(self):
        """Force refresh all cached data"""
        data_types = ['clients', 'portfolios', 'performance', 'holdings']
        
        for data_type in data_types:
            try:
                if data_type == 'clients':
                    self.load_clients_data(force_refresh=True)
                elif data_type == 'portfolios':
                    self.load_portfolios_data(force_refresh=True)
                elif data_type == 'performance':
                    self.load_performance_data(force_refresh=True)
                elif data_type == 'holdings':
                    self.load_holdings_data(force_refresh=True)
                    
                logger.info(f"Refreshed {data_type} data")
            except Exception as e:
                logger.error(f"Error refreshing {data_type} data: {str(e)}")
    
    def clear_cache(self):
        """Clear all cached data"""
        try:
            for cache_file in self.cache_dir.glob("*_cache.json"):
                cache_file.unlink()
            logger.info("Cache cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")

