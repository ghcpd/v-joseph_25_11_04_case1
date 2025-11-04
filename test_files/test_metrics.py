"""
Test suite for metrics.py module
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from metrics import get_latency


class TestMetrics:
    """Test metrics functions"""
    
    def test_get_latency_exists(self):
        """Test that get_latency function exists"""
        assert callable(get_latency)
    
    def test_get_latency_returns_float(self):
        """Test that get_latency returns a float"""
        latency = get_latency()
        assert isinstance(latency, float)
    
    def test_get_latency_value(self):
        """Test that get_latency returns expected value"""
        latency = get_latency()
        assert latency == 0.352
    
    def test_get_latency_positive(self):
        """Test that latency is positive"""
        latency = get_latency()
        assert latency > 0
    
    def test_get_latency_consistent(self):
        """Test that get_latency returns consistent value"""
        latency1 = get_latency()
        latency2 = get_latency()
        assert latency1 == latency2
    
    def test_get_latency_no_parameters(self):
        """Test that get_latency takes no parameters"""
        # Should not raise any errors
        latency = get_latency()
        assert latency is not None
