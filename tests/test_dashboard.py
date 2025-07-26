"""
Comprehensive Test Suite for PMS Intelligence Hub Dashboard
Tests all components, utilities, and integrations
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import tempfile
import os
import sys
from unittest.mock import Mock, patch, MagicMock
import io

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from dashboard.utils.data_loader import DataLoader
from dashboard.utils.calculations import PerformanceCalculator
from dashboard.utils.pdf_generator import PDFReportGenerator, generate_pdf_report
from data_ingestion.salesforce_connector import SalesforceConnector
from data_ingestion.wealth_spectrum_connector import WealthSpectrumConnector

class TestDataLoader:
    """Test suite for DataLoader class"""
    
    def setup_method(self):
        """Setup test environment"""
        self.data_loader = DataLoader()
        
    def test_cache_path_generation(self):
        """Test cache path generation"""
        cache_path = self.data_loader._get_cache_path('test_data')
        assert cache_path.name == 'test_data_cache.json'
        assert cache_path.parent.name == 'cache'
    
    def test_sample_clients_data_generation(self):
        """Test sample clients data generation"""
        df = self.data_loader._generate_sample_clients_data()
        
        # Check structure
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 150  # Default number of clients
        
        # Check required columns
        required_columns = [
            'client_id', 'client_name', 'rm_name', 'aum', 
            'risk_profile', 'investment_category', 'status'
        ]
        for col in required_columns:
            assert col in df.columns
        
        # Check data types and ranges
        assert df['aum'].dtype in [np.float64, np.int64]
        assert df['aum'].min() > 0
        assert set(df['status'].unique()).issubset({'Active', 'Inactive'})
        assert set(df['risk_profile'].unique()).issubset({'Conservative', 'Moderate', 'Aggressive'})
    
    def test_sample_portfolios_data_generation(self):
        """Test sample portfolios data generation"""
        df = self.data_loader._generate_sample_portfolios_data()
        
        # Check structure
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 200  # Default number of portfolios
        
        # Check required columns
        required_columns = [
            'portfolio_id', 'client_id', 'portfolio_name', 
            'portfolio_type', 'investment_strategy'
        ]
        for col in required_columns:
            assert col in df.columns
        
        # Check portfolio IDs format
        assert all(df['portfolio_id'].str.startswith('PF_'))
        assert all(df['client_id'].str.startswith('CL_'))
    
    def test_sample_performance_data_generation(self):
        """Test sample performance data generation"""
        df = self.data_loader._generate_sample_performance_data()
        
        # Check structure
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        
        # Check required columns
        required_columns = [
            'portfolio_id', 'period_end_date', 'annualized_return',
            'volatility', 'sharpe_ratio', 'alpha', 'beta'
        ]
        for col in required_columns:
            assert col in df.columns
        
        # Check data validity
        assert df['period_end_date'].dtype == 'datetime64[ns]'
        assert df['sharpe_ratio'].notna().all()
    
    def test_sample_holdings_data_generation(self):
        """Test sample holdings data generation"""
        df = self.data_loader._generate_sample_holdings_data()
        
        # Check structure
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 500  # Default number of holdings
        
        # Check required columns
        required_columns = [
            'portfolio_id', 'asset_id', 'asset_name', 'asset_type',
            'quantity', 'current_price', 'market_value'
        ]
        for col in required_columns:
            assert col in df.columns
        
        # Check data validity
        assert df['quantity'].min() >= 0
        assert df['current_price'].min() >= 0
        assert df['market_value'].min() >= 0
    
    @patch('src.dashboard.utils.data_loader.SalesforceConnector')
    def test_salesforce_connector_initialization(self, mock_sf_connector):
        """Test Salesforce connector initialization"""
        mock_instance = Mock()
        mock_sf_connector.return_value = mock_instance
        mock_instance.connect_api.return_value = True
        
        # Test successful initialization
        with patch('src.dashboard.utils.data_loader.sf_config') as mock_config:
            mock_config.return_value = Mock(
                username='test', password='test', security_token='test'
            )
            result = self.data_loader._init_salesforce_connector()
            assert result is True
    
    @patch('src.dashboard.utils.data_loader.WealthSpectrumConnector')
    def test_wealth_spectrum_connector_initialization(self, mock_ws_connector):
        """Test Wealth Spectrum connector initialization"""
        mock_instance = Mock()
        mock_ws_connector.return_value = mock_instance
        mock_instance.authenticate_api.return_value = True
        
        # Test successful initialization
        with patch('src.dashboard.utils.data_loader.ws_config') as mock_config:
            mock_config.return_value = Mock(
                api_key='test', base_url='https://test.com'
            )
            result = self.data_loader._init_wealth_spectrum_connector()
            assert result is True
    
    def test_data_freshness_info(self):
        """Test data freshness information"""
        info = self.data_loader.get_data_freshness_info()
        
        # Check structure
        assert isinstance(info, dict)
        expected_keys = ['clients', 'portfolios', 'performance', 'holdings']
        for key in expected_keys:
            assert key in info
            assert 'last_updated' in info[key]
            assert 'is_fresh' in info[key]
            assert 'age_minutes' in info[key]

class TestPerformanceCalculator:
    """Test suite for PerformanceCalculator class"""
    
    def setup_method(self):
        """Setup test environment"""
        self.calc = PerformanceCalculator()
        
        # Create sample data
        dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
        np.random.seed(42)
        returns = np.random.normal(0.001, 0.02, len(dates))  # Daily returns
        prices = pd.Series(100 * np.cumprod(1 + returns), index=dates)
        
        self.sample_prices = prices
        self.sample_returns = self.calc.calculate_returns(prices)
    
    def test_calculate_returns_simple(self):
        """Test simple returns calculation"""
        prices = pd.Series([100, 105, 110, 108])
        returns = self.calc.calculate_returns(prices, method='simple')
        
        expected = pd.Series([0.05, 0.047619, -0.018182], index=[1, 2, 3])
        pd.testing.assert_series_equal(returns, expected, rtol=1e-5)
    
    def test_calculate_returns_log(self):
        """Test log returns calculation"""
        prices = pd.Series([100, 105, 110])
        returns = self.calc.calculate_returns(prices, method='log')
        
        assert len(returns) == 2
        assert returns.iloc[0] == np.log(105/100)
        assert returns.iloc[1] == np.log(110/105)
    
    def test_calculate_cagr(self):
        """Test CAGR calculation"""
        # Test normal case
        cagr = self.calc.calculate_cagr(100, 121, 2)  # 10% CAGR over 2 years
        assert abs(cagr - 10.0) < 0.01
        
        # Test edge cases
        assert self.calc.calculate_cagr(0, 100, 1) == 0.0  # Zero beginning value
        assert self.calc.calculate_cagr(100, 100, 0) == 0.0  # Zero periods
    
    def test_calculate_volatility(self):
        """Test volatility calculation"""
        returns = pd.Series([0.01, -0.02, 0.015, -0.01, 0.005])
        
        # Test non-annualized
        vol = self.calc.calculate_volatility(returns, annualize=False)
        expected = returns.std() * 100
        assert abs(vol - expected) < 0.01
        
        # Test annualized (assuming daily data)
        vol_ann = self.calc.calculate_volatility(returns, annualize=True)
        assert vol_ann > vol  # Annualized should be higher
    
    def test_calculate_sharpe_ratio(self):
        """Test Sharpe ratio calculation"""
        # Create returns with positive mean
        returns = pd.Series([0.01, 0.02, -0.005, 0.015, 0.008])
        
        sharpe = self.calc.calculate_sharpe_ratio(returns, risk_free_rate=0.05)
        assert isinstance(sharpe, float)
        assert not np.isnan(sharpe)
        
        # Test with zero volatility
        zero_vol_returns = pd.Series([0.01, 0.01, 0.01, 0.01])
        sharpe_zero = self.calc.calculate_sharpe_ratio(zero_vol_returns)
        assert sharpe_zero == 0.0
    
    def test_calculate_sortino_ratio(self):
        """Test Sortino ratio calculation"""
        returns = pd.Series([0.02, -0.01, 0.015, -0.005, 0.01])
        
        sortino = self.calc.calculate_sortino_ratio(returns)
        assert isinstance(sortino, float)
        assert not np.isnan(sortino)
        
        # Test with no negative returns
        positive_returns = pd.Series([0.01, 0.02, 0.015, 0.01])
        sortino_pos = self.calc.calculate_sortino_ratio(positive_returns)
        assert sortino_pos == np.inf  # Should be infinite with no downside
    
    def test_calculate_max_drawdown(self):
        """Test maximum drawdown calculation"""
        # Create price series with known drawdown
        prices = pd.Series([100, 120, 110, 90, 95, 105], 
                          index=pd.date_range('2023-01-01', periods=6, freq='M'))
        
        dd_info = self.calc.calculate_max_drawdown(prices)
        
        assert 'max_drawdown' in dd_info
        assert 'start_date' in dd_info
        assert 'end_date' in dd_info
        assert dd_info['max_drawdown'] < 0  # Should be negative
        
        # Check that max drawdown is approximately -25% (120 to 90)
        expected_dd = -25.0  # (90-120)/120 * 100
        assert abs(dd_info['max_drawdown'] - expected_dd) < 1.0
    
    def test_calculate_alpha_beta(self):
        """Test alpha and beta calculation"""
        # Create correlated returns
        np.random.seed(42)
        benchmark_returns = pd.Series(np.random.normal(0.001, 0.015, 100))
        portfolio_returns = 0.5 * benchmark_returns + pd.Series(np.random.normal(0.0005, 0.01, 100))
        
        alpha, beta = self.calc.calculate_alpha_beta(portfolio_returns, benchmark_returns)
        
        assert isinstance(alpha, float)
        assert isinstance(beta, float)
        assert not np.isnan(alpha)
        assert not np.isnan(beta)
        assert beta > 0  # Should be positive for correlated returns
    
    def test_calculate_information_ratio(self):
        """Test information ratio calculation"""
        np.random.seed(42)
        benchmark_returns = pd.Series(np.random.normal(0.001, 0.015, 100))
        portfolio_returns = benchmark_returns + pd.Series(np.random.normal(0.0002, 0.005, 100))
        
        ir = self.calc.calculate_information_ratio(portfolio_returns, benchmark_returns)
        
        assert isinstance(ir, float)
        assert not np.isnan(ir)
    
    def test_calculate_var(self):
        """Test Value at Risk calculation"""
        returns = pd.Series(np.random.normal(0.001, 0.02, 1000))
        
        var_95 = self.calc.calculate_var(returns, 0.95)
        var_99 = self.calc.calculate_var(returns, 0.99)
        
        assert isinstance(var_95, float)
        assert isinstance(var_99, float)
        assert var_99 < var_95  # 99% VaR should be more extreme
    
    def test_calculate_portfolio_metrics(self):
        """Test comprehensive portfolio metrics calculation"""
        metrics = self.calc.calculate_portfolio_metrics(self.sample_prices)
        
        # Check all expected metrics are present
        expected_metrics = [
            'total_return', 'annualized_return', 'volatility', 'sharpe_ratio',
            'sortino_ratio', 'max_drawdown', 'calmar_ratio', 'var_95', 'var_99'
        ]
        
        for metric in expected_metrics:
            assert metric in metrics
            assert isinstance(metrics[metric], (int, float))
            assert not np.isnan(metrics[metric])
    
    def test_calculate_portfolio_metrics_with_benchmark(self):
        """Test portfolio metrics with benchmark comparison"""
        # Create benchmark prices
        np.random.seed(43)
        benchmark_returns = np.random.normal(0.0008, 0.015, len(self.sample_prices))
        benchmark_prices = pd.Series(
            100 * np.cumprod(1 + benchmark_returns), 
            index=self.sample_prices.index
        )
        
        metrics = self.calc.calculate_portfolio_metrics(
            self.sample_prices, 
            benchmark_prices
        )
        
        # Check benchmark-specific metrics
        benchmark_metrics = ['alpha', 'beta', 'information_ratio', 'tracking_error', 'excess_return']
        for metric in benchmark_metrics:
            assert metric in metrics
            assert isinstance(metrics[metric], (int, float))
    
    def test_empty_metrics(self):
        """Test empty metrics for edge cases"""
        empty_metrics = self.calc._empty_metrics()
        
        assert isinstance(empty_metrics, dict)
        assert 'total_return' in empty_metrics
        assert empty_metrics['total_return'] == 0.0
        assert empty_metrics['beta'] == 1.0  # Beta defaults to 1
    
    def test_xirr_calculation(self):
        """Test XIRR calculation"""
        # Test with simple cash flows
        cash_flows = [-1000, -1000, 1500, 1500]  # Two investments, two returns
        dates = [
            datetime(2023, 1, 1),
            datetime(2023, 6, 1),
            datetime(2023, 12, 1),
            datetime(2024, 6, 1)
        ]
        
        xirr = self.calc.calculate_xirr(cash_flows, dates)
        assert isinstance(xirr, float)
        # XIRR should be reasonable for this cash flow pattern

class TestPDFReportGenerator:
    """Test suite for PDFReportGenerator class"""
    
    def setup_method(self):
        """Setup test environment"""
        self.generator = PDFReportGenerator()
        
        # Create sample data
        self.sample_client_data = pd.DataFrame({
            'client_id': ['CL_0001', 'CL_0002', 'CL_0003'],
            'client_name': ['Client A', 'Client B', 'Client C'],
            'aum': [1000000, 2000000, 1500000],
            'cagr': [12.5, 15.2, 10.8],
            'alpha': [2.1, 3.5, 1.2],
            'investment_category': ['Equity', 'Hybrid', 'Debt'],
            'risk_profile': ['Aggressive', 'Moderate', 'Conservative'],
            'status': ['Active', 'Active', 'Active']
        })
        
        self.sample_portfolio_data = pd.DataFrame({
            'portfolio_id': ['PF_0001', 'PF_0002', 'PF_0003'],
            'client_id': ['CL_0001', 'CL_0002', 'CL_0003'],
            'portfolio_type': ['PMS', 'AIF', 'PMS'],
            'investment_strategy': ['Growth', 'Value', 'Balanced']
        })
        
        self.sample_performance_data = pd.DataFrame({
            'portfolio_id': ['PF_0001', 'PF_0002', 'PF_0003'],
            'annualized_return': [12.5, 15.2, 10.8],
            'volatility': [18.5, 22.1, 15.3],
            'sharpe_ratio': [1.2, 1.5, 1.1]
        })
    
    def test_pdf_generator_initialization(self):
        """Test PDF generator initialization"""
        assert self.generator is not None
        assert hasattr(self.generator, 'styles')
        assert 'CustomTitle' in self.generator.styles
        assert 'CustomSubtitle' in self.generator.styles
    
    def test_generate_portfolio_report(self):
        """Test portfolio report generation"""
        config = {
            'title': 'Test Portfolio Report',
            'date': '2024-01-01'
        }
        
        pdf_bytes = self.generator.generate_portfolio_report(
            self.sample_client_data,
            self.sample_portfolio_data,
            self.sample_performance_data,
            config
        )
        
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 1000  # Should be substantial PDF content
        assert pdf_bytes.startswith(b'%PDF')  # PDF header
    
    def test_generate_client_report(self):
        """Test individual client report generation"""
        client_data = {
            'client_id': 'CL_0001',
            'client_name': 'Test Client',
            'aum': 1000000,
            'risk_profile': 'Moderate',
            'investment_category': 'Equity',
            'rm_name': 'Test RM',
            'onboarding_date': '2023-01-01'
        }
        
        portfolio_data = [
            {
                'portfolio_id': 'PF_0001',
                'portfolio_type': 'PMS',
                'investment_strategy': 'Growth'
            }
        ]
        
        performance_data = [
            {
                'ending_value': 1200000,
                'annualized_return': 15.5,
                'alpha': 2.5,
                'beta': 1.1,
                'sharpe_ratio': 1.3,
                'max_drawdown': -8.5
            }
        ]
        
        pdf_bytes = self.generator.generate_client_report(
            'CL_0001',
            client_data,
            portfolio_data,
            performance_data
        )
        
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 500
        assert pdf_bytes.startswith(b'%PDF')
    
    def test_convenience_function(self):
        """Test convenience function for PDF generation"""
        pdf_bytes = generate_pdf_report(
            self.sample_client_data,
            report_type="portfolio_overview"
        )
        
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 1000
        assert pdf_bytes.startswith(b'%PDF')
    
    def test_invalid_report_type(self):
        """Test handling of invalid report type"""
        with pytest.raises(ValueError):
            generate_pdf_report(
                self.sample_client_data,
                report_type="invalid_type"
            )

class TestIntegration:
    """Integration tests for dashboard components"""
    
    def setup_method(self):
        """Setup integration test environment"""
        self.data_loader = DataLoader()
        self.calc = PerformanceCalculator()
        self.pdf_gen = PDFReportGenerator()
    
    def test_data_loader_to_calculator_integration(self):
        """Test integration between data loader and calculator"""
        # Load sample data
        client_data = self.data_loader._generate_sample_clients_data()
        performance_data = self.data_loader._generate_sample_performance_data()
        
        # Test that calculator can process the data
        if not performance_data.empty and 'annualized_return' in performance_data.columns:
            returns = performance_data['annualized_return'] / 100  # Convert to decimal
            vol = self.calc.calculate_volatility(returns, annualize=False)
            assert isinstance(vol, float)
            assert vol >= 0
    
    def test_data_loader_to_pdf_integration(self):
        """Test integration between data loader and PDF generator"""
        # Load sample data
        client_data = self.data_loader._generate_sample_clients_data()
        portfolio_data = self.data_loader._generate_sample_portfolios_data()
        performance_data = self.data_loader._generate_sample_performance_data()
        
        # Generate PDF report
        config = {'title': 'Integration Test Report'}
        pdf_bytes = self.pdf_gen.generate_portfolio_report(
            client_data.head(10),  # Use smaller subset for testing
            portfolio_data.head(10),
            performance_data.head(50),
            config
        )
        
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 1000
    
    def test_full_workflow_integration(self):
        """Test complete workflow from data loading to report generation"""
        # Step 1: Load data
        client_data = self.data_loader.load_clients_data()
        
        # Step 2: Calculate metrics (simulate with sample data)
        sample_prices = pd.Series(
            np.random.lognormal(4.6, 0.2, 100),
            index=pd.date_range('2023-01-01', periods=100, freq='D')
        )
        metrics = self.calc.calculate_portfolio_metrics(sample_prices)
        
        # Step 3: Generate report
        config = {
            'title': 'Full Workflow Test Report',
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        pdf_bytes = generate_pdf_report(
            client_data.head(5),
            report_type="portfolio_overview",
            config=config
        )
        
        # Verify complete workflow
        assert isinstance(client_data, pd.DataFrame)
        assert len(client_data) > 0
        assert isinstance(metrics, dict)
        assert len(metrics) > 0
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 1000

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrames"""
        calc = PerformanceCalculator()
        
        # Empty price series
        empty_prices = pd.Series([], dtype=float)
        metrics = calc.calculate_portfolio_metrics(empty_prices)
        
        # Should return empty metrics without crashing
        assert isinstance(metrics, dict)
        assert metrics['total_return'] == 0.0
    
    def test_invalid_data_handling(self):
        """Test handling of invalid data"""
        calc = PerformanceCalculator()
        
        # Negative prices (should handle gracefully)
        invalid_prices = pd.Series([-100, -90, -110])
        
        # Should not crash, but may return zero/default values
        try:
            metrics = calc.calculate_portfolio_metrics(invalid_prices)
            assert isinstance(metrics, dict)
        except Exception as e:
            # If it does raise an exception, it should be handled gracefully
            assert isinstance(e, (ValueError, ZeroDivisionError))
    
    def test_missing_data_handling(self):
        """Test handling of missing data"""
        data_loader = DataLoader()
        
        # Test with missing cache files
        cache_info = data_loader.get_data_freshness_info()
        
        # Should handle missing cache gracefully
        assert isinstance(cache_info, dict)
        for data_type in ['clients', 'portfolios', 'performance', 'holdings']:
            assert data_type in cache_info
    
    def test_pdf_generation_with_minimal_data(self):
        """Test PDF generation with minimal data"""
        generator = PDFReportGenerator()
        
        # Minimal data
        minimal_client_data = pd.DataFrame({
            'client_id': ['CL_0001'],
            'client_name': ['Test Client'],
            'aum': [100000],
            'status': ['Active']
        })
        
        minimal_portfolio_data = pd.DataFrame()
        minimal_performance_data = pd.DataFrame()
        
        config = {'title': 'Minimal Data Test'}
        
        # Should generate PDF without crashing
        pdf_bytes = generator.generate_portfolio_report(
            minimal_client_data,
            minimal_portfolio_data,
            minimal_performance_data,
            config
        )
        
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 500

# Pytest configuration and fixtures
@pytest.fixture
def sample_data():
    """Fixture providing sample data for tests"""
    np.random.seed(42)
    
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    returns = np.random.normal(0.001, 0.02, len(dates))
    prices = pd.Series(100 * np.cumprod(1 + returns), index=dates)
    
    client_data = pd.DataFrame({
        'client_id': [f'CL_{i:04d}' for i in range(1, 11)],
        'client_name': [f'Client {i}' for i in range(1, 11)],
        'aum': np.random.lognormal(15, 0.5, 10) * 1000,
        'cagr': np.random.normal(12, 3, 10),
        'status': ['Active'] * 10
    })
    
    return {
        'prices': prices,
        'returns': returns,
        'client_data': client_data
    }

@pytest.fixture
def temp_directory():
    """Fixture providing temporary directory for tests"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

# Performance benchmarks (optional)
class TestPerformance:
    """Performance tests for critical components"""
    
    def test_large_dataset_performance(self):
        """Test performance with large datasets"""
        import time
        
        # Generate large dataset
        n_records = 10000
        large_data = pd.DataFrame({
            'client_id': [f'CL_{i:04d}' for i in range(n_records)],
            'aum': np.random.lognormal(15, 0.5, n_records) * 1000,
            'cagr': np.random.normal(12, 3, n_records)
        })
        
        # Time the operations
        start_time = time.time()
        
        # Simulate data processing
        total_aum = large_data['aum'].sum()
        avg_cagr = large_data['cagr'].mean()
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Should complete within reasonable time (adjust threshold as needed)
        assert processing_time < 1.0  # 1 second for 10k records
        assert total_aum > 0
        assert not np.isnan(avg_cagr)
    
    def test_calculation_performance(self):
        """Test performance of financial calculations"""
        import time
        
        calc = PerformanceCalculator()
        
        # Generate large price series
        np.random.seed(42)
        n_days = 2520  # ~10 years of daily data
        returns = np.random.normal(0.001, 0.02, n_days)
        prices = pd.Series(100 * np.cumprod(1 + returns))
        
        start_time = time.time()
        
        # Perform comprehensive calculations
        metrics = calc.calculate_portfolio_metrics(prices)
        
        end_time = time.time()
        calculation_time = end_time - start_time
        
        # Should complete within reasonable time
        assert calculation_time < 2.0  # 2 seconds for 10 years of data
        assert len(metrics) > 10  # Should calculate multiple metrics

if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])

