"""
Basic tests for PMS Intelligence Hub
Essential functionality testing only
"""

import pytest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that core modules can be imported"""
    try:
        from dashboard.main_dashboard import main
        from dashboard.utils.data_loader import DataLoader
        from dashboard.utils.calculations import PerformanceCalculator
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_data_loader_init():
    """Test DataLoader initialization"""
    from dashboard.utils.data_loader import DataLoader
    loader = DataLoader()
    assert loader is not None

def test_performance_calculator_init():
    """Test PerformanceCalculator initialization"""
    from dashboard.utils.calculations import PerformanceCalculator
    calc = PerformanceCalculator()
    assert calc is not None

if __name__ == "__main__":
    pytest.main([__file__])

