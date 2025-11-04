"""
Integration tests for the complete datasync library
Tests the interaction between all modules
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sync import SyncManager
from config import MAX_RETRIES
from metrics import get_latency


class TestLibraryIntegration:
    """Integration tests across all modules"""
    
    def test_import_all_modules(self):
        """Test that all modules can be imported"""
        assert SyncManager is not None
        assert MAX_RETRIES is not None
        assert get_latency is not None
    
    def test_config_used_in_sync(self):
        """Test that config.MAX_RETRIES is used as default in SyncManager"""
        manager = SyncManager()
        assert manager.retry_limit == MAX_RETRIES
    
    def test_complete_use_case_with_metrics(self):
        """Test complete use case including metrics"""
        # Initialize manager
        manager = SyncManager(chunk_size=50, retry_limit=5)
        
        # Connect
        manager.connect(
            remote_url="https://api.example.com/data",
            auth_token="test_token_123",
            timeout=3
        )
        
        # Push data
        for i in range(5):
            result = manager.push(
                {"id": i, "value": f"item_{i}"},
                mode="async"
            )
            assert result["status"] == "ok"
        
        # Get metrics
        synced = manager.get_synced_count()
        latency = get_latency()
        
        # Verify
        assert synced == 5
        assert isinstance(latency, float)
        assert latency > 0
    
    def test_readme_corrected_example(self):
        """Test the corrected example from corrected_readme.md"""
        from sync import SyncManager
        
        manager = SyncManager(chunk_size=50, retry_limit=3)
        
        manager.connect(
            remote_url="https://example.com/data",
            auth_token="your_auth_token_here",
            timeout=2
        )
        
        result = manager.push({"id": 1, "value": "abc"}, mode="async")
        
        synced_count = manager.get_synced_count()
        
        assert result["status"] == "ok"
        assert result["count"] == 1
        assert synced_count == 1
    
    def test_readme_complete_example(self):
        """Test the complete working example from corrected_readme.md"""
        from sync import SyncManager
        from metrics import get_latency
        
        # Initialize with custom settings
        manager = SyncManager(
            chunk_size=50,
            retry_limit=5,
            enable_cache=True
        )
        
        # Connect to remote server
        manager.connect(
            remote_url="https://api.example.com/sync",
            auth_token="your_secure_token",
            timeout=3
        )
        
        # Push data in async mode
        data_items = [
            {"id": 1, "value": "first"},
            {"id": 2, "value": "second"},
            {"id": 3, "value": "third"}
        ]
        
        for item in data_items:
            result = manager.push(item, mode="async")
            assert result["status"] == "ok"
        
        # Get sync statistics
        total_synced = manager.get_synced_count()
        latency = get_latency()
        
        assert total_synced == 3
        assert latency == 0.352
    
    def test_both_modes_work(self):
        """Test that both sync and async modes work correctly"""
        manager = SyncManager()
        manager.connect("https://example.com", "token")
        
        # Test sync mode
        result_sync = manager.push({"id": 1}, mode="sync")
        assert result_sync["status"] == "ok"
        assert result_sync["count"] == 1
        
        # Test async mode
        result_async = manager.push({"id": 2}, mode="async")
        assert result_async["status"] == "ok"
        assert result_async["count"] == 2
        
        # Verify total count
        assert manager.get_synced_count() == 2
    
    def test_error_handling_invalid_chunk_size(self):
        """Test error handling for invalid chunk_size"""
        with pytest.raises(ValueError):
            SyncManager(chunk_size=0)
        
        with pytest.raises(ValueError):
            SyncManager(chunk_size=501)
    
    def test_error_handling_invalid_url(self):
        """Test error handling for invalid URL"""
        manager = SyncManager()
        
        with pytest.raises(ConnectionError):
            manager.connect("http://insecure.com", "token")
    
    def test_error_handling_invalid_mode(self):
        """Test error handling for invalid push mode"""
        manager = SyncManager()
        manager.connect("https://example.com", "token")
        
        with pytest.raises(ValueError):
            manager.push({"id": 1}, mode="invalid")
