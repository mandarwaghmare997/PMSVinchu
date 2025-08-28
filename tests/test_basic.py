"""
Comprehensive Test Suite for PMS Intelligence Hub
Tests core functionality, data integrity, and performance
Author: Vulnuris Development Team
"""

import unittest
import sys
import os
import pandas as pd
import sqlite3
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'dashboard'))

def test_imports():
    """Test that core modules can be imported"""
    try:
        from main_dashboard import PMSIntelligenceHub
        from flows_tracker import ClientFlowsTracker
        return True
    except ImportError as e:
        print(f"Import failed: {e}")
        return False

def test_dashboard_functionality():
    """Test basic dashboard functionality"""
    try:
        from main_dashboard import PMSIntelligenceHub
        dashboard = PMSIntelligenceHub()
        
        # Test data loading
        data = dashboard.load_sample_data()
        assert len(data) == 150, f"Expected 150 records, got {len(data)}"
        
        # Test required columns
        required_columns = ['client_id', 'client_name', 'current_aum', 'rm_name']
        for col in required_columns:
            assert col in data.columns, f"Missing column: {col}"
        
        print("✅ Dashboard functionality test passed")
        return True
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        return False

def test_flows_tracker():
    """Test flows tracker functionality"""
    try:
        from flows_tracker import ClientFlowsTracker
        tracker = ClientFlowsTracker("test_flows.db")
        
        # Test flows generation
        flows = tracker.generate_sample_flows(5)
        assert len(flows) > 0, "No flows generated"
        
        # Clean up
        if os.path.exists("test_flows.db"):
            os.remove("test_flows.db")
        
        print("✅ Flows tracker test passed")
        return True
    except Exception as e:
        print(f"❌ Flows tracker test failed: {e}")
        return False

def test_data_integrity():
    """Test data integrity and calculations"""
    try:
        from main_dashboard import PMSIntelligenceHub
        dashboard = PMSIntelligenceHub()
        data = dashboard.load_sample_data()
        
        # Test data types
        assert pd.api.types.is_numeric_dtype(data['current_aum']), "AUM should be numeric"
        assert pd.api.types.is_numeric_dtype(data['annualised_returns']), "Returns should be numeric"
        
        # Test data ranges
        assert all(data['current_aum'] > 0), "AUM should be positive"
        assert all(data['age_of_client'] >= 25), "Age should be >= 25"
        assert all(data['age_of_client'] <= 75), "Age should be <= 75"
        
        print("✅ Data integrity test passed")
        return True
    except Exception as e:
        print(f"❌ Data integrity test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running PMS Intelligence Hub Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Dashboard Functionality", test_dashboard_functionality),
        ("Flows Tracker", test_flows_tracker),
        ("Data Integrity", test_data_integrity)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for deployment.")
    else:
        print("⚠️ Some tests failed. Please review the issues above.")

