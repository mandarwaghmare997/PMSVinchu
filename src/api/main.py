"""
FastAPI Main Application for PMS Intelligence Hub
Provides REST API endpoints for dashboard functionality
"""

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import logging
from typing import List, Optional, Dict, Any
import os
from datetime import datetime, timedelta

# Import API endpoints
from .endpoints import (
    clients, portfolios, performance, 
    reports, dashboard, auth, admin
)

# Import database and utilities
from ..database.connection import get_db_session
from ..database.models import AuditLog
from ..config.settings import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting PMS Intelligence Hub API")
    yield
    # Shutdown
    logger.info("Shutting down PMS Intelligence Hub API")

# Create FastAPI application
app = FastAPI(
    title="PMS Intelligence Hub API",
    description="REST API for Portfolio Management Services Dashboard",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Custom middleware for request logging and timing
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests for audit purposes"""
    start_time = time.time()
    
    # Extract request information
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")
    method = request.method
    url = str(request.url)
    
    # Process request
    response = await call_next(request)
    
    # Calculate response time
    process_time = time.time() - start_time
    response_time_ms = int(process_time * 1000)
    
    # Log request (in production, this would go to audit log table)
    logger.info(
        f"{method} {url} - {response.status_code} - "
        f"{response_time_ms}ms - {client_ip}"
    )
    
    # Add response time header
    response.headers["X-Process-Time"] = str(response_time_ms)
    
    return response

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

# API Information endpoint
@app.get("/info", tags=["System"])
async def api_info():
    """API information endpoint"""
    return {
        "name": "PMS Intelligence Hub API",
        "version": "1.0.0",
        "description": "REST API for Portfolio Management Services Dashboard",
        "endpoints": {
            "authentication": "/auth",
            "clients": "/clients",
            "portfolios": "/portfolios", 
            "performance": "/performance",
            "reports": "/reports",
            "dashboard": "/dashboard",
            "admin": "/admin"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

# Include API routers
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    clients.router,
    prefix="/clients",
    tags=["Clients"]
)

app.include_router(
    portfolios.router,
    prefix="/portfolios",
    tags=["Portfolios"]
)

app.include_router(
    performance.router,
    prefix="/performance",
    tags=["Performance"]
)

app.include_router(
    reports.router,
    prefix="/reports",
    tags=["Reports"]
)

app.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"]
)

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["Administration"]
)

# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API welcome message"""
    return {
        "message": "Welcome to PMS Intelligence Hub API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

