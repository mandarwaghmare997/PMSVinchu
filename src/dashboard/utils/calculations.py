"""
Performance Calculations Utility for PMS Intelligence Hub
Implements financial calculations for portfolio performance metrics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
import logging
from scipy import stats
import warnings

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class PerformanceCalculator:
    """
    Comprehensive performance calculator for portfolio metrics
    Implements industry-standard financial calculations
    """
    
    def __init__(self):
        self.risk_free_rate = 0.06  # Default 6% risk-free rate (can be configured)
        self.trading_days_per_year = 252
        self.calendar_days_per_year = 365
    
    def calculate_returns(
        self, 
        prices: pd.Series, 
        method: str = 'simple'
    ) -> pd.Series:
        """
        Calculate returns from price series
        
        Args:
            prices: Price series with datetime index
            method: 'simple' or 'log' returns
            
        Returns:
            Returns series
        """
        if method == 'simple':
            returns = prices.pct_change().dropna()
        elif method == 'log':
            returns = np.log(prices / prices.shift(1)).dropna()
        else:
            raise ValueError("Method must be 'simple' or 'log'")
        
        return returns
    
    def calculate_cagr(
        self, 
        beginning_value: float, 
        ending_value: float, 
        periods: float
    ) -> float:
        """
        Calculate Compound Annual Growth Rate (CAGR)
        
        Args:
            beginning_value: Starting portfolio value
            ending_value: Ending portfolio value
            periods: Number of years
            
        Returns:
            CAGR as percentage
        """
        if beginning_value <= 0 or periods <= 0:
            return 0.0
        
        cagr = ((ending_value / beginning_value) ** (1 / periods)) - 1
        return cagr * 100
    
    def calculate_xirr(
        self, 
        cash_flows: List[float], 
        dates: List[datetime],
        guess: float = 0.1
    ) -> float:
        """
        Calculate Extended Internal Rate of Return (XIRR)
        
        Args:
            cash_flows: List of cash flows (negative for outflows, positive for inflows)
            dates: Corresponding dates for cash flows
            guess: Initial guess for IRR calculation
            
        Returns:
            XIRR as percentage
        """
        try:
            from scipy.optimize import newton
            
            if len(cash_flows) != len(dates) or len(cash_flows) < 2:
                return 0.0
            
            # Convert dates to days from first date
            first_date = min(dates)
            days = [(date - first_date).days for date in dates]
            
            def xirr_func(rate):
                return sum(cf / (1 + rate) ** (day / 365.0) for cf, day in zip(cash_flows, days))
            
            # Use Newton's method to find the root
            xirr = newton(xirr_func, guess, maxiter=100)
            return xirr * 100
            
        except Exception as e:
            logger.warning(f"XIRR calculation failed: {str(e)}")
            return 0.0
    
    def calculate_volatility(
        self, 
        returns: pd.Series, 
        annualize: bool = True
    ) -> float:
        """
        Calculate portfolio volatility (standard deviation of returns)
        
        Args:
            returns: Returns series
            annualize: Whether to annualize the volatility
            
        Returns:
            Volatility as percentage
        """
        if len(returns) < 2:
            return 0.0
        
        vol = returns.std()
        
        if annualize:
            # Annualize based on frequency
            if len(returns) > 50:  # Assume daily data
                vol *= np.sqrt(self.trading_days_per_year)
            else:  # Assume monthly data
                vol *= np.sqrt(12)
        
        return vol * 100
    
    def calculate_sharpe_ratio(
        self, 
        returns: pd.Series, 
        risk_free_rate: Optional[float] = None
    ) -> float:
        """
        Calculate Sharpe Ratio
        
        Args:
            returns: Returns series
            risk_free_rate: Risk-free rate (annualized)
            
        Returns:
            Sharpe ratio
        """
        if risk_free_rate is None:
            risk_free_rate = self.risk_free_rate
        
        if len(returns) < 2:
            return 0.0
        
        # Convert risk-free rate to same frequency as returns
        if len(returns) > 50:  # Daily data
            rf_period = risk_free_rate / self.trading_days_per_year
        else:  # Monthly data
            rf_period = risk_free_rate / 12
        
        excess_returns = returns - rf_period
        
        if excess_returns.std() == 0:
            return 0.0
        
        sharpe = excess_returns.mean() / excess_returns.std()
        
        # Annualize
        if len(returns) > 50:  # Daily data
            sharpe *= np.sqrt(self.trading_days_per_year)
        else:  # Monthly data
            sharpe *= np.sqrt(12)
        
        return sharpe
    
    def calculate_sortino_ratio(
        self, 
        returns: pd.Series, 
        target_return: float = 0.0
    ) -> float:
        """
        Calculate Sortino Ratio (downside risk-adjusted return)
        
        Args:
            returns: Returns series
            target_return: Target return threshold
            
        Returns:
            Sortino ratio
        """
        if len(returns) < 2:
            return 0.0
        
        excess_returns = returns - target_return
        downside_returns = excess_returns[excess_returns < 0]
        
        if len(downside_returns) == 0:
            return np.inf
        
        downside_deviation = downside_returns.std()
        
        if downside_deviation == 0:
            return 0.0
        
        sortino = excess_returns.mean() / downside_deviation
        
        # Annualize
        if len(returns) > 50:  # Daily data
            sortino *= np.sqrt(self.trading_days_per_year)
        else:  # Monthly data
            sortino *= np.sqrt(12)
        
        return sortino
    
    def calculate_max_drawdown(self, prices: pd.Series) -> Dict[str, Any]:
        """
        Calculate Maximum Drawdown
        
        Args:
            prices: Price series
            
        Returns:
            Dictionary with max drawdown info
        """
        if len(prices) < 2:
            return {'max_drawdown': 0.0, 'start_date': None, 'end_date': None, 'recovery_date': None}
        
        # Calculate running maximum
        peak = prices.expanding().max()
        
        # Calculate drawdown
        drawdown = (prices - peak) / peak
        
        # Find maximum drawdown
        max_dd = drawdown.min()
        max_dd_date = drawdown.idxmin()
        
        # Find the peak before max drawdown
        peak_date = peak.loc[:max_dd_date].idxmax()
        
        # Find recovery date (if any)
        recovery_date = None
        post_dd_prices = prices.loc[max_dd_date:]
        peak_value = peak.loc[max_dd_date]
        
        recovery_prices = post_dd_prices[post_dd_prices >= peak_value]
        if not recovery_prices.empty:
            recovery_date = recovery_prices.index[0]
        
        return {
            'max_drawdown': max_dd * 100,  # Convert to percentage
            'start_date': peak_date,
            'end_date': max_dd_date,
            'recovery_date': recovery_date,
            'duration_days': (max_dd_date - peak_date).days if peak_date != max_dd_date else 0
        }
    
    def calculate_alpha_beta(
        self, 
        portfolio_returns: pd.Series, 
        benchmark_returns: pd.Series
    ) -> Tuple[float, float]:
        """
        Calculate Alpha and Beta vs benchmark
        
        Args:
            portfolio_returns: Portfolio returns series
            benchmark_returns: Benchmark returns series
            
        Returns:
            Tuple of (alpha, beta)
        """
        if len(portfolio_returns) < 2 or len(benchmark_returns) < 2:
            return 0.0, 1.0
        
        # Align the series
        aligned_data = pd.DataFrame({
            'portfolio': portfolio_returns,
            'benchmark': benchmark_returns
        }).dropna()
        
        if len(aligned_data) < 2:
            return 0.0, 1.0
        
        # Calculate beta using linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            aligned_data['benchmark'], 
            aligned_data['portfolio']
        )
        
        beta = slope
        
        # Calculate alpha (annualized)
        portfolio_mean = aligned_data['portfolio'].mean()
        benchmark_mean = aligned_data['benchmark'].mean()
        
        # Annualize the alpha
        if len(aligned_data) > 50:  # Daily data
            alpha = (portfolio_mean - intercept) * self.trading_days_per_year
        else:  # Monthly data
            alpha = (portfolio_mean - intercept) * 12
        
        return alpha * 100, beta  # Alpha as percentage
    
    def calculate_information_ratio(
        self, 
        portfolio_returns: pd.Series, 
        benchmark_returns: pd.Series
    ) -> float:
        """
        Calculate Information Ratio
        
        Args:
            portfolio_returns: Portfolio returns series
            benchmark_returns: Benchmark returns series
            
        Returns:
            Information ratio
        """
        # Align the series
        aligned_data = pd.DataFrame({
            'portfolio': portfolio_returns,
            'benchmark': benchmark_returns
        }).dropna()
        
        if len(aligned_data) < 2:
            return 0.0
        
        # Calculate active returns
        active_returns = aligned_data['portfolio'] - aligned_data['benchmark']
        
        # Calculate tracking error
        tracking_error = active_returns.std()
        
        if tracking_error == 0:
            return 0.0
        
        # Calculate information ratio
        ir = active_returns.mean() / tracking_error
        
        # Annualize
        if len(aligned_data) > 50:  # Daily data
            ir *= np.sqrt(self.trading_days_per_year)
        else:  # Monthly data
            ir *= np.sqrt(12)
        
        return ir
    
    def calculate_calmar_ratio(
        self, 
        returns: pd.Series, 
        prices: pd.Series
    ) -> float:
        """
        Calculate Calmar Ratio (Annual return / Max Drawdown)
        
        Args:
            returns: Returns series
            prices: Price series
            
        Returns:
            Calmar ratio
        """
        if len(returns) < 2 or len(prices) < 2:
            return 0.0
        
        # Calculate annualized return
        annual_return = returns.mean()
        if len(returns) > 50:  # Daily data
            annual_return *= self.trading_days_per_year
        else:  # Monthly data
            annual_return *= 12
        
        # Calculate max drawdown
        max_dd_info = self.calculate_max_drawdown(prices)
        max_drawdown = abs(max_dd_info['max_drawdown'])
        
        if max_drawdown == 0:
            return np.inf
        
        return (annual_return * 100) / max_drawdown
    
    def calculate_var(
        self, 
        returns: pd.Series, 
        confidence_level: float = 0.95
    ) -> float:
        """
        Calculate Value at Risk (VaR)
        
        Args:
            returns: Returns series
            confidence_level: Confidence level (e.g., 0.95 for 95% VaR)
            
        Returns:
            VaR as percentage
        """
        if len(returns) < 2:
            return 0.0
        
        var = np.percentile(returns, (1 - confidence_level) * 100)
        return var * 100
    
    def calculate_portfolio_metrics(
        self, 
        prices: pd.Series, 
        benchmark_prices: Optional[pd.Series] = None,
        cash_flows: Optional[List[Tuple[datetime, float]]] = None
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive portfolio metrics
        
        Args:
            prices: Portfolio price series
            benchmark_prices: Benchmark price series (optional)
            cash_flows: List of (date, amount) tuples for cash flows
            
        Returns:
            Dictionary of all calculated metrics
        """
        metrics = {}
        
        if len(prices) < 2:
            return self._empty_metrics()
        
        # Calculate returns
        returns = self.calculate_returns(prices)
        
        # Basic metrics
        metrics['total_return'] = ((prices.iloc[-1] / prices.iloc[0]) - 1) * 100
        metrics['annualized_return'] = self.calculate_cagr(
            prices.iloc[0], 
            prices.iloc[-1], 
            (prices.index[-1] - prices.index[0]).days / 365.25
        )
        
        # Risk metrics
        metrics['volatility'] = self.calculate_volatility(returns)
        metrics['sharpe_ratio'] = self.calculate_sharpe_ratio(returns)
        metrics['sortino_ratio'] = self.calculate_sortino_ratio(returns)
        
        # Drawdown metrics
        dd_info = self.calculate_max_drawdown(prices)
        metrics.update(dd_info)
        
        # Calmar ratio
        metrics['calmar_ratio'] = self.calculate_calmar_ratio(returns, prices)
        
        # VaR
        metrics['var_95'] = self.calculate_var(returns, 0.95)
        metrics['var_99'] = self.calculate_var(returns, 0.99)
        
        # XIRR calculation if cash flows provided
        if cash_flows:
            cf_amounts = [cf[1] for cf in cash_flows]
            cf_dates = [cf[0] for cf in cash_flows]
            # Add final value as positive cash flow
            cf_amounts.append(prices.iloc[-1])
            cf_dates.append(prices.index[-1])
            
            metrics['xirr'] = self.calculate_xirr(cf_amounts, cf_dates)
        
        # Benchmark comparison metrics
        if benchmark_prices is not None and len(benchmark_prices) >= 2:
            benchmark_returns = self.calculate_returns(benchmark_prices)
            
            # Align returns
            aligned_data = pd.DataFrame({
                'portfolio': returns,
                'benchmark': benchmark_returns
            }).dropna()
            
            if len(aligned_data) >= 2:
                alpha, beta = self.calculate_alpha_beta(
                    aligned_data['portfolio'], 
                    aligned_data['benchmark']
                )
                metrics['alpha'] = alpha
                metrics['beta'] = beta
                
                metrics['information_ratio'] = self.calculate_information_ratio(
                    aligned_data['portfolio'], 
                    aligned_data['benchmark']
                )
                
                # Tracking error
                active_returns = aligned_data['portfolio'] - aligned_data['benchmark']
                metrics['tracking_error'] = self.calculate_volatility(active_returns)
                
                # Benchmark comparison
                benchmark_total_return = ((benchmark_prices.iloc[-1] / benchmark_prices.iloc[0]) - 1) * 100
                metrics['excess_return'] = metrics['total_return'] - benchmark_total_return
        
        return metrics
    
    def _empty_metrics(self) -> Dict[str, Any]:
        """Return empty metrics dictionary with default values"""
        return {
            'total_return': 0.0,
            'annualized_return': 0.0,
            'volatility': 0.0,
            'sharpe_ratio': 0.0,
            'sortino_ratio': 0.0,
            'max_drawdown': 0.0,
            'calmar_ratio': 0.0,
            'var_95': 0.0,
            'var_99': 0.0,
            'alpha': 0.0,
            'beta': 1.0,
            'information_ratio': 0.0,
            'tracking_error': 0.0,
            'excess_return': 0.0
        }
    
    def calculate_portfolio_attribution(
        self, 
        portfolio_weights: pd.DataFrame, 
        asset_returns: pd.DataFrame,
        benchmark_weights: Optional[pd.DataFrame] = None,
        benchmark_returns: Optional[pd.DataFrame] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Calculate portfolio performance attribution
        
        Args:
            portfolio_weights: Portfolio weights over time
            asset_returns: Asset returns over time
            benchmark_weights: Benchmark weights (optional)
            benchmark_returns: Benchmark returns (optional)
            
        Returns:
            Dictionary with attribution analysis
        """
        # This is a simplified attribution analysis
        # In practice, this would be much more complex
        
        attribution = {}
        
        # Calculate contribution to return
        contribution = portfolio_weights.shift(1) * asset_returns
        attribution['asset_contribution'] = contribution.sum(axis=1)
        
        # Calculate sector/asset level attribution
        attribution['individual_contribution'] = contribution
        
        return attribution
    
    def calculate_risk_metrics(
        self, 
        returns: pd.Series,
        benchmark_returns: Optional[pd.Series] = None
    ) -> Dict[str, float]:
        """
        Calculate comprehensive risk metrics
        
        Args:
            returns: Portfolio returns
            benchmark_returns: Benchmark returns (optional)
            
        Returns:
            Dictionary of risk metrics
        """
        risk_metrics = {}
        
        if len(returns) < 2:
            return {}
        
        # Basic risk metrics
        risk_metrics['volatility'] = self.calculate_volatility(returns)
        risk_metrics['downside_deviation'] = self.calculate_volatility(returns[returns < 0])
        risk_metrics['var_95'] = self.calculate_var(returns, 0.95)
        risk_metrics['var_99'] = self.calculate_var(returns, 0.99)
        
        # Skewness and Kurtosis
        risk_metrics['skewness'] = returns.skew()
        risk_metrics['kurtosis'] = returns.kurtosis()
        
        # Risk-adjusted returns
        risk_metrics['sharpe_ratio'] = self.calculate_sharpe_ratio(returns)
        risk_metrics['sortino_ratio'] = self.calculate_sortino_ratio(returns)
        
        # Benchmark relative metrics
        if benchmark_returns is not None:
            aligned_data = pd.DataFrame({
                'portfolio': returns,
                'benchmark': benchmark_returns
            }).dropna()
            
            if len(aligned_data) >= 2:
                active_returns = aligned_data['portfolio'] - aligned_data['benchmark']
                risk_metrics['tracking_error'] = self.calculate_volatility(active_returns)
                risk_metrics['information_ratio'] = self.calculate_information_ratio(
                    aligned_data['portfolio'], 
                    aligned_data['benchmark']
                )
        
        return risk_metrics

# Utility functions for common calculations
def calculate_simple_return(start_value: float, end_value: float) -> float:
    """Calculate simple return percentage"""
    if start_value <= 0:
        return 0.0
    return ((end_value / start_value) - 1) * 100

def calculate_compound_return(returns: List[float]) -> float:
    """Calculate compound return from list of period returns"""
    if not returns:
        return 0.0
    
    compound = 1.0
    for ret in returns:
        compound *= (1 + ret / 100)
    
    return (compound - 1) * 100

def annualize_return(return_rate: float, periods_per_year: int) -> float:
    """Annualize a return rate"""
    return ((1 + return_rate / 100) ** periods_per_year - 1) * 100

def calculate_weighted_average(values: List[float], weights: List[float]) -> float:
    """Calculate weighted average"""
    if len(values) != len(weights) or sum(weights) == 0:
        return 0.0
    
    return sum(v * w for v, w in zip(values, weights)) / sum(weights)

# Export main classes and functions
__all__ = [
    'PerformanceCalculator',
    'calculate_simple_return',
    'calculate_compound_return',
    'annualize_return',
    'calculate_weighted_average'
]

