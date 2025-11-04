"""
Test suite for SyncManager class in sync.py
Tests all functionality and edge cases
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sync import SyncManager
from config import MAX_RETRIES


class TestSyncManagerInit:
    """Test SyncManager initialization"""
    
    def test_init_with_defaults(self):
        """Test initialization with default parameters"""
        manager = SyncManager()
        assert manager.chunk_size == 100
        assert manager.retry_limit == MAX_RETRIES
        assert manager.enable_cache is False
        assert manager._synced == 0
    
    def test_init_with_custom_chunk_size(self):
        """Test initialization with custom chunk_size"""
        manager = SyncManager(chunk_size=50)
        assert manager.chunk_size == 50
    
    def test_init_with_custom_retry_limit(self):
        """Test initialization with custom retry_limit"""
        manager = SyncManager(retry_limit=5)
        assert manager.retry_limit == 5
    
    def test_init_with_cache_enabled(self):
        """Test initialization with cache enabled"""
        manager = SyncManager(enable_cache=True)
        assert manager.enable_cache is True
    
    def test_init_with_all_parameters(self):
        """Test initialization with all custom parameters"""
        manager = SyncManager(chunk_size=200, retry_limit=7, enable_cache=True)
        assert manager.chunk_size == 200
        assert manager.retry_limit == 7
        assert manager.enable_cache is True
    
    def test_init_chunk_size_minimum_valid(self):
        """Test chunk_size at minimum valid value (1)"""
        manager = SyncManager(chunk_size=1)
        assert manager.chunk_size == 1
    
    def test_init_chunk_size_maximum_valid(self):
        """Test chunk_size at maximum valid value (500)"""
        manager = SyncManager(chunk_size=500)
        assert manager.chunk_size == 500
    
    def test_init_chunk_size_too_small(self):
        """Test that chunk_size < 1 raises ValueError"""
        with pytest.raises(ValueError, match="chunk_size must be between 1 and 500"):
            SyncManager(chunk_size=0)
    
    def test_init_chunk_size_negative(self):
        """Test that negative chunk_size raises ValueError"""
        with pytest.raises(ValueError, match="chunk_size must be between 1 and 500"):
            SyncManager(chunk_size=-10)
    
    def test_init_chunk_size_too_large(self):
        """Test that chunk_size > 500 raises ValueError"""
        with pytest.raises(ValueError, match="chunk_size must be between 1 and 500"):
            SyncManager(chunk_size=501)


class TestSyncManagerConnect:
    """Test SyncManager connect method"""
    
    def test_connect_with_valid_url(self):
        """Test connect with valid HTTPS URL"""
        manager = SyncManager()
        result = manager.connect(
            remote_url="https://example.com/api",
            auth_token="test_token"
        )
        assert result is True
        assert manager.remote_url == "https://example.com/api"
        assert manager.auth_token == "test_token"
        assert manager.timeout == 2  # default
    
    def test_connect_with_custom_timeout(self):
        """Test connect with custom timeout"""
        manager = SyncManager()
        result = manager.connect(
            remote_url="https://example.com/api",
            auth_token="token123",
            timeout=5
        )
        assert result is True
        assert manager.timeout == 5
    
    def test_connect_with_http_url_fails(self):
        """Test that HTTP URL (not HTTPS) raises ConnectionError"""
        manager = SyncManager()
        with pytest.raises(ConnectionError, match="Invalid remote URL"):
            manager.connect(
                remote_url="http://example.com/api",
                auth_token="test_token"
            )
    
    def test_connect_with_invalid_url_fails(self):
        """Test that non-HTTPS URL raises ConnectionError"""
        manager = SyncManager()
        with pytest.raises(ConnectionError, match="Invalid remote URL"):
            manager.connect(
                remote_url="ftp://example.com/api",
                auth_token="test_token"
            )
    
    def test_connect_with_empty_url_fails(self):
        """Test that empty URL raises ConnectionError"""
        manager = SyncManager()
        with pytest.raises(ConnectionError, match="Invalid remote URL"):
            manager.connect(
                remote_url="",
                auth_token="test_token"
            )
    
    def test_connect_stores_auth_token(self):
        """Test that auth_token is stored correctly"""
        manager = SyncManager()
        manager.connect(
            remote_url="https://api.example.com",
            auth_token="secret_token_123"
        )
        assert manager.auth_token == "secret_token_123"


class TestSyncManagerPush:
    """Test SyncManager push method"""
    
    def test_push_with_sync_mode(self):
        """Test push in sync mode"""
        manager = SyncManager()
        manager.connect(
            remote_url="https://example.com/api",
            auth_token="token"
        )
        result = manager.push({"id": 1, "value": "test"}, mode="sync")
        
        assert result == {"status": "ok", "count": 1}
        assert manager._synced == 1
    
    def test_push_with_async_mode(self):
        """Test push in async mode"""
        manager = SyncManager()
        manager.connect(
            remote_url="https://example.com/api",
            auth_token="token"
        )
        result = manager.push({"id": 2, "value": "test2"}, mode="async")
        
        assert result == {"status": "ok", "count": 1}
        assert manager._synced == 1
    
    def test_push_default_mode(self):
        """Test push with default mode (should be sync)"""
        manager = SyncManager()
        manager.connect(
            remote_url="https://example.com/api",
            auth_token="token"
        )
        result = manager.push({"id": 3, "value": "test3"})
        
        assert result == {"status": "ok", "count": 1}
    
    def test_push_multiple_times(self):
        """Test pushing multiple times increments counter"""
        manager = SyncManager()
        manager.connect(
            remote_url="https://example.com/api",
            auth_token="token"
        )
        
        result1 = manager.push({"id": 1}, mode="sync")
        assert result1["count"] == 1
        
        result2 = manager.push({"id": 2}, mode="async")
        assert result2["count"] == 2
        
        result3 = manager.push({"id": 3}, mode="sync")
        assert result3["count"] == 3
    
    def test_push_with_invalid_mode(self):
        """Test that invalid mode raises ValueError"""
        manager = SyncManager()
        manager.connect(
            remote_url="https://example.com/api",
            auth_token="token"
        )
        
        with pytest.raises(ValueError, match="mode must be 'sync' or 'async'"):
            manager.push({"id": 1}, mode="invalid")
    
    def test_push_with_empty_mode(self):
        """Test that empty mode raises ValueError"""
        manager = SyncManager()
        manager.connect(
            remote_url="https://example.com/api",
            auth_token="token"
        )
        
        with pytest.raises(ValueError, match="mode must be 'sync' or 'async'"):
            manager.push({"id": 1}, mode="")
    
    def test_push_with_various_data(self):
        """Test push with different data structures"""
        manager = SyncManager()
        manager.connect(
            remote_url="https://example.com/api",
            auth_token="token"
        )
        
        # Simple dict
        result1 = manager.push({"key": "value"})
        assert result1["status"] == "ok"
        
        # Nested dict
        result2 = manager.push({"user": {"name": "John", "age": 30}})
        assert result2["status"] == "ok"
        
        # Empty dict
        result3 = manager.push({})
        assert result3["status"] == "ok"


class TestSyncManagerGetSyncedCount:
    """Test SyncManager get_synced_count method"""
    
    def test_get_synced_count_initial(self):
        """Test synced count is 0 initially"""
        manager = SyncManager()
        assert manager.get_synced_count() == 0
    
    def test_get_synced_count_after_pushes(self):
        """Test synced count after multiple pushes"""
        manager = SyncManager()
        manager.connect(
            remote_url="https://example.com/api",
            auth_token="token"
        )
        
        assert manager.get_synced_count() == 0
        
        manager.push({"id": 1})
        assert manager.get_synced_count() == 1
        
        manager.push({"id": 2})
        assert manager.get_synced_count() == 2
        
        manager.push({"id": 3})
        assert manager.get_synced_count() == 3
    
    def test_get_synced_count_returns_int(self):
        """Test that get_synced_count returns an integer"""
        manager = SyncManager()
        count = manager.get_synced_count()
        assert isinstance(count, int)


class TestSyncManagerIntegration:
    """Integration tests for complete workflows"""
    
    def test_complete_workflow(self):
        """Test complete workflow from init to multiple pushes"""
        # Initialize
        manager = SyncManager(chunk_size=50, retry_limit=3, enable_cache=True)
        
        # Connect
        connected = manager.connect(
            remote_url="https://api.example.com/sync",
            auth_token="secure_token_123",
            timeout=5
        )
        assert connected is True
        
        # Push multiple items
        items = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"},
        ]
        
        for item in items:
            result = manager.push(item, mode="async")
            assert result["status"] == "ok"
        
        # Verify count
        assert manager.get_synced_count() == 3
    
    def test_multiple_managers_independent(self):
        """Test that multiple SyncManager instances are independent"""
        manager1 = SyncManager(chunk_size=50)
        manager2 = SyncManager(chunk_size=100)
        
        manager1.connect("https://example.com", "token1")
        manager2.connect("https://example.org", "token2")
        
        manager1.push({"id": 1})
        manager1.push({"id": 2})
        
        manager2.push({"id": 1})
        
        assert manager1.get_synced_count() == 2
        assert manager2.get_synced_count() == 1
        assert manager1.auth_token == "token1"
        assert manager2.auth_token == "token2"
