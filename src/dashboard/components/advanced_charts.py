"""
Advanced Chart Components for PMS Intelligence Hub
Optimized charting library with professional financial visualizations
Author: Vulnuris Development Team
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
import streamlit as st

class OptimizedChartGenerator:
    """
    Optimized chart generator with caching and performance improvements
    """
    
    def __init__(self):
        self.color_palette = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e', 
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff7f0e',
            'info': '#17becf',
            'light': '#7f7f7f',
            'dark': '#1f1f1f'
        }
        
        self.chart_config = {
            'displayModeBar': False,
            'responsive': True,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'pms_chart',
                'height': 500,
                'width': 700,
                'scale': 1
            }
        }
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def create_performance_comparison_chart(_self, portfolio_data: pd.DataFrame, 
                                          benchmark_data: pd.DataFrame = None,
                                          title: str = "Portfolio Performance") -> go.Figure:
        """
        Create optimized performance comparison chart
        """
        fig = go.Figure()
        
        # Portfolio line
        fig.add_trace(go.Scatter(
            x=portfolio_data.index,
            y=portfolio_data['portfolio_value'] if 'portfolio_value' in portfolio_data.columns else portfolio_data.iloc[:, 0],
            mode='lines',
            name='Portfolio',
            line=dict(color=_self.color_palette['primary'], width=2),
            hovertemplate='<b>Portfolio</b><br>Date: %{x}<br>Value: %{y:.2f}<extra></extra>'
        ))
        
        # Benchmark line (if provided)
        if benchmark_data is not None:
            fig.add_trace(go.Scatter(
                x=benchmark_data.index,
                y=benchmark_data['benchmark_value'] if 'benchmark_value' in benchmark_data.columns else benchmark_data.iloc[:, 0],
                mode='lines',
                name='Benchmark',
                line=dict(color=_self.color_palette['secondary'], width=2, dash='dash'),
                hovertemplate='<b>Benchmark</b><br>Date: %{x}<br>Value: %{y:.2f}<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=16, color=_self.color_palette['dark'])),
            xaxis_title="Date",
            yaxis_title="Portfolio Value",
            template="plotly_white",
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    @st.cache_data(ttl=300)
    def create_risk_return_scatter(_self, data: pd.DataFrame, 
                                 size_column: str = 'current_aum',
                                 color_column: str = 'portfolio_type',
                                 title: str = "Risk-Return Analysis") -> go.Figure:
        """
        Create optimized risk-return scatter plot
        """
        fig = px.scatter(
            data,
            x='benchmark_returns',
            y='annualized_returns', 
            size=size_column,
            color=color_column,
            hover_data=['client_name', 'rm_name'],
            title=title,
            labels={
                'benchmark_returns': 'Benchmark Returns (%)',
                'annualized_returns': 'Portfolio Returns (%)',
                size_column: 'AUM (Cr)'
            },
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        # Add diagonal line for benchmark
        min_val = min(data['benchmark_returns'].min(), data['annualized_returns'].min())
        max_val = max(data['benchmark_returns'].max(), data['annualized_returns'].max())
        
        fig.add_shape(
            type="line",
            x0=min_val, y0=min_val,
            x1=max_val, y1=max_val,
            line=dict(color="red", width=2, dash="dash"),
            name="Benchmark Line"
        )
        
        fig.update_layout(
            template="plotly_white",
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig
    
    @st.cache_data(ttl=300)
    def create_drawdown_chart(_self, returns_data: pd.Series, 
                            title: str = "Drawdown Analysis") -> go.Figure:
        """
        Create optimized drawdown chart
        """
        # Calculate cumulative returns and drawdown
        cumulative = (1 + returns_data).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max * 100
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Cumulative Returns', 'Drawdown (%)'),
            vertical_spacing=0.1,
            row_heights=[0.6, 0.4]
        )
        
        # Cumulative returns
        fig.add_trace(
            go.Scatter(
                x=cumulative.index,
                y=cumulative.values,
                mode='lines',
                name='Cumulative Returns',
                line=dict(color=_self.color_palette['primary'], width=2)
            ),
            row=1, col=1
        )
        
        # Drawdown
        fig.add_trace(
            go.Scatter(
                x=drawdown.index,
                y=drawdown.values,
                mode='lines',
                name='Drawdown',
                fill='tonexty',
                line=dict(color=_self.color_palette['danger'], width=1),
                fillcolor='rgba(214, 39, 40, 0.3)'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title=dict(text=title, x=0.5),
            template="plotly_white",
            height=500,
            showlegend=False,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig
    
    @st.cache_data(ttl=300)
    def create_correlation_heatmap(_self, correlation_matrix: pd.DataFrame,
                                 title: str = "Correlation Matrix") -> go.Figure:
        """
        Create optimized correlation heatmap
        """
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale='RdBu',
            zmid=0,
            text=correlation_matrix.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 10},
            hovertemplate='<b>%{y} vs %{x}</b><br>Correlation: %{z:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=title, x=0.5),
            template="plotly_white",
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig
    
    @st.cache_data(ttl=300)
    def create_rolling_metrics_chart(_self, data: pd.DataFrame, 
                                   metric: str = 'sharpe_ratio',
                                   window: int = 252,
                                   title: str = "Rolling Metrics") -> go.Figure:
        """
        Create optimized rolling metrics chart
        """
        if 'returns' not in data.columns:
            return go.Figure()
        
        returns = data['returns'].dropna()
        
        # Calculate rolling metric
        if metric == 'sharpe_ratio':
            rolling_metric = returns.rolling(window).apply(
                lambda x: (x.mean() * 252) / (x.std() * np.sqrt(252)) if x.std() > 0 else 0
            )
            y_title = "Sharpe Ratio"
        elif metric == 'volatility':
            rolling_metric = returns.rolling(window).std() * np.sqrt(252)
            y_title = "Volatility (%)"
        else:
            rolling_metric = returns.rolling(window).mean() * 252
            y_title = "Annualized Return (%)"
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=rolling_metric.index,
            y=rolling_metric.values,
            mode='lines',
            name=f'Rolling {metric.replace("_", " ").title()}',
            line=dict(color=_self.color_palette['primary'], width=2),
            hovertemplate=f'<b>{y_title}</b><br>Date: %{{x}}<br>Value: %{{y:.3f}}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=title, x=0.5),
            xaxis_title="Date",
            yaxis_title=y_title,
            template="plotly_white",
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig
    
    @st.cache_data(ttl=300)
    def create_sector_allocation_chart(_self, allocation_data: pd.DataFrame,
                                     title: str = "Sector Allocation") -> go.Figure:
        """
        Create optimized sector allocation chart
        """
        fig = go.Figure(data=[
            go.Pie(
                labels=allocation_data.index,
                values=allocation_data.values,
                hole=0.4,
                textinfo='label+percent',
                textposition='outside',
                marker=dict(
                    colors=px.colors.qualitative.Set3,
                    line=dict(color='#FFFFFF', width=2)
                ),
                hovertemplate='<b>%{label}</b><br>Allocation: %{value:.1f}%<br>Percentage: %{percent}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=dict(text=title, x=0.5),
            template="plotly_white",
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
        )
        
        return fig
    
    @st.cache_data(ttl=300)
    def create_performance_attribution_chart(_self, attribution_data: pd.DataFrame,
                                           title: str = "Performance Attribution") -> go.Figure:
        """
        Create optimized performance attribution waterfall chart
        """
        categories = attribution_data.index.tolist()
        values = attribution_data.values.flatten()
        
        # Calculate cumulative values for waterfall
        cumulative = np.cumsum([0] + values.tolist())
        
        fig = go.Figure()
        
        # Add bars for each component
        for i, (category, value) in enumerate(zip(categories, values)):
            color = _self.color_palette['success'] if value >= 0 else _self.color_palette['danger']
            
            fig.add_trace(go.Bar(
                x=[category],
                y=[value],
                name=category,
                marker_color=color,
                text=[f'{value:.2f}%'],
                textposition='outside',
                hovertemplate=f'<b>{category}</b><br>Contribution: %{{y:.3f}}%<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(text=title, x=0.5),
            xaxis_title="Attribution Components",
            yaxis_title="Contribution (%)",
            template="plotly_white",
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
            showlegend=False
        )
        
        return fig
    
    def create_metrics_gauge_chart(self, value: float, title: str, 
                                 min_val: float = 0, max_val: float = 100,
                                 threshold_good: float = 70, 
                                 threshold_excellent: float = 90) -> go.Figure:
        """
        Create optimized gauge chart for metrics
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title, 'font': {'size': 16}},
            delta={'reference': threshold_good},
            gauge={
                'axis': {'range': [None, max_val]},
                'bar': {'color': self.color_palette['primary']},
                'steps': [
                    {'range': [min_val, threshold_good], 'color': "lightgray"},
                    {'range': [threshold_good, threshold_excellent], 'color': "yellow"},
                    {'range': [threshold_excellent, max_val], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': threshold_excellent
                }
            }
        ))
        
        fig.update_layout(
            template="plotly_white",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig

class ChartOptimizer:
    """
    Chart optimization utilities for performance improvement
    """
    
    @staticmethod
    def optimize_dataframe_for_charts(df: pd.DataFrame, max_points: int = 1000) -> pd.DataFrame:
        """
        Optimize dataframe for chart rendering by reducing data points if necessary
        """
        if len(df) <= max_points:
            return df
        
        # Sample data points evenly
        step = len(df) // max_points
        return df.iloc[::step].copy()
    
    @staticmethod
    def prepare_time_series_data(df: pd.DataFrame, date_column: str = None) -> pd.DataFrame:
        """
        Prepare time series data for optimal chart performance
        """
        if date_column and date_column in df.columns:
            df = df.copy()
            df[date_column] = pd.to_datetime(df[date_column])
            df.set_index(date_column, inplace=True)
        
        # Remove any infinite or NaN values
        df = df.replace([np.inf, -np.inf], np.nan).dropna()
        
        return df
    
    @staticmethod
    def calculate_chart_dimensions(container_width: int = 800) -> Tuple[int, int]:
        """
        Calculate optimal chart dimensions based on container
        """
        width = min(container_width, 1200)
        height = int(width * 0.6)  # 16:10 aspect ratio
        return width, height

