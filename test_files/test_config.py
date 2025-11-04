"""
Test suite for config.py module
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import MAX_RETRIES


class TestConfig:
    """Test configuration constants"""
    
    def test_max_retries_exists(self):
        """Test that MAX_RETRIES constant exists"""
        assert MAX_RETRIES is not None
    
    def test_max_retries_value(self):
        """Test that MAX_RETRIES has the correct value"""
        assert MAX_RETRIES == 10
    
    def test_max_retries_type(self):
        """Test that MAX_RETRIES is an integer"""
        assert isinstance(MAX_RETRIES, int)
    
    def test_max_retries_positive(self):
        """Test that MAX_RETRIES is positive"""
        assert MAX_RETRIES > 0
