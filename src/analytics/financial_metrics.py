"""
Advanced Financial Metrics and Analytics Module
Comprehensive financial calculations for Portfolio Management Services
Author: Vulnuris Development Team
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
import warnings
warnings.filterwarnings('ignore')

class AdvancedFinancialMetrics:
    """
    Comprehensive financial metrics calculator for portfolio management
    Implements industry-standard calculations following CFA Institute guidelines
    """
    
    def __init__(self, risk_free_rate: float = 0.06):
        """
        Initialize with risk-free rate (default 6% for Indian market)
        """
        self.risk_free_rate = risk_free_rate
    
    def calculate_returns(self, prices: pd.Series, method: str = 'simple') -> pd.Series:
        """
        Calculate returns from price series
        
        Args:
            prices: Series of prices
            method: 'simple' or 'log' returns
        
        Returns:
            Series of returns
        """
        if method == 'log':
            return np.log(prices / prices.shift(1)).dropna()
        else:
            return (prices / prices.shift(1) - 1).dropna()
    
    def annualized_return(self, returns: pd.Series, periods_per_year: int = 252) -> float:
        """
        Calculate annualized return
        
        Args:
            returns: Series of periodic returns
            periods_per_year: Number of periods in a year (252 for daily, 12 for monthly)
        
        Returns:
            Annualized return
        """
        if len(returns) == 0:
            return 0.0
        
        total_return = (1 + returns).prod() - 1
        years = len(returns) / periods_per_year
        
        if years <= 0:
            return 0.0
        
        return (1 + total_return) ** (1 / years) - 1
    
    def annualized_volatility(self, returns: pd.Series, periods_per_year: int = 252) -> float:
        """
        Calculate annualized volatility (standard deviation)
        
        Args:
            returns: Series of periodic returns
            periods_per_year: Number of periods in a year
        
        Returns:
            Annualized volatility
        """
        if len(returns) <= 1:
            return 0.0
        
        return returns.std() * np.sqrt(periods_per_year)
    
    def sharpe_ratio(self, returns: pd.Series, periods_per_year: int = 252) -> float:
        """
        Calculate Sharpe ratio
        
        Args:
            returns: Series of periodic returns
            periods_per_year: Number of periods in a year
        
        Returns:
            Sharpe ratio
        """
        if len(returns) <= 1:
            return 0.0
        
        excess_returns = returns - (self.risk_free_rate / periods_per_year)
        
        if excess_returns.std() == 0:
            return 0.0
        
        return excess_returns.mean() / excess_returns.std() * np.sqrt(periods_per_year)
    
    def sortino_ratio(self, returns: pd.Series, periods_per_year: int = 252) -> float:
        """
        Calculate Sortino ratio (downside deviation)
        
        Args:
            returns: Series of periodic returns
            periods_per_year: Number of periods in a year
        
        Returns:
            Sortino ratio
        """
        if len(returns) <= 1:
            return 0.0
        
        excess_returns = returns - (self.risk_free_rate / periods_per_year)
        downside_returns = excess_returns[excess_returns < 0]
        
        if len(downside_returns) == 0 or downside_returns.std() == 0:
            return 0.0
        
        downside_deviation = downside_returns.std() * np.sqrt(periods_per_year)
        annualized_excess = excess_returns.mean() * periods_per_year
        
        return annualized_excess / downside_deviation
    
    def calmar_ratio(self, returns: pd.Series, periods_per_year: int = 252) -> float:
        """
        Calculate Calmar ratio (return / max drawdown)
        
        Args:
            returns: Series of periodic returns
            periods_per_year: Number of periods in a year
        
        Returns:
            Calmar ratio
        """
        if len(returns) <= 1:
            return 0.0
        
        ann_return = self.annualized_return(returns, periods_per_year)
        max_dd = self.maximum_drawdown(returns)
        
        if max_dd == 0:
            return 0.0
        
        return ann_return / abs(max_dd)
    
    def maximum_drawdown(self, returns: pd.Series) -> float:
        """
        Calculate maximum drawdown
        
        Args:
            returns: Series of periodic returns
        
        Returns:
            Maximum drawdown (negative value)
        """
        if len(returns) == 0:
            return 0.0
        
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        
        return drawdown.min()
    
    def value_at_risk(self, returns: pd.Series, confidence_level: float = 0.05) -> float:
        """
        Calculate Value at Risk (VaR)
        
        Args:
            returns: Series of periodic returns
            confidence_level: Confidence level (0.05 for 95% VaR)
        
        Returns:
            Value at Risk
        """
        if len(returns) == 0:
            return 0.0
        
        return np.percentile(returns, confidence_level * 100)
    
    def conditional_var(self, returns: pd.Series, confidence_level: float = 0.05) -> float:
        """
        Calculate Conditional Value at Risk (CVaR) / Expected Shortfall
        
        Args:
            returns: Series of periodic returns
            confidence_level: Confidence level (0.05 for 95% CVaR)
        
        Returns:
            Conditional Value at Risk
        """
        if len(returns) == 0:
            return 0.0
        
        var = self.value_at_risk(returns, confidence_level)
        return returns[returns <= var].mean()
    
    def beta(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """
        Calculate Beta (systematic risk)
        
        Args:
            portfolio_returns: Series of portfolio returns
            benchmark_returns: Series of benchmark returns
        
        Returns:
            Beta coefficient
        """
        if len(portfolio_returns) != len(benchmark_returns) or len(portfolio_returns) <= 1:
            return 1.0
        
        # Align the series
        aligned_data = pd.DataFrame({
            'portfolio': portfolio_returns,
            'benchmark': benchmark_returns
        }).dropna()
        
        if len(aligned_data) <= 1:
            return 1.0
        
        covariance = aligned_data['portfolio'].cov(aligned_data['benchmark'])
        benchmark_variance = aligned_data['benchmark'].var()
        
        if benchmark_variance == 0:
            return 1.0
        
        return covariance / benchmark_variance
    
    def alpha(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series, 
              periods_per_year: int = 252) -> float:
        """
        Calculate Alpha (excess return over CAPM)
        
        Args:
            portfolio_returns: Series of portfolio returns
            benchmark_returns: Series of benchmark returns
            periods_per_year: Number of periods in a year
        
        Returns:
            Alpha (annualized)
        """
        if len(portfolio_returns) != len(benchmark_returns) or len(portfolio_returns) <= 1:
            return 0.0
        
        portfolio_return = self.annualized_return(portfolio_returns, periods_per_year)
        benchmark_return = self.annualized_return(benchmark_returns, periods_per_year)
        beta_coeff = self.beta(portfolio_returns, benchmark_returns)
        
        expected_return = self.risk_free_rate + beta_coeff * (benchmark_return - self.risk_free_rate)
        
        return portfolio_return - expected_return
    
    def tracking_error(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series,
                      periods_per_year: int = 252) -> float:
        """
        Calculate tracking error (volatility of excess returns)
        
        Args:
            portfolio_returns: Series of portfolio returns
            benchmark_returns: Series of benchmark returns
            periods_per_year: Number of periods in a year
        
        Returns:
            Tracking error (annualized)
        """
        if len(portfolio_returns) != len(benchmark_returns) or len(portfolio_returns) <= 1:
            return 0.0
        
        # Align the series
        aligned_data = pd.DataFrame({
            'portfolio': portfolio_returns,
            'benchmark': benchmark_returns
        }).dropna()
        
        if len(aligned_data) <= 1:
            return 0.0
        
        excess_returns = aligned_data['portfolio'] - aligned_data['benchmark']
        
        return excess_returns.std() * np.sqrt(periods_per_year)
    
    def information_ratio(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series,
                         periods_per_year: int = 252) -> float:
        """
        Calculate Information Ratio (excess return / tracking error)
        
        Args:
            portfolio_returns: Series of portfolio returns
            benchmark_returns: Series of benchmark returns
            periods_per_year: Number of periods in a year
        
        Returns:
            Information ratio
        """
        if len(portfolio_returns) != len(benchmark_returns) or len(portfolio_returns) <= 1:
            return 0.0
        
        # Align the series
        aligned_data = pd.DataFrame({
            'portfolio': portfolio_returns,
            'benchmark': benchmark_returns
        }).dropna()
        
        if len(aligned_data) <= 1:
            return 0.0
        
        excess_returns = aligned_data['portfolio'] - aligned_data['benchmark']
        excess_return_ann = excess_returns.mean() * periods_per_year
        tracking_err = self.tracking_error(portfolio_returns, benchmark_returns, periods_per_year)
        
        if tracking_err == 0:
            return 0.0
        
        return excess_return_ann / tracking_err
    
    def treynor_ratio(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series,
                     periods_per_year: int = 252) -> float:
        """
        Calculate Treynor Ratio (excess return / beta)
        
        Args:
            portfolio_returns: Series of portfolio returns
            benchmark_returns: Series of benchmark returns
            periods_per_year: Number of periods in a year
        
        Returns:
            Treynor ratio
        """
        if len(portfolio_returns) <= 1:
            return 0.0
        
        portfolio_return = self.annualized_return(portfolio_returns, periods_per_year)
        beta_coeff = self.beta(portfolio_returns, benchmark_returns)
        
        if beta_coeff == 0:
            return 0.0
        
        return (portfolio_return - self.risk_free_rate) / beta_coeff
    
    def up_capture_ratio(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """
        Calculate Up Capture Ratio
        
        Args:
            portfolio_returns: Series of portfolio returns
            benchmark_returns: Series of benchmark returns
        
        Returns:
            Up capture ratio
        """
        if len(portfolio_returns) != len(benchmark_returns) or len(portfolio_returns) <= 1:
            return 1.0
        
        # Align the series
        aligned_data = pd.DataFrame({
            'portfolio': portfolio_returns,
            'benchmark': benchmark_returns
        }).dropna()
        
        if len(aligned_data) <= 1:
            return 1.0
        
        up_periods = aligned_data[aligned_data['benchmark'] > 0]
        
        if len(up_periods) == 0:
            return 1.0
        
        portfolio_up = (1 + up_periods['portfolio']).prod() - 1
        benchmark_up = (1 + up_periods['benchmark']).prod() - 1
        
        if benchmark_up == 0:
            return 1.0
        
        return portfolio_up / benchmark_up
    
    def down_capture_ratio(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """
        Calculate Down Capture Ratio
        
        Args:
            portfolio_returns: Series of portfolio returns
            benchmark_returns: Series of benchmark returns
        
        Returns:
            Down capture ratio
        """
        if len(portfolio_returns) != len(benchmark_returns) or len(portfolio_returns) <= 1:
            return 1.0
        
        # Align the series
        aligned_data = pd.DataFrame({
            'portfolio': portfolio_returns,
            'benchmark': benchmark_returns
        }).dropna()
        
        if len(aligned_data) <= 1:
            return 1.0
        
        down_periods = aligned_data[aligned_data['benchmark'] < 0]
        
        if len(down_periods) == 0:
            return 1.0
        
        portfolio_down = (1 + down_periods['portfolio']).prod() - 1
        benchmark_down = (1 + down_periods['benchmark']).prod() - 1
        
        if benchmark_down == 0:
            return 1.0
        
        return portfolio_down / benchmark_down
    
    def high_water_mark(self, returns: pd.Series) -> Dict[str, float]:
        """
        Calculate High Water Mark metrics
        
        Args:
            returns: Series of periodic returns
        
        Returns:
            Dictionary with HWM metrics
        """
        if len(returns) == 0:
            return {
                'current_hwm': 1.0,
                'current_value': 1.0,
                'hwm_date': None,
                'days_since_hwm': 0,
                'drawdown_from_hwm': 0.0
            }
        
        cumulative = (1 + returns).cumprod()
        hwm_series = cumulative.expanding().max()
        
        current_hwm = hwm_series.iloc[-1]
        current_value = cumulative.iloc[-1]
        hwm_date = cumulative[cumulative == current_hwm].index[-1]
        
        # Calculate days since HWM
        if isinstance(returns.index, pd.DatetimeIndex):
            days_since_hwm = (returns.index[-1] - hwm_date).days
        else:
            days_since_hwm = len(returns) - returns.index.get_loc(hwm_date)
        
        drawdown_from_hwm = (current_value - current_hwm) / current_hwm
        
        return {
            'current_hwm': current_hwm,
            'current_value': current_value,
            'hwm_date': hwm_date,
            'days_since_hwm': days_since_hwm,
            'drawdown_from_hwm': drawdown_from_hwm
        }
    
    def calculate_comprehensive_metrics(self, portfolio_data: pd.DataFrame, 
                                      benchmark_data: pd.DataFrame = None) -> Dict[str, float]:
        """
        Calculate comprehensive set of financial metrics
        
        Args:
            portfolio_data: DataFrame with portfolio data
            benchmark_data: DataFrame with benchmark data (optional)
        
        Returns:
            Dictionary with all calculated metrics
        """
        metrics = {}
        
        # Ensure we have returns data
        if 'returns' not in portfolio_data.columns:
            if 'portfolio_value' in portfolio_data.columns:
                portfolio_returns = self.calculate_returns(portfolio_data['portfolio_value'])
            else:
                # Generate synthetic returns for demonstration
                portfolio_returns = pd.Series(np.random.normal(0.001, 0.02, 252))
        else:
            portfolio_returns = portfolio_data['returns'].dropna()
        
        # Basic metrics
        metrics['annualized_return'] = self.annualized_return(portfolio_returns)
        metrics['annualized_volatility'] = self.annualized_volatility(portfolio_returns)
        metrics['sharpe_ratio'] = self.sharpe_ratio(portfolio_returns)
        metrics['sortino_ratio'] = self.sortino_ratio(portfolio_returns)
        metrics['calmar_ratio'] = self.calmar_ratio(portfolio_returns)
        metrics['maximum_drawdown'] = self.maximum_drawdown(portfolio_returns)
        
        # Risk metrics
        metrics['var_95'] = self.value_at_risk(portfolio_returns, 0.05)
        metrics['var_99'] = self.value_at_risk(portfolio_returns, 0.01)
        metrics['cvar_95'] = self.conditional_var(portfolio_returns, 0.05)
        metrics['cvar_99'] = self.conditional_var(portfolio_returns, 0.01)
        
        # High Water Mark
        hwm_metrics = self.high_water_mark(portfolio_returns)
        metrics.update({f'hwm_{k}': v for k, v in hwm_metrics.items()})
        
        # Benchmark-relative metrics (if benchmark provided)
        if benchmark_data is not None:
            if 'returns' not in benchmark_data.columns:
                if 'benchmark_value' in benchmark_data.columns:
                    benchmark_returns = self.calculate_returns(benchmark_data['benchmark_value'])
                else:
                    # Generate synthetic benchmark returns
                    benchmark_returns = pd.Series(np.random.normal(0.0008, 0.015, 252))
            else:
                benchmark_returns = benchmark_data['returns'].dropna()
            
            metrics['beta'] = self.beta(portfolio_returns, benchmark_returns)
            metrics['alpha'] = self.alpha(portfolio_returns, benchmark_returns)
            metrics['tracking_error'] = self.tracking_error(portfolio_returns, benchmark_returns)
            metrics['information_ratio'] = self.information_ratio(portfolio_returns, benchmark_returns)
            metrics['treynor_ratio'] = self.treynor_ratio(portfolio_returns, benchmark_returns)
            metrics['up_capture_ratio'] = self.up_capture_ratio(portfolio_returns, benchmark_returns)
            metrics['down_capture_ratio'] = self.down_capture_ratio(portfolio_returns, benchmark_returns)
        
        return metrics

class PortfolioAttributionAnalysis:
    """
    Portfolio attribution analysis for performance decomposition
    """
    
    def __init__(self):
        pass
    
    def sector_attribution(self, portfolio_weights: pd.DataFrame, 
                          benchmark_weights: pd.DataFrame,
                          sector_returns: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate sector attribution analysis
        
        Args:
            portfolio_weights: DataFrame with portfolio sector weights
            benchmark_weights: DataFrame with benchmark sector weights  
            sector_returns: DataFrame with sector returns
        
        Returns:
            DataFrame with attribution results
        """
        # Align all dataframes
        common_sectors = portfolio_weights.columns.intersection(
            benchmark_weights.columns).intersection(sector_returns.columns)
        
        if len(common_sectors) == 0:
            return pd.DataFrame()
        
        pw = portfolio_weights[common_sectors].fillna(0)
        bw = benchmark_weights[common_sectors].fillna(0)
        sr = sector_returns[common_sectors].fillna(0)
        
        # Calculate attribution components
        allocation_effect = (pw - bw) * sr
        selection_effect = bw * (sr - sr.mean(axis=1).values.reshape(-1, 1))
        interaction_effect = (pw - bw) * (sr - sr.mean(axis=1).values.reshape(-1, 1))
        
        attribution_df = pd.DataFrame({
            'allocation_effect': allocation_effect.sum(axis=1),
            'selection_effect': selection_effect.sum(axis=1),
            'interaction_effect': interaction_effect.sum(axis=1)
        })
        
        attribution_df['total_effect'] = (attribution_df['allocation_effect'] + 
                                        attribution_df['selection_effect'] + 
                                        attribution_df['interaction_effect'])
        
        return attribution_df
    
    def style_attribution(self, portfolio_exposures: pd.DataFrame,
                         benchmark_exposures: pd.DataFrame,
                         factor_returns: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate style attribution analysis
        
        Args:
            portfolio_exposures: DataFrame with portfolio factor exposures
            benchmark_exposures: DataFrame with benchmark factor exposures
            factor_returns: DataFrame with factor returns
        
        Returns:
            DataFrame with style attribution results
        """
        # Align dataframes
        common_factors = portfolio_exposures.columns.intersection(
            benchmark_exposures.columns).intersection(factor_returns.columns)
        
        if len(common_factors) == 0:
            return pd.DataFrame()
        
        pe = portfolio_exposures[common_factors].fillna(0)
        be = benchmark_exposures[common_factors].fillna(0)
        fr = factor_returns[common_factors].fillna(0)
        
        # Calculate style attribution
        style_attribution = (pe - be) * fr
        
        attribution_df = pd.DataFrame({
            'style_attribution': style_attribution.sum(axis=1)
        })
        
        # Add individual factor contributions
        for factor in common_factors:
            attribution_df[f'{factor}_contribution'] = (pe[factor] - be[factor]) * fr[factor]
        
        return attribution_df

def generate_performance_time_series(start_date: str, end_date: str, 
                                   initial_value: float = 100,
                                   annual_return: float = 0.12,
                                   annual_volatility: float = 0.15) -> pd.DataFrame:
    """
    Generate realistic performance time series for testing
    
    Args:
        start_date: Start date string
        end_date: End date string
        initial_value: Initial portfolio value
        annual_return: Expected annual return
        annual_volatility: Annual volatility
    
    Returns:
        DataFrame with performance time series
    """
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    n_days = len(dates)
    
    # Generate daily returns
    daily_return = annual_return / 252
    daily_volatility = annual_volatility / np.sqrt(252)
    
    daily_returns = np.random.normal(daily_return, daily_volatility, n_days)
    
    # Calculate cumulative values
    cumulative_returns = np.cumprod(1 + daily_returns)
    portfolio_values = initial_value * cumulative_returns
    
    # Create benchmark (slightly lower return, lower volatility)
    benchmark_returns = np.random.normal(daily_return * 0.9, daily_volatility * 0.8, n_days)
    benchmark_values = initial_value * np.cumprod(1 + benchmark_returns)
    
    df = pd.DataFrame({
        'date': dates,
        'portfolio_value': portfolio_values,
        'portfolio_returns': daily_returns,
        'benchmark_value': benchmark_values,
        'benchmark_returns': benchmark_returns
    })
    
    df.set_index('date', inplace=True)
    
    return df

