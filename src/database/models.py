"""
Database Models for PMS Intelligence Hub
Defines SQLAlchemy models for all entities in the system
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, DateTime, Date, Numeric, Boolean, 
    Text, ForeignKey, Index, UniqueConstraint, CheckConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

Base = declarative_base()

class TimestampMixin:
    """Mixin for created_at and updated_at timestamps"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Client(Base, TimestampMixin):
    """Client master table - stores all client information"""
    __tablename__ = 'clients'
    
    # Primary Key
    client_id = Column(String(50), primary_key=True)
    
    # Basic Information
    client_name = Column(String(200), nullable=False)
    client_type = Column(String(50), nullable=False)  # Individual, HUF, Corporate, Trust
    pan_number = Column(String(10), unique=True)
    aadhaar_number = Column(String(12))
    
    # Contact Information
    email = Column(String(100))
    phone = Column(String(15))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100), default='India')
    pincode = Column(String(10))
    
    # Business Information
    onboarding_date = Column(Date, nullable=False)
    relationship_manager_id = Column(String(50), ForeignKey('relationship_managers.rm_id'))
    risk_profile = Column(String(20))  # Conservative, Moderate, Aggressive
    investment_objective = Column(String(100))
    
    # Status and Compliance
    status = Column(String(20), default='Active')  # Active, Inactive, Suspended
    kyc_status = Column(String(20), default='Pending')  # Pending, Verified, Expired
    kyc_expiry_date = Column(Date)
    
    # Salesforce Integration
    salesforce_id = Column(String(50), unique=True)
    salesforce_last_sync = Column(DateTime)
    
    # Relationships
    relationship_manager = relationship("RelationshipManager", back_populates="clients")
    portfolios = relationship("Portfolio", back_populates="client")
    transactions = relationship("Transaction", back_populates="client")
    
    # Indexes
    __table_args__ = (
        Index('idx_client_name', 'client_name'),
        Index('idx_client_rm', 'relationship_manager_id'),
        Index('idx_client_status', 'status'),
        Index('idx_client_onboarding', 'onboarding_date'),
        Index('idx_salesforce_id', 'salesforce_id'),
    )

class RelationshipManager(Base, TimestampMixin):
    """Relationship Manager master table"""
    __tablename__ = 'relationship_managers'
    
    # Primary Key
    rm_id = Column(String(50), primary_key=True)
    
    # Basic Information
    rm_name = Column(String(100), nullable=False)
    employee_id = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    phone = Column(String(15))
    
    # Hierarchy
    manager_id = Column(String(50), ForeignKey('relationship_managers.rm_id'))
    department = Column(String(100))
    designation = Column(String(100))
    
    # Status
    status = Column(String(20), default='Active')
    joining_date = Column(Date)
    
    # Relationships
    manager = relationship("RelationshipManager", remote_side=[rm_id])
    clients = relationship("Client", back_populates="relationship_manager")
    
    # Indexes
    __table_args__ = (
        Index('idx_rm_name', 'rm_name'),
        Index('idx_rm_status', 'status'),
    )

class Portfolio(Base, TimestampMixin):
    """Portfolio master table - each client can have multiple portfolios"""
    __tablename__ = 'portfolios'
    
    # Primary Key
    portfolio_id = Column(String(50), primary_key=True)
    
    # Client Reference
    client_id = Column(String(50), ForeignKey('clients.client_id'), nullable=False)
    
    # Portfolio Information
    portfolio_name = Column(String(200), nullable=False)
    portfolio_type = Column(String(50), nullable=False)  # PMS, AIF, Discretionary
    investment_strategy = Column(String(100))
    benchmark_id = Column(String(50), ForeignKey('benchmarks.benchmark_id'))
    
    # Financial Information
    inception_date = Column(Date, nullable=False)
    initial_investment = Column(Numeric(15, 2), default=0)
    minimum_investment = Column(Numeric(15, 2), default=0)
    
    # Fee Structure
    management_fee_rate = Column(Numeric(5, 4), default=0)  # As decimal (e.g., 0.02 for 2%)
    performance_fee_rate = Column(Numeric(5, 4), default=0)
    high_watermark = Column(Numeric(15, 2), default=0)
    
    # Status
    status = Column(String(20), default='Active')
    closure_date = Column(Date)
    closure_reason = Column(String(200))
    
    # Wealth Spectrum Integration
    wealth_spectrum_id = Column(String(50), unique=True)
    wealth_spectrum_last_sync = Column(DateTime)
    
    # Relationships
    client = relationship("Client", back_populates="portfolios")
    benchmark = relationship("Benchmark", back_populates="portfolios")
    holdings = relationship("Holding", back_populates="portfolio")
    transactions = relationship("Transaction", back_populates="portfolio")
    performance_records = relationship("PerformanceRecord", back_populates="portfolio")
    
    # Indexes
    __table_args__ = (
        Index('idx_portfolio_client', 'client_id'),
        Index('idx_portfolio_type', 'portfolio_type'),
        Index('idx_portfolio_status', 'status'),
        Index('idx_wealth_spectrum_id', 'wealth_spectrum_id'),
    )

class Asset(Base, TimestampMixin):
    """Asset master table - stores all tradeable instruments"""
    __tablename__ = 'assets'
    
    # Primary Key
    asset_id = Column(String(50), primary_key=True)
    
    # Basic Information
    asset_name = Column(String(200), nullable=False)
    asset_type = Column(String(50), nullable=False)  # Equity, Debt, Mutual Fund, ETF, etc.
    asset_class = Column(String(50))  # Large Cap, Mid Cap, Government Bond, etc.
    
    # Identifiers
    isin = Column(String(12), unique=True)
    symbol = Column(String(50))
    exchange = Column(String(50))
    
    # Classification
    sector = Column(String(100))
    industry = Column(String(100))
    market_cap_category = Column(String(20))  # Large, Mid, Small
    
    # Attributes
    currency = Column(String(3), default='INR')
    face_value = Column(Numeric(10, 2))
    lot_size = Column(Integer, default=1)
    
    # Status
    status = Column(String(20), default='Active')
    listing_date = Column(Date)
    delisting_date = Column(Date)
    
    # Relationships
    holdings = relationship("Holding", back_populates="asset")
    transactions = relationship("Transaction", back_populates="asset")
    prices = relationship("AssetPrice", back_populates="asset")
    
    # Indexes
    __table_args__ = (
        Index('idx_asset_name', 'asset_name'),
        Index('idx_asset_type', 'asset_type'),
        Index('idx_asset_class', 'asset_class'),
        Index('idx_isin', 'isin'),
        Index('idx_symbol', 'symbol'),
    )

class AssetPrice(Base, TimestampMixin):
    """Daily asset prices for valuation and performance calculation"""
    __tablename__ = 'asset_prices'
    
    # Composite Primary Key
    asset_id = Column(String(50), ForeignKey('assets.asset_id'), primary_key=True)
    price_date = Column(Date, primary_key=True)
    
    # Price Information
    open_price = Column(Numeric(12, 4))
    high_price = Column(Numeric(12, 4))
    low_price = Column(Numeric(12, 4))
    close_price = Column(Numeric(12, 4), nullable=False)
    volume = Column(Integer)
    
    # Adjusted Prices (for corporate actions)
    adjusted_close = Column(Numeric(12, 4))
    
    # Data Source
    data_source = Column(String(50))  # NSE, BSE, Manual, etc.
    
    # Relationships
    asset = relationship("Asset", back_populates="prices")
    
    # Indexes
    __table_args__ = (
        Index('idx_price_date', 'price_date'),
        Index('idx_asset_price_date', 'asset_id', 'price_date'),
    )

class Holding(Base, TimestampMixin):
    """Current portfolio holdings"""
    __tablename__ = 'holdings'
    
    # Composite Primary Key
    portfolio_id = Column(String(50), ForeignKey('portfolios.portfolio_id'), primary_key=True)
    asset_id = Column(String(50), ForeignKey('assets.asset_id'), primary_key=True)
    
    # Holding Information
    quantity = Column(Numeric(15, 4), nullable=False)
    average_cost = Column(Numeric(12, 4), nullable=False)
    current_price = Column(Numeric(12, 4))
    
    # Calculated Values
    market_value = Column(Numeric(15, 2))
    unrealized_pnl = Column(Numeric(15, 2))
    
    # Dates
    first_purchase_date = Column(Date)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="holdings")
    asset = relationship("Asset", back_populates="holdings")
    
    # Indexes
    __table_args__ = (
        Index('idx_holding_portfolio', 'portfolio_id'),
        Index('idx_holding_asset', 'asset_id'),
    )

class Transaction(Base, TimestampMixin):
    """All portfolio transactions"""
    __tablename__ = 'transactions'
    
    # Primary Key
    transaction_id = Column(String(50), primary_key=True)
    
    # References
    portfolio_id = Column(String(50), ForeignKey('portfolios.portfolio_id'), nullable=False)
    client_id = Column(String(50), ForeignKey('clients.client_id'), nullable=False)
    asset_id = Column(String(50), ForeignKey('assets.asset_id'))
    
    # Transaction Details
    transaction_date = Column(Date, nullable=False)
    transaction_type = Column(String(20), nullable=False)  # Buy, Sell, Dividend, Interest, Fee
    quantity = Column(Numeric(15, 4))
    price = Column(Numeric(12, 4))
    amount = Column(Numeric(15, 2), nullable=False)
    
    # Additional Information
    charges = Column(Numeric(10, 2), default=0)
    taxes = Column(Numeric(10, 2), default=0)
    net_amount = Column(Numeric(15, 2))
    
    # References
    order_id = Column(String(50))
    exchange_ref = Column(String(100))
    
    # Status
    status = Column(String(20), default='Settled')  # Pending, Settled, Cancelled
    settlement_date = Column(Date)
    
    # Data Source
    data_source = Column(String(50))  # Wealth Spectrum, Manual, etc.
    external_ref = Column(String(100))
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="transactions")
    client = relationship("Client", back_populates="transactions")
    asset = relationship("Asset", back_populates="transactions")
    
    # Indexes
    __table_args__ = (
        Index('idx_transaction_portfolio', 'portfolio_id'),
        Index('idx_transaction_client', 'client_id'),
        Index('idx_transaction_date', 'transaction_date'),
        Index('idx_transaction_type', 'transaction_type'),
        Index('idx_transaction_asset', 'asset_id'),
    )

class PerformanceRecord(Base, TimestampMixin):
    """Portfolio performance metrics calculated at various intervals"""
    __tablename__ = 'performance_records'
    
    # Composite Primary Key
    portfolio_id = Column(String(50), ForeignKey('portfolios.portfolio_id'), primary_key=True)
    period_end_date = Column(Date, primary_key=True)
    period_type = Column(String(20), primary_key=True)  # Daily, Monthly, Quarterly, Annual
    
    # Portfolio Values
    beginning_value = Column(Numeric(15, 2))
    ending_value = Column(Numeric(15, 2))
    cash_flows = Column(Numeric(15, 2), default=0)
    
    # Returns
    absolute_return = Column(Numeric(15, 2))
    percentage_return = Column(Numeric(8, 4))
    annualized_return = Column(Numeric(8, 4))
    
    # Risk Metrics
    volatility = Column(Numeric(8, 4))
    max_drawdown = Column(Numeric(8, 4))
    sharpe_ratio = Column(Numeric(8, 4))
    
    # Benchmark Comparison
    benchmark_return = Column(Numeric(8, 4))
    alpha = Column(Numeric(8, 4))
    beta = Column(Numeric(8, 4))
    tracking_error = Column(Numeric(8, 4))
    information_ratio = Column(Numeric(8, 4))
    
    # Advanced Metrics
    sortino_ratio = Column(Numeric(8, 4))
    calmar_ratio = Column(Numeric(8, 4))
    var_95 = Column(Numeric(8, 4))  # Value at Risk 95%
    
    # Calculation Details
    calculation_date = Column(DateTime, default=datetime.utcnow)
    calculation_method = Column(String(50))
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="performance_records")
    
    # Indexes
    __table_args__ = (
        Index('idx_performance_portfolio', 'portfolio_id'),
        Index('idx_performance_date', 'period_end_date'),
        Index('idx_performance_type', 'period_type'),
    )

class Benchmark(Base, TimestampMixin):
    """Benchmark indices for performance comparison"""
    __tablename__ = 'benchmarks'
    
    # Primary Key
    benchmark_id = Column(String(50), primary_key=True)
    
    # Basic Information
    benchmark_name = Column(String(200), nullable=False)
    benchmark_type = Column(String(50))  # Equity, Debt, Hybrid
    provider = Column(String(100))  # NSE, BSE, CRISIL, etc.
    
    # Attributes
    currency = Column(String(3), default='INR')
    base_date = Column(Date)
    base_value = Column(Numeric(10, 2), default=100)
    
    # Status
    status = Column(String(20), default='Active')
    
    # Relationships
    portfolios = relationship("Portfolio", back_populates="benchmark")
    benchmark_values = relationship("BenchmarkValue", back_populates="benchmark")
    
    # Indexes
    __table_args__ = (
        Index('idx_benchmark_name', 'benchmark_name'),
        Index('idx_benchmark_type', 'benchmark_type'),
    )

class BenchmarkValue(Base, TimestampMixin):
    """Daily benchmark values"""
    __tablename__ = 'benchmark_values'
    
    # Composite Primary Key
    benchmark_id = Column(String(50), ForeignKey('benchmarks.benchmark_id'), primary_key=True)
    value_date = Column(Date, primary_key=True)
    
    # Values
    index_value = Column(Numeric(12, 4), nullable=False)
    daily_return = Column(Numeric(8, 4))
    
    # Data Source
    data_source = Column(String(50))
    
    # Relationships
    benchmark = relationship("Benchmark", back_populates="benchmark_values")
    
    # Indexes
    __table_args__ = (
        Index('idx_benchmark_value_date', 'value_date'),
    )

class UserView(Base, TimestampMixin):
    """Saved user dashboard views and filters"""
    __tablename__ = 'user_views'
    
    # Primary Key
    view_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # User Information
    user_id = Column(String(50), nullable=False)
    view_name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # View Configuration
    view_type = Column(String(50), nullable=False)  # Dashboard, Report, Analysis
    filters = Column(JSONB)  # Stored as JSON
    chart_config = Column(JSONB)
    layout_config = Column(JSONB)
    
    # Sharing
    is_public = Column(Boolean, default=False)
    shared_with = Column(JSONB)  # List of user IDs
    
    # Usage Statistics
    access_count = Column(Integer, default=0)
    last_accessed = Column(DateTime)
    
    # Indexes
    __table_args__ = (
        Index('idx_user_views_user', 'user_id'),
        Index('idx_user_views_type', 'view_type'),
        Index('idx_user_views_public', 'is_public'),
    )

class AuditLog(Base):
    """Comprehensive audit logging for compliance"""
    __tablename__ = 'audit_logs'
    
    # Primary Key
    log_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Event Information
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(String(50))
    session_id = Column(String(100))
    
    # Action Details
    action = Column(String(100), nullable=False)  # Login, View, Export, Modify, etc.
    resource_type = Column(String(50))  # Client, Portfolio, Report, etc.
    resource_id = Column(String(50))
    
    # Request Information
    ip_address = Column(String(45))  # IPv6 compatible
    user_agent = Column(Text)
    request_method = Column(String(10))
    request_url = Column(Text)
    
    # Response Information
    response_status = Column(Integer)
    response_time_ms = Column(Integer)
    
    # Additional Data
    details = Column(JSONB)
    
    # Indexes
    __table_args__ = (
        Index('idx_audit_timestamp', 'timestamp'),
        Index('idx_audit_user', 'user_id'),
        Index('idx_audit_action', 'action'),
        Index('idx_audit_resource', 'resource_type', 'resource_id'),
    )

class SystemConfiguration(Base, TimestampMixin):
    """System configuration and settings"""
    __tablename__ = 'system_configuration'
    
    # Primary Key
    config_key = Column(String(100), primary_key=True)
    
    # Configuration Value
    config_value = Column(Text)
    config_type = Column(String(20), default='string')  # string, integer, boolean, json
    
    # Metadata
    description = Column(Text)
    category = Column(String(50))
    is_sensitive = Column(Boolean, default=False)
    
    # Validation
    validation_rule = Column(Text)
    default_value = Column(Text)
    
    # Indexes
    __table_args__ = (
        Index('idx_config_category', 'category'),
    )

# Database utility functions
def create_tables(engine):
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

def get_table_names():
    """Get list of all table names"""
    return [table.name for table in Base.metadata.tables.values()]

def get_model_by_tablename(tablename):
    """Get model class by table name"""
    for cls in Base.registry._class_registry.values():
        if hasattr(cls, '__tablename__') and cls.__tablename__ == tablename:
            return cls
    return None

